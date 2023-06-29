from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bid, Item, Wallet
from .serializers import (
    BidCreateSerializer,
    BidListSerializer,
    ItemCreateSerializer,
    ItemDestroySerializer,
    ItemListSerializer,
    ItemRetrieveSerializer,
    ItemUpdateSerializer,
    WalletSerializer,
    WalletUpdateSerializer,
)


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the item.
        return obj.seller == request.user


class IsBidderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the item.
        return obj.bidder == request.user


class ItemListAllView(generics.ListAPIView):
    """
    A view that returns a list of all available items posted by all users in the system.

    GET: Return a list of all available items posted by all users.
    """

    queryset = Item.objects.all()
    permission_classes = [IsSellerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ItemListSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    """
    A view that returns a list of all items posted by the logged-in user, and allows
    authenticated users to create a new item.

    GET request:
    Returns a list of all items posted by the logged-in user.

    POST request:
    Creates a new item with the data provided in the request body.
    """

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            """List all items posted by a user"""
            return ItemListSerializer
        if self.request.method == "POST":
            return ItemCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the item
        self.perform_create(serializer)

        # Custom response
        response_data = {
            "status": "success",
            "message": "Item created successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view that allows a logged-in user to retrieve, update or delete their own items.

    GET request:
    Retrieves details of a single item.

    PUT or PATCH request:
    Updates the details of a single item.

    DELETE request:
    Deletes a single item.
    """

    permission_classes = [IsSellerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ItemRetrieveSerializer
        if self.request.method == "PUT":
            return ItemUpdateSerializer
        if self.request.method == "PATCH":
            return ItemUpdateSerializer
        if self.request.method == "DELETE":
            return ItemDestroySerializer

    def perform_update(self, serializer):
        instance = serializer.save(seller=self.request.user)
        instance.save()


class ItemSearchView(generics.ListAPIView):
    """Get all items based on query parameters."""

    serializer_class = ItemListSerializer

    def get_queryset(self):
        queryset = Item.objects.all()

        # Get query parameters from request
        query = self.request.query_params.get("q", "")
        current_bid = self.request.query_params.get("current_bid")
        starting_bid = self.request.query_params.get("starting_bid")
        number_of_bid = self.request.query_params.get("number_of_bid")
        end_date = self.request.query_params.get("end_date")
        uploaded_at = self.request.query_params.get("uploaded_at")

        # Filter queryset based on query parameters
        if query:
            queryset = queryset.filter(name__icontains=query)

        if current_bid:
            queryset = queryset.filter(current_bid=current_bid)

        if starting_bid:
            queryset = queryset.filter(starting_bid=starting_bid)

        if number_of_bid:
            queryset = queryset.filter(number_of_bid=number_of_bid)

        if end_date:
            queryset = queryset.filter(end_date=end_date)

        if uploaded_at:
            queryset = queryset.filter(uploaded_at=uploaded_at)

        return queryset


class BidListAllView(generics.ListAPIView):
    """
    A view that returns a list of all bids made by the logged-in user.

    GET request:
    Returns a list of all bids made by the logged-in user.
    """

    permission_classes = [IsBidderOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(bidder=self.request.user)

    serializer_class = BidListSerializer


class BidListView(generics.ListAPIView):

    """
    A view that returns a list of all bids made by all users for a particular item.

    GET request:
    Returns a list of all bids made by all users for a particular item.

    """

    def get_queryset(self):
        id = self.kwargs["id"]
        return Bid.objects.filter(item__id=id)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BidListSerializer


class BidUserItemListView(generics.ListAPIView):
    """
    A view that returns a list of all bids made by the logged-in user for a particular item.

    GET request:
    Returns a list of all bids made by the logged-in user for a particular item.
    """

    serializer_class = BidListSerializer
    permission_classes = [IsBidderOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        item_id = self.kwargs["item_id"]
        return Bid.objects.filter(bidder=self.request.user, item=item_id)


class BidCreateView(generics.CreateAPIView):
    """
    A view that allows authenticated users to make a new bid on an item.

    POST request:
    Creates a new bid with the data provided in the request body.
    """

    serializer_class = BidCreateSerializer
    permission_classes = [IsBidderOrReadOnly, permissions.IsAuthenticated]


class WalletView(APIView):
    """
    Get current user's wallet balance
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        try:
            wallet = Wallet.objects.get(user=user)
            wallet_balance = wallet.balance
        except Wallet.DoesNotExist:
            # If wallet does not exist, create a new wallet with balance 0 for the user
            wallet = Wallet(user=user, balance=0.00)
            wallet.save()
            wallet_balance = 0.00
        data = {
            "user": user.id,
            "username": user.username,
            "wallet_balance": wallet_balance,
        }
        return Response(data)


class WalletUpdateView(generics.UpdateAPIView):
    """
    Update current logged in user's balance
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WalletUpdateSerializer
    queryset = Wallet.objects.all()

    def get_object(self):
        # Return the queryset filtered by the currently logged in user
        return self.queryset.get(user=self.request.user)

    def perform_update(self, serializer):
        funded_amount = self.request.data.get("balance")
        if funded_amount is not None:
            wallet = self.get_object()
            wallet.balance += Decimal(funded_amount)
            wallet.save()
            serializer.instance = wallet
            return Response(serializer.data)
        else:
            return JsonResponse({"status": "error", "message": "Amount not provided"})
