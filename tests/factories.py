from decimal import Decimal

import factory
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Bid, Item


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker('word')
    image = factory.django.ImageField()
    description = factory.Faker('text')
    starting_bid = Decimal('10.00')
    current_bid = None
    number_of_bid = 0
    end_date = timezone.now() + timezone.timedelta(days=7)
    seller = factory.SubFactory(UserFactory)
    is_available = True
    winner = None

class BidFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bid

    bidder = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)
    amount = Decimal('15.00')
