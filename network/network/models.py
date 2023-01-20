from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class FOLLOWERS(models.Model):
    user= models.ForeignKey("User", on_delete=models.CASCADE, related_name="follows")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    
    def __str__(self):
        return f"{self.user} follows {self.following}"

class POSTS (models.Model):
    user= models.ForeignKey("User", on_delete=models.CASCADE, related_name="posted")
    timestamp = models.DateTimeField(auto_now_add=True)
    content= models.TextField(blank=True)
    like= models.ManyToManyField(User, blank=True, related_name="liked")

    def __str__(self):
        return f"{self.user} posted at {self.timestamp}"

    def post_comments(self):
        return COMMENT_SECTION.objects.get(post = self)
        

class COMMENT_SECTION(models.Model):
    comment_content = models.CharField(max_length = 1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    post = models.ForeignKey(POSTS, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.origin} has commented on {self.post}"