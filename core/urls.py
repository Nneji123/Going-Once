from django.urls import path

from .views import (
    BidCreateView,
    BidListAllView,
    BidListView,
    BidUserItemListView,
    ItemListAllView,
    ItemListCreateView,
    ItemRetrieveUpdateDestroyView,
    ItemSearchView,
    WalletUpdateView,
    WalletView,
)

urlpatterns = [
    path("items/all/", ItemListAllView.as_view(), name="items_list_all"),
    path("items/", ItemListCreateView.as_view(), name="item_list_create"),
    path(
        "items/<int:pk>/",
        ItemRetrieveUpdateDestroyView.as_view(),
        name="item_retrieve_update_destroy",
    ),
    path("items/search/", ItemSearchView.as_view(), name="item_search"),
    path("bids/user/", BidListAllView.as_view(), name="bid_list_all_user"),
    path("bids/<int:id>", BidListView.as_view(), name="bid_list"),
    path("bids/create/", BidCreateView.as_view(), name="bid_create"),
    path(
        "bids/item/<int:item_id>/",
        BidUserItemListView.as_view(),
        name="bid_user_item_list",
    ),
    path("wallet/", WalletView.as_view(), name="wallet_balance"),
    path("wallet/update/", WalletUpdateView.as_view(), name="update_wallet"),
]
