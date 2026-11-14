import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from catalog.models import Coffee, Origin


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        username="user1", password="password123", is_staff=False
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin1", password="password123", is_staff=True
    )


@pytest.fixture
def auth_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def sample_origin():
    return Origin.objects.create(
        country="Ефіопія", region="Їргачеф", altitude="1800-2200 м"
    )


@pytest.fixture
def sample_coffee(sample_origin):
    return Coffee.objects.create(
        title="Arabica Ethiopia",
        description="Квітковий аромат з нотами бергамоту",
        price=350.00,
        weight_grams=250,
        roast_level="light",
        processing_method="washed",
        flavor_notes="Жасмин, бергамот, лимон",
        stock_quantity=10,
        origin=sample_origin,
    )


@pytest.mark.django_db
class TestCoffeeAPI:
    def test_get_coffees_public(self, api_client, sample_coffee):
        response = api_client.get("/api/coffees/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == sample_coffee.title

    def test_get_coffee_detail_not_found(self, api_client):
        response = api_client.get("/api/coffees/9999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_coffee_unauthorized(self, api_client, sample_origin):
        data = {
            "title": "Robusta",
            "price": 200.00,
            "weight_grams": 250,
            "roast_level": "dark",
            "processing_method": "natural",
            "flavor_notes": "Шоколад, горіхи",
            "stock_quantity": 5,
            "origin": sample_origin.id,
        }
        response = api_client.post("/api/coffees/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_coffee_regular_user_forbidden(self, auth_client, sample_origin):
        data = {
            "title": "Robusta",
            "price": 200.00,
            "weight_grams": 250,
            "roast_level": "dark",
            "processing_method": "natural",
            "flavor_notes": "Шоколад, горіхи",
            "stock_quantity": 5,
            "origin": sample_origin.id,
        }
        response = auth_client.post("/api/coffees/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_coffee_admin_success(self, admin_client, sample_origin):
        data = {
            "title": "Colombia Geisha",
            "price": 600.00,
            "weight_grams": 250,
            "roast_level": "light",
            "processing_method": "washed",
            "flavor_notes": "Жасмин, цитруси",
            "stock_quantity": 4,
            "origin": sample_origin.id,
        }
        response = admin_client.post("/api/coffees/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Coffee.objects.count() == 1
        assert Coffee.objects.first().title == "Colombia Geisha"

    def test_create_coffee_invalid_data(self, admin_client):
        data = {"title": ""}
        response = admin_client.post("/api/coffees/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_coffee_admin_success(self, admin_client, sample_coffee):
        response = admin_client.patch(
            f"/api/coffees/{sample_coffee.id}/",
            {"price": 420.00, "stock_quantity": 15},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        sample_coffee.refresh_from_db()
        assert float(sample_coffee.price) == 420.00
        assert sample_coffee.stock_quantity == 15

    def test_update_coffee_regular_user_forbidden(self, auth_client, sample_coffee):
        response = auth_client.patch(
            f"/api/coffees/{sample_coffee.id}/",
            {"price": 100.00},
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_coffee_regular_user_forbidden(self, auth_client, sample_coffee):
        response = auth_client.delete(f"/api/coffees/{sample_coffee.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Coffee.objects.count() == 1

    def test_delete_coffee_admin_success(self, admin_client, sample_coffee):
        response = admin_client.delete(f"/api/coffees/{sample_coffee.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Coffee.objects.count() == 0

    def test_delete_coffee_not_found(self, admin_client):
        response = admin_client.delete("/api/coffees/9999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
