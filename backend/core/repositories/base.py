"""
Abstract Base Repository Interface (`BaseRepository`).
Enforces the Repository Pattern across all domain modules (`auth`, `farms`, `crop_recommendation`, etc.)
to completely decouple business logic (`Services`) from direct ORM `Model.objects` calls.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from django.db import models
from django.db.models.query import QuerySet
from core.exceptions import ResourceNotFoundError

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T], ABC):
    """
    Abstract base repository providing common CRUD operations over a Django Model class.
    All feature-specific repositories must inherit from this class and set `model_class`.
    """

    @property
    @abstractmethod
    def model_class(self) -> Type[T]:
        """Return the Django Model associated with this repository."""
        pass

    def get_by_id(self, entity_id: Any) -> Optional[T]:
        """Retrieve a single entity instance by its primary key."""
        try:
            return self.model_class.objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def get_by_id_or_raise(self, entity_id: Any) -> T:
        """Retrieve a single entity instance by its primary key, raising ResourceNotFoundError if missing."""
        entity = self.get_by_id(entity_id)
        if not entity:
            raise ResourceNotFoundError(
                f"{self.model_class.__name__} with ID '{entity_id}' not found."
            )
        return entity

    def list_all(self, **filters: Any) -> QuerySet[T]:
        """Retrieve a queryset of entity instances matching optional keyword filters."""
        return self.model_class.objects.filter(**filters)

    def create(self, **data: Any) -> T:
        """Create and persist a new entity instance."""
        instance = self.model_class.objects.create(**data)
        return instance

    def update(self, instance: T, **data: Any) -> T:
        """Update fields on an existing entity instance and save to DB."""
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(data.keys()))
        return instance

    def delete(self, instance: T) -> None:
        """Delete an entity instance from the database."""
        instance.delete()
