from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Bid, Item

from .factories import BidFactory, ItemFactory, UserFactory


class ItemModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.item = ItemFactory(seller=self.user)

    def test_item_name(self):
        self.assertEqual(str(self.item), self.item.name)

    def test_item_starting_bid(self):
        self.assertEqual(self.item.starting_bid, Decimal("10.00"))

    def test_item_current_bid_default(self):
        self.assertIsNone(self.item.current_bid)

    def test_item_number_of_bid_default(self):
        self.assertEqual(self.item.number_of_bid, 0)

    def test_item_end_date(self):
        self.assertTrue(isinstance(self.item.end_date, datetime))

    def test_item_is_available_default(self):
        self.assertTrue(self.item.is_available)

    def test_item_uploaded_at(self):
        self.assertTrue(isinstance(self.item.uploaded_at, datetime))

    def test_item_seller(self):
        self.assertEqual(self.item.seller, self.user)

    def test_item_winner_default(self):
        self.assertIsNone(self.item.winner)


class BidModelTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.item = ItemFactory(starting_bid=Decimal("10.00"))
        self.bid = BidFactory(item=self.item, bidder=self.user1, amount=Decimal("12.00"))

    def test_bid_is_winning(self):
        self.assertFalse(self.bid.is_winning)

    def test_bid_save_with_item_unavailable(self):
        self.item.is_available = False
        self.item.save()
        with self.assertRaises(ValueError):
            BidFactory(item=self.item, bidder=self.user2, amount=Decimal("14.00"))

    def test_bid_save_with_amount_lower_than_starting_bid(self):
        with self.assertRaises(ValueError):
            BidFactory(item=self.item, bidder=self.user2, amount=Decimal("8.00"))

    def test_bid_save_with_amount_lower_than_current_bid(self):
        with self.assertRaises(ValueError):
            BidFactory(item=self.item, bidder=self.user2, amount=Decimal("11.00"))

    def test_bid_save_with_bidder_as_seller(self):
        with self.assertRaises(ValueError):
            BidFactory(item=self.item, bidder=self.user1, amount=Decimal("14.00"))

    def test_bid_save_with_bidder_as_winner(self):
        self.bid.amount = Decimal("14.00")
        self.bid.save()
        with self.assertRaises(ValueError):
            BidFactory(item=self.item, bidder=self.user1, amount=Decimal("16.00"))

    def test_bid_save_updates_item_current_bid(self):
        BidFactory(item=self.item, bidder=self.user2, amount=Decimal("14.00"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.current_bid, Decimal("14.00"))

    def test_bid_save_updates_item_number_of_bid(self):
        BidFactory(item=self.item, bidder=self.user2, amount=Decimal("14.00"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.number_of_bid, 2)

    def test_bid_save_updates_item_winner(self):
        BidFactory(item=self.item, bidder=self.user2, amount=Decimal("14.00"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.winner, self.user2)