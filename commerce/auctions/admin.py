from django.contrib import admin
from .models import User, CATALOG, AUCTION_LISTINGS, BIDS, COMMENT_SECTION

admin.site.register(User)
admin.site.register(CATALOG)
admin.site.register(AUCTION_LISTINGS)
admin.site.register(BIDS)
admin.site.register(COMMENT_SECTION)
# Register your models here.
