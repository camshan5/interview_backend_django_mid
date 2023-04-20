from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)


class InventoryAfterDateListCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory_language = InventoryLanguage.objects.create(name="English")
        cls.inventory_type = InventoryType.objects.create(name="Type A")
        cls.inventory_tag = InventoryTag.objects.create(name="Tag A", is_active=True)

        cls.inventory1 = Inventory.objects.create(
            name="Item 1",
            type=cls.inventory_type,
            language=cls.inventory_language,
            metadata={},
        )
        cls.inventory1.tags.add(cls.inventory_tag)
        cls.inventory1.created_at = timezone.now() - timedelta(days=5)
        cls.inventory1.save()

        cls.inventory2 = Inventory.objects.create(
            name="Item 2",
            type=cls.inventory_type,
            language=cls.inventory_language,
            metadata={},
        )
        cls.inventory2.tags.add(cls.inventory_tag)
        cls.inventory2.created_at = timezone.now() - timedelta(days=1)
        cls.inventory2.save()

    def test_inventory_created_after_filter(self):
        url = reverse("inventory-created-after") + "?date={}".format(
            (timezone.now() - timedelta(days=3)).date()
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.inventory2.id)
