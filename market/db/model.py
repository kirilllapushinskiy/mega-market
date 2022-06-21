from sqlalchemy import (
    Column,
    Enum,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, declarative_base

from market.api import schemas

Base = declarative_base()


class ShopUnit(Base):
    __tablename__ = "shop_units"
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(Enum(schemas.ShopUnitType), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=True)


class Category(Base):
    __tablename__ = "categories"
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    total_price = Column(Integer, nullable=True)
    offers_number = Column(Integer, nullable=False, default=0)


class Offer(Base):
    __tablename__ = "offers"
    uuid = Column(UUID(as_uuid=True), primary_key=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)


class CategoryHistory(Base):
    __tablename__ = "categories_history"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    total_price = Column(Integer, nullable=True)
    offers_number = Column(Integer, nullable=False, default=0)


class OffersHistory(Base):
    __tablename__ = "offers_history"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), ForeignKey("offers.uuid", ondelete="CASCADE"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.uuid", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)
