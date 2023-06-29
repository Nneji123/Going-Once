from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Bid, Item, Wallet


# Bid Serializers
class BidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ("item", "amount")

    def validate_amount(self, value):
        item_id = self.initial_data["item"]
        item = get_object_or_404(Item, id=item_id)
        if not item.is_available:
            raise serializers.ValidationError("Item is currently not available")
        if value < item.starting_bid:
            raise serializers.ValidationError("Amount is lower than starting bid")
        if item.current_bid is not None and value <= item.current_bid:
            raise serializers.ValidationError("Amount is lower than current bid")
        if item.winner is not None and item.winner == self.context["request"].user:
            raise serializers.ValidationError(
                "You cannot bid on an item you're currently winning"
            )
        return value

    def validate(self, data):
        item = get_object_or_404(Item, id=data["item"].id)
        if item.seller == self.context["request"].user:
            raise serializers.ValidationError("Seller cannot bid on their own item")

        # Check wallet balance before placing a bid
        bidder_wallet = Wallet.objects.get(user=self.context["request"].user)
        if bidder_wallet.balance < item.starting_bid or (
            item.current_bid is not None and bidder_wallet.balance < data["amount"]
        ):
            raise serializers.ValidationError("Insufficient balance to place bid")
        return data

    def create(self, validated_data):
        try:
            bidder = self.context["request"].user
            bid = Bid.objects.create(bidder=bidder, **validated_data)
            return bid
        except ValidationError as e:
            raise serializers.ValidationError({"detail": e.detail})


# Item Serializers
class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "name",
            "image",
            "description",
            "starting_bid",
            "end_date",
        )

    def create(self, validated_data):
        try:
            seller = self.context["request"].user
            validated_data.pop(
                "seller", None
            )  # remove seller field from validated_data
            item = Item.objects.create(seller=seller, **validated_data)
            return item
        except ValidationError as e:
            raise serializers.ValidationError({"detail": e.detail})


class ItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "name",
            "image",
            "description",
            "starting_bid",
            "end_date",
        )

    def create(self, validated_data):
        try:
            seller = self.context["request"].user
            validated_data.pop(
                "seller", None
            )  # remove seller field from validated_data
            item = Item.objects.create(seller=seller, **validated_data)
            return item
        except ValidationError as e:
            raise serializers.ValidationError({"detail": e.detail})


class ItemDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class WalletUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("balance", "account_number", "bank_code")

    def create(self, validated_data):
        try:
            user = self.context["request"].user
            validated_data.pop("user", None)
            balance = Wallet.objects.create(user=user, **validated_data)
            return balance
        except ValidationError as e:
            raise serializers.ValidationError({"detail": e.detail})
