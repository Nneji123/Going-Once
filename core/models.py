from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from customauth.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    bank_code = models.CharField(
        max_length=20, null=True, blank=True
    )  # Add max_length to the field
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Transactions(models.Model):
    pass


class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="item_images/", blank=True)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    number_of_bid = models.IntegerField(default=0)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    is_available = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="won_items", null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["uploaded_at"]


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now=True)

    @property
    def is_winning(self):
        return self.amount == self.item.current_bid

    def save(self, *args, **kwargs):
        item = Item.objects.get(id=self.item.id)
        if not item.is_available:
            raise ValueError("Item is currently not available")
        if self.amount < item.starting_bid:
            raise ValueError("Amount is lower than starting bid")
        if item.current_bid is not None and self.amount <= item.current_bid:
            raise ValueError("Amount is lower than current bid")
        if item.winner == self.bidder:
            raise ValueError("You are already the highest bidder")
        if item.seller == self.bidder:
            raise ValueError("You cannot bid on your own item")
        # Check wallet balance before placing a bid
        bidder_wallet = Wallet.objects.get(user=self.bidder)
        if bidder_wallet.balance < item.starting_bid or (
            item.current_bid is not None and bidder_wallet.balance < self.amount
        ):
            raise ValidationError("Insufficient balance to place bid")
        item.winner = None
        item.current_bid = self.amount
        item.number_of_bid += 1
        item.winner = self.bidder
        item.save()
        if (
            not item.is_available
            and item.winner is not None
            and timezone.now() > item.end_date
        ):
            winner_wallet = Wallet.objects.get(user=self.bidder)
            winner_wallet.balance -= self.amount
            winner_wallet.save()
            # Transfer amount to seller's wallet balance
            seller_wallet = Wallet.objects.get(user=item.seller)
            seller_wallet.balance += self.amount
            seller_wallet.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bidder.username}'s Bid"
