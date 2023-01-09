from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class CATALOG(models.Model):
    category = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.category}"

class AUCTION_LISTINGS(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(CATALOG, on_delete=models.PROTECT, blank=True, related_name="catalog")
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.URLField(blank=True)
    current_price = models.FloatField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    status = models.BooleanField(default = True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watched")

    def __str__(self):
        return f"{self.id} {self.owner}: {self.title}"

class BIDS(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_by")
    amount = models.FloatField()
    bid_item = models.ForeignKey(AUCTION_LISTINGS, on_delete=models.CASCADE, related_name="past_bids")

    def __str__(self):
        return f"{self.bidder} bidded {self.bid_item} for {self.amount}"

class COMMENT_SECTION(models.Model):
    comment_content = models.CharField(max_length = 1000)
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    post = models.ManyToManyField(AUCTION_LISTINGS, blank=True, related_name="comments")

    def __str__(self):
        return f"{self.origin} has commented on {self.post}"
