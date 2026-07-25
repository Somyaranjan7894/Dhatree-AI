"""
Abstract Base Service Interface (`BaseService`).
Enforces the Service Layer Pattern: all domain logic, transaction boundaries, orchestration, and validation
must reside in Service classes rather than inside Django DRF API views or Serializers.
"""
import logging
from abc import ABC
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base service providing structured logging, orchestration utilities, and invariant verification.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__module__)

    def log_operation(
        self, operation_name: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log a business operation execution with structured context."""
        payload = context or {}
        self.logger.info(f"Executing Business Operation [{operation_name}] | {payload}")
