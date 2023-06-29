from datetime import datetime, timedelta, timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core.models import Bid, Item
from core.serializers import (BidCreateSerializer, BidListSerializer,
                              ItemCreateSerializer, ItemDestroySerializer,
                              ItemListSerializer, ItemRetrieveSerializer,
                              ItemUpdateSerializer)

User = get_user_model()


# Test retrieving a list of bids
class TestBidList(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="testpass123"
        )
        self.item = Item.objects.create(
            seller=self.user1,
            name="Test Item",
            starting_bid=Decimal("10.00"),
            end_date=datetime.now() + timezone.timedelta(days=7),
            is_available=True,
        )

        # Create some bids
        Bid.objects.create(bidder=self.user1, item=self.item, amount=Decimal("10.00"))
        Bid.objects.create(bidder=self.user2, item=self.item, amount=Decimal("12.00"))
        Bid.objects.create(bidder=self.user1, item=self.item, amount=Decimal("15.00"))

    def test_get_bid_list(self):
        url = reverse("bid-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bids = Bid.objects.all()
        serializer = BidListSerializer(bids, many=True)
        self.assertEqual(response.data, serializer.data)
        for bid, data in zip(bids, serializer.data):
            self.assertEqual(str(bid.id), data["id"])
            self.assertEqual(bid.bidder.username, data["bidder"]["username"])
            self.assertEqual(bid.item.id, data["item"])
            self.assertEqual(str(bid.amount), data["amount"])
            self.assertEqual(str(bid.created_at.isoformat()), data["created_at"])