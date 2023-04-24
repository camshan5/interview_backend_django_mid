from datetime import date
from rest_framework.test import APITestCase
from interview.inventory.models import Inventory


class DeactivateOrderViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an Inventory instance for testing
        cls.inventory = Inventory.objects.create(
            name="Test Item",
            type=InventoryType.objects.create(name="Type A"),
            language=InventoryLanguage.objects.create(name="English"),
            metadata={},
        )
        cls.inventory.tags.add(
            InventoryTag.objects.create(name="Tag A", is_active=True)
        )

        # Create an Order instance for testing
        cls.order = Order.objects.create(
            inventory=cls.inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=True,
        )
