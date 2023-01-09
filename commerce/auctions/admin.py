from django.contrib import admin
from .models import User, CATALOG, AUCTION_LISTINGS, BIDS

admin.site.register(User)
admin.site.register(CATALOG)
admin.site.register(AUCTION_LISTINGS)
admin.site.register(BIDS)
# Register your models here.
