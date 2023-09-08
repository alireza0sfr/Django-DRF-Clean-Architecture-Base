import pytest
from django.utils import timezone
from datetime import datetime
from uuid import UUID, uuid4

from application.dtos.base import BaseDto
from tests.base import BaseTest

class TestBaseDto(BaseTest):

    @pytest.mark.unit
    def test_attrs(self):
        # Arrange
        dto = BaseDto(
            id=uuid4(),
            created_date=timezone.now(),
            updated_date=timezone.now()
    )

        # Act

        # Assert
        assert isinstance(dto.id, UUID)
        assert isinstance(dto.created_date, datetime)
        assert isinstance(dto.updated_date, datetime)
