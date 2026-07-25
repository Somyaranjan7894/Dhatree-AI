"""
Serializers for Farm, FarmCrop, FarmImage, and FarmActivity models.
Enforces strict input validation and formats clean JSON representations.
"""
from rest_framework import serializers
from modules.farms.models.farm import Farm
from modules.farms.models.farm_activity import FarmActivity
from modules.farms.models.farm_crop import FarmCrop
from modules.farms.models.farm_image import FarmImage


class FarmImageSerializer(serializers.ModelSerializer):
    """Serializer for FarmImage observation records."""

    image_type_display = serializers.CharField(source="get_image_type_display", read_only=True)

    class Meta:
        model = FarmImage
        fields = [
            "id",
            "farm",
            "farm_crop",
            "image",
            "image_type",
            "image_type_display",
            "caption",
            "taken_at",
            "created_at",
        ]
        read_only_fields = ["id", "farm", "created_at"]


class FarmActivitySerializer(serializers.ModelSerializer):
    """Serializer for FarmActivity history log entries."""

    activity_type_display = serializers.CharField(source="get_activity_type_display", read_only=True)
    performed_by_name = serializers.CharField(source="performed_by.username", read_only=True, default=None)

    class Meta:
        model = FarmActivity
        fields = [
            "id",
            "farm",
            "farm_crop",
            "performed_by",
            "performed_by_name",
            "activity_type",
            "activity_type_display",
            "activity_date",
            "title",
            "description",
            "cost_incurred",
            "created_at",
        ]
        read_only_fields = ["id", "farm", "performed_by", "created_at"]


class FarmCropSerializer(serializers.ModelSerializer):
    """Serializer for FarmCrop cultivation cycles."""

    crop_name = serializers.CharField(source="crop.crop_name", read_only=True)
    scientific_name = serializers.CharField(source="crop.scientific_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    images = FarmImageSerializer(many=True, read_only=True)
    activities = FarmActivitySerializer(many=True, read_only=True)

    class Meta:
        model = FarmCrop
        fields = [
            "id",
            "farm",
            "crop",
            "crop_name",
            "scientific_name",
            "variety",
            "sowing_date",
            "expected_harvest_date",
            "actual_harvest_date",
            "area_allocated",
            "status",
            "status_display",
            "estimated_yield_kg",
            "actual_yield_kg",
            "notes",
            "images",
            "activities",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "farm", "created_at", "updated_at"]


class FarmSerializer(serializers.ModelSerializer):
    """Detailed read serializer for Farm profile including nested summary items."""

    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    owner_name = serializers.CharField(source="owner.full_name", read_only=True, default="")
    unit_display = serializers.CharField(source="get_unit_display", read_only=True)
    water_source_display = serializers.CharField(source="get_water_source_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    active_crop_count = serializers.SerializerMethodField()

    class Meta:
        model = Farm
        fields = [
            "id",
            "owner",
            "owner_email",
            "owner_name",
            "farm_name",
            "farm_image",
            "area",
            "unit",
            "unit_display",
            "latitude",
            "longitude",
            "state",
            "district",
            "village",
            "address",
            "water_source",
            "water_source_display",
            "status",
            "status_display",
            "notes",
            "active_crop_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def get_active_crop_count(self, obj: Farm) -> int:
        if hasattr(obj, "farm_crops"):
            return obj.farm_crops.filter(is_deleted=False).exclude(status=FarmCrop.CropStatus.ARCHIVED).count()
        return 0


class FarmCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Farm profiles."""

    class Meta:
        model = Farm
        fields = [
            "farm_name",
            "farm_image",
            "area",
            "unit",
            "latitude",
            "longitude",
            "state",
            "district",
            "village",
            "address",
            "water_source",
            "status",
            "notes",
        ]
