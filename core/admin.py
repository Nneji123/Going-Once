from django.contrib import admin

from .models import Bid, Item, Wallet


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "description",
        "starting_bid",
        "current_bid",
        "number_of_bid",
        "end_date",
        "seller",
        "is_available",
        "uploaded_at",
        "winner",
    )


class BidAdmin(admin.ModelAdmin):
    list_display = ("bidder", "item", "amount", "created")


class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "account_number", "bank_code", "balance")


admin.site.register(Item, ItemAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Wallet, WalletAdmin)
