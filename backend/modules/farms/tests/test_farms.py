"""
Unit and integration tests for Farm Management (`modules.farms`).
Verifies Farm profile CRUD, area/coordinate validation, soft deletion, archiving, and activity logging.
"""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.exceptions import ValidationError
from modules.farms.models.farm import Farm
from modules.farms.models.farm_activity import FarmActivity
from modules.farms.services.farm_service import FarmActivityService, FarmService

User = get_user_model()


@pytest.fixture
def farmer_user(db):
    return User.objects.create_user(
        username="farmer_test",
        email="farmer_test@dhatree.ai",
        password="TestPassword123!",
        full_name="Test Farmer",
        role="farmer",
    )


@pytest.fixture
def api_client(farmer_user):
    client = APIClient()
    client.force_authenticate(user=farmer_user)
    return client


@pytest.mark.django_db
class TestFarmService:
    def test_create_farm_success(self, farmer_user):
        service = FarmService()
        farm = service.create_farm(
            owner=farmer_user,
            farm_name="Green Acres Farm",
            area=Decimal("12.50"),
            unit="acres",
            latitude=Decimal("19.0760"),
            longitude=Decimal("72.8777"),
            state="Maharashtra",
            district="Pune",
        )
        assert farm.id is not None
        assert farm.farm_name == "Green Acres Farm"
        assert farm.area == Decimal("12.50")
        assert farm.is_deleted is False
        assert farm.status == Farm.Status.ACTIVE

    def test_create_farm_invalid_area(self, farmer_user):
        service = FarmService()
        with pytest.raises(ValidationError, match="Total farm area must be greater than 0"):
            service.create_farm(
                owner=farmer_user,
                farm_name="Negative Area Farm",
                area=Decimal("-5.00"),
            )

    def test_create_farm_invalid_latitude(self, farmer_user):
        service = FarmService()
        with pytest.raises(ValidationError, match="Latitude must be between -90.0 and 90.0"):
            service.create_farm(
                owner=farmer_user,
                farm_name="Out of bounds Farm",
                area=Decimal("10.00"),
                latitude=Decimal("95.5000"),
            )

    def test_create_duplicate_farm_name(self, farmer_user):
        service = FarmService()
        service.create_farm(
            owner=farmer_user,
            farm_name="Sunrise Orchard",
            area=Decimal("5.00"),
        )
        with pytest.raises(ValidationError, match="already have an active farm named 'Sunrise Orchard'"):
            service.create_farm(
                owner=farmer_user,
                farm_name="Sunrise Orchard",
                area=Decimal("8.00"),
            )

    def test_soft_delete_and_archive_farm(self, farmer_user):
        service = FarmService()
        farm = service.create_farm(owner=farmer_user, farm_name="Archive Me", area=Decimal("4.00"))
        
        # Test archive
        archived = service.archive_farm(farm.id)
        assert archived.status == Farm.Status.ARCHIVED

        # Test soft delete
        service.soft_delete_farm(farm.id)
        farm.refresh_from_db()
        assert farm.is_deleted is True
        assert farm.deleted_at is not None
        assert Farm.active_objects.filter(pk=farm.id).exists() is False
        assert Farm.objects.filter(pk=farm.id).exists() is True


@pytest.mark.django_db
class TestFarmActivityService:
    def test_log_activity_success(self, farmer_user):
        farm_service = FarmService()
        farm = farm_service.create_farm(owner=farmer_user, farm_name="Activity Farm", area=Decimal("10.00"))

        act_service = FarmActivityService()
        activity = act_service.log_activity(
            farm_id=farm.id,
            performed_by=farmer_user,
            activity_type=FarmActivity.ActivityType.IRRIGATION,
            title="Drip irrigation cycle",
            cost_incurred=Decimal("1500.00"),
        )
        assert activity.id is not None
        assert activity.farm == farm
        assert activity.cost_incurred == Decimal("1500.00")

    def test_log_activity_negative_cost(self, farmer_user):
        farm_service = FarmService()
        farm = farm_service.create_farm(owner=farmer_user, farm_name="Cost Farm", area=Decimal("10.00"))

        act_service = FarmActivityService()
        with pytest.raises(ValidationError, match="Cost incurred cannot be negative"):
            act_service.log_activity(
                farm_id=farm.id,
                title="Bad cost activity",
                cost_incurred=Decimal("-200.00"),
            )


@pytest.mark.django_db
class TestFarmAPIEndpoints:
    def test_list_farms_api(self, api_client, farmer_user):
        Farm.objects.create(owner=farmer_user, farm_name="API Farm 1", area=Decimal("15.00"))
        response = api_client.get("/api/v1/farms/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]["results"]) == 1
        assert response.data["data"]["results"][0]["farm_name"] == "API Farm 1"

    def test_create_farm_api(self, api_client):
        payload = {
            "farm_name": "API Created Farm",
            "area": "25.50",
            "unit": "acres",
            "latitude": "18.5204",
            "longitude": "73.8567",
            "water_source": "tube_well",
        }
        response = api_client.post("/api/v1/farms/", data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["farm_name"] == "API Created Farm"
        assert response.data["data"]["area"] == "25.50"
