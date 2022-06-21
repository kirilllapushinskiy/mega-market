from datetime import datetime
from typing import List, Dict, Set, Tuple
from uuid import UUID

from sqlalchemy import select, func, update, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import model


def prepare(unit_import: schemas.ShopUnitImportRequest) -> Tuple[List, List, List, Dict]:
    """
    Подготовка данных для вставки/обновления: категории и товары
    разделяются на отдельные списки, создается общий список юнитов.
    Кроме того собирается словарь uuid-тип для того чтобы в функции handle,
    можно было проверить не изменяется ли тип уже существующего юнита.
    :raise ValidationFailed400: в случае невалидных данный выбрасывается исключение.
    """
    if not unit_import.items:
        raise ValidationFailed400("empty list of units")
    categorise, offers, units, types = [], [], [], {}
    for unit in unit_import.items:
        # Проверка уникальности uuid в рамках запроса.
        if unit.id in types:
            raise ValidationFailed400("duplicate uuid in a single request")
        types[unit.id] = unit.type
        if unit.type == 'CATEGORY':
            # Проверка, что у категории отсутствует цена.
            if unit.price is not None:
                raise ValidationFailed400("unit with the CATEGORY type cannot contain  a price field")
            categorise.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date,
            })
        elif unit.type == 'OFFER':
            # Проверка, что у товара присутствует цена.
            if unit.price is None:
                raise ValidationFailed400("unit with the OFFER type must contain a price field")
            offers.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date,
                'price': unit.price
            })
        units.append({'uuid': unit.id, 'type': unit.type, 'parent_id': unit.parent_id})
    return categorise, offers, units, types


async def parents(units: List[Dict], uuids: Dict, session: Session) -> Set[UUID]:
    """
    Находит все категории, которые необходимо обновить из-за вставки новых или
    изменения уже существующих данных прямо или косвенно влияющих
    на среднюю цену и дату родительских каталогов.
    :param uuids: словарь со всеми импортируемыми uuid.
    :param units: список словарей для вставки/обновления.
    :param session: сессия БД.
    :return: множество uuid всех категорий дата и средняя ценя которых подлежит обновлению.
    """
    updated_categories = set()
    import_categories = {u for u, t in uuids.items() if t == schemas.ShopUnitType.CATEGORY}
    # Добавление родительских категорий элементов импорта.
    all_parents = {unit['parent_id'] for unit in units}
    # Добавление родительских категорий элементов до импорта.
    all_parents |= set((await session.execute(
        select(model.ShopUnit.parent_id).
        where(model.ShopUnit.uuid.in_(uuids))
    )).scalars()) - {None}
    for parent_uuid in all_parents:
        while parent_uuid:
            # Если данный каталог уже в множестве, то не имеет смысла искать его предков.
            if parent_uuid in updated_categories:
                break
            updated_categories.add(parent_uuid)
            # Получаем следующую категорию верхнего уровня.
            parent_uuid = (await session.execute(
                select(model.Category.parent_id).
                where(model.Category.uuid == parent_uuid)
            )).scalar()
    updated_categories |= import_categories
    updated_categories.discard(None)
    return updated_categories


async def insert_imported_units(
        categorise: List[dict],
        offers: List[dict],
        units: List[dict],
        types: Dict,
        session: Session
):
    # Получаем типы юнитов, которые ВОЗМОЖНО будем обновлять.
    result = await session.execute(
        select(model.ShopUnit).
        where(model.ShopUnit.uuid.in_(types))
    )
    # Проверяем что не изменяется тип уже существующего юнита.
    for u, in result.all():
        if u.type != types[u.uuid]:
            raise ValidationFailed400("it is not allowed to change the unit type")
    # Вставка/обновление категорий.
    if categorise:
        category_insert_stmt = insert(model.Category).values(categorise)
        await session.execute(
            category_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=category_insert_stmt.excluded
            ))
    # Вставляем НОВЫЕ юниты. Вставка происходит ОБЯЗАТЕЛЬНО после категорий,
    # иначе каталога юнита может ЕЩЁ НЕ БЫТЬ в базе данных.
    unit_insert_stmt = insert(model.ShopUnit).values(units)
    await session.execute(
        unit_insert_stmt.
        on_conflict_do_update(
            index_elements=['uuid'],
            set_=unit_insert_stmt.excluded
        ))
    # Вставка/обновление товаров.
    if offers:
        offer_insert_stmt = insert(model.Offer).values(offers)
        await session.execute(
            offer_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=offer_insert_stmt.excluded
            ))
        await session.execute(insert(model.OffersHistory).values(offers))


async def update_categories_stats(parent_uuids: set, session: Session):
    cache = {}
    miss, strike = 0, 0
    for target_uuid in parent_uuids:
        stack = [target_uuid]
        number, total = 0, 0
        while stack:
            current_parent = stack.pop()
            if current_parent in cache:
                strike += 1
                number += cache[current_parent][0]
                total += cache[current_parent][1]
                continue
            miss += 1
            # Получаем товары каталога.
            (current_number, current_total), = (await session.execute(
                select(
                    [
                        func.count(model.Offer.uuid),
                        func.sum(model.Offer.price)
                    ]
                ).
                where(model.Offer.parent_id == current_parent)
            )).all()
            current_total = current_total or 0
            total += current_total
            number += current_number
            # Получаем подкатегории.
            sub_categories = (await session.execute(
                select(model.Category.uuid, model.Category.offers_number, model.Category.total_price).
                where(model.Category.parent_id == current_parent)
            )).all()
            if not sub_categories:
                cache[current_parent] = (current_number, current_total)
            else:
                for sub_uuid, sub_number, sub_total in sub_categories:
                    if sub_uuid not in parent_uuids:
                        total += sub_total
                        number += sub_number
                    else:
                        stack.append(sub_uuid)
        cache[target_uuid] = (number, total)
    return cache


async def save_updated_stats(updated_stats: dict, update_date: datetime, session: Session):
    to_save = []
    updated_categories = (await session.execute(
        select(model.Category).
        where(model.Category.uuid.in_(updated_stats))
    )).scalars()
    for c in updated_categories:
        offers_number, total_price = updated_stats[c.uuid]
        to_save.append({
            '_uuid': c.uuid,
            'total_price': total_price,
            'offers_number': offers_number,
            'date': update_date,
            'name': c.name,
            'parent_id': c.parent_id
        })
    await session.execute(insert(model.CategoryHistory).values(
        uuid=bindparam('_uuid'),
        total_price=bindparam('total_price'),
        offers_number=bindparam('offers_number'),
        date=bindparam('date'),
        parent_id=bindparam('parent_id'),
        name=bindparam('name')
    ), to_save)
    await session.execute(
        update(model.Category).
        where(model.Category.uuid == bindparam('_uuid')).
        values(
            date=bindparam('date'),
            total_price=bindparam('total_price'),
            offers_number=bindparam('offers_number')
        ), to_save
    )


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    Вставка и валидация данных, полученных от пользователя, в рамках одной транзакции.
    :raise ValidationFailed400: выбрасывает исключение, если данные невалидны.
    """
    categorise, offers, units, types = prepare(unit_import)
    async with Session() as s:
        async with s.begin():
            try:
                await insert_imported_units(categorise, offers, units, types, s)
                parent_uuids = await parents(units, uuids=types, session=s)
                if not parent_uuids:
                    return
                updated_stats = await update_categories_stats(parent_uuids, s)
                await save_updated_stats(updated_stats, unit_import.update_date, s)
            except IntegrityError as err:
                raise ValidationFailed400(err)
