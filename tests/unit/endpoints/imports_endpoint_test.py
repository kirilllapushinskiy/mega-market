import pytest
import requests


@pytest.fixture
def endpoint(host):
    return host + "/imports"


class TestValidRequestsToImportsEndpoint:

    def test_post_1(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 200

    def test_post_2(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Смартфоны",
                        "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                    },
                    {
                        "type": "OFFER",
                        "name": "jPhone 13",
                        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "price": 79999
                    },
                    {
                        "type": "OFFER",
                        "name": "Xomiа Readme 10",
                        "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                        "price": 59999
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200

    def test_post_3(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Телевизоры",
                        "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                    },
                    {
                        "type": "OFFER",
                        "name": "Samson 70\" LED UHD Smart",
                        "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 32999
                    },
                    {
                        "type": "OFFER",
                        "name": "Phyllis 50\" LED UHD Smarter",
                        "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 49999
                    }
                ],
                "updateDate": "2022-02-03T12:00:00.000Z"
            }
        )
        assert response.status_code == 200

    def test_post_4(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Goldstar 65\" LED UHD LOL Very Smart",
                        "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 69999
                    }
                ],
                "updateDate": "2022-06-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 200

    def test_import_offer_and_then_offer_category_in_same_request(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Teapot 2.0",
                        "id": "918d241a-1c48-4125-a465-456bae2199bb",
                        "parentId": "23ab4aac-63d1-4876-9c8d-bc3f113de4d3",
                        "price": 1099
                    },
                    {
                        "type": "CATEGORY",
                        "name": "Teapots",
                        "id": "23ab4aac-63d1-4876-9c8d-bc3f113de4d3",
                    }
                ],
                "updateDate": "2022-11-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 200

    def test_import_offer_and_then_category_category_in_same_request(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Extra Small teapots",
                        "id": "adcd5045-c22f-4716-87e8-311b4b2b8c38",
                        "parentId": "b492dc16-c399-4b4a-b111-9318e3e399e6",
                    },
                    {
                        "type": "CATEGORY",
                        "name": "Small teapots",
                        "id": "b492dc16-c399-4b4a-b111-9318e3e399e6",
                        "parentId": "17ecfdfa-8640-489d-ab24-fa91956728b8",
                    },
                    {
                        "type": "CATEGORY",
                        "name": "Teapots",
                        "id": "17ecfdfa-8640-489d-ab24-fa91956728b8",
                    }
                ],
                "updateDate": "2022-11-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 200

    def test_import_offer_and_then_category_and_offer_category_in_same_request(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Extra Small teapots",
                        "id": "5df4a525-406a-4580-ae26-f4577b903cda",
                        "parentId": "a39697c3-1362-49f7-9442-6a31a9cffb1c",
                    },
                    {
                        "type": "CATEGORY",
                        "name": "Small teapots",
                        "id": "a39697c3-1362-49f7-9442-6a31a9cffb1c",
                        "parentId": "4a5609a1-c4bc-4970-94aa-3aea782cab87",
                    },
                    {
                        "type": "CATEGORY",
                        "name": "Teapots",
                        "id": "4a5609a1-c4bc-4970-94aa-3aea782cab87",
                    },
                    {
                        "type": "OFFER",
                        "name": "Small Teapot",
                        "id": "f3e69b87-5488-4d4a-b183-937e0d1a27ed",
                        "parentId": "a39697c3-1362-49f7-9442-6a31a9cffb1c",
                        "price": 1080
                    },
                    {
                        "type": "OFFER",
                        "name": "Extra Small teapot",
                        "id": "724a4542-e7b0-4ae6-be38-30473bbe5122",
                        "parentId": "5df4a525-406a-4580-ae26-f4577b903cda",
                        "price": 900
                    }
                ],
                "updateDate": "2022-11-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 200


class TestInvalidRequestsToImportsEndpoint:
    def test_non_uuid_id(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": "bbdd-47d3-ad8f",
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_int_id(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Товары",
                        "id": 1000,
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_type(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "SOMETHING",
                        "name": "Товары",
                        "id": 1000,
                        "parentId": None
                    }
                ],
                "updateDate": "2022-02-01T12:00:00.000Z"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_duplicate_uuid(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Goldstar 65\" LED UHD LOL Very Smart",
                        "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 69999
                    },
                    {
                        "type": "OFFER",
                        "name": "Goldstar 77",
                        "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                        "price": 57567
                    }
                ],
                "updateDate": "2022-06-13T03:06:22+00:00"
            }
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_none_price(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "OPPO",
                        "id": "d515e43f-f3f6-4471-xx77-6b455017a2d2"
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_cat_price(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Умные дома",
                        "id": "bc88321d-19ba-49a3-ba88-baac67500f75",
                        "price": 777
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_global_unique_uuid(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Умные дома",
                        "id": "9d9c9554-88f2-470a-b41d-fd100d56d3be",
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Умный дом",
                        "id": "9d9c9554-88f2-470a-b41d-fd100d56d3be",
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_negative_price(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "OPPO",
                        "id": "d515e43f-f3f6-4471-xx77-6b455017a2d2",
                        "price": -9999
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_offer_as_offer_parent(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Network card",
                        "id": "70761699-9fee-4a4c-9515-ab75a8ad54be",
                        "price": 2300
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Smart card",
                        "id": "596337f2-f5ca-4db9-ab86-70f6f774a129",
                        "price": 1999,
                        "parentId": "70761699-9fee-4a4c-9515-ab75a8ad54be"
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_offer_as_category_parent(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Network card 2",
                        "id": "b331257e-637d-42f8-ac6f-5585aa868cfc",
                        "price": 2300
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Smart cards",
                        "id": "6e0f83cd-fd0d-4702-bd9a-6167a8e37ae9",
                        "parentId": "b331257e-637d-42f8-ac6f-5585aa868cfc"
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_replace_offer_by_category(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Network card 3",
                        "id": "3eece73d-ebf3-4e4a-9746-abff847b8284",
                        "price": 2300
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Network cards",
                        "id": "3eece73d-ebf3-4e4a-9746-abff847b8284",
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_replace_category_by_offer(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "CATEGORY",
                        "name": "Displays",
                        "id": "bc64aeef-2ce7-475c-961e-4770988011de",
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Display 15.4",
                        "id": "bc64aeef-2ce7-475c-961e-4770988011de",
                    }
                ],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_empty_items(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [],
                "updateDate": "2022-02-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }

    def test_non_category_parent(self, endpoint):
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Notebook Asus ROG",
                        "id": "394555d9-9e93-4aea-bcf9-28580b9dee3c",
                        "price": 114000
                    }
                ],
                "updateDate": "2022-10-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 200
        response = requests.post(
            endpoint,
            json={
                "items": [
                    {
                        "type": "OFFER",
                        "name": "Notebook Asus ROG II",
                        "id": "88f5e2ac-fe01-4a63-ab58-b7179be181ed",
                        "parentId": "394555d9-9e93-4aea-bcf9-28580b9dee3c",
                        "price": 114000
                    }
                ],
                "updateDate": "2022-10-02T12:00:00.000Z"
            },
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": 400,
            "message": "Validation Failed"
        }
