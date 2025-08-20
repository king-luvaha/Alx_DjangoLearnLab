from django.contrib.auth.models import AbstractUser
from django.db import models


def profile_picture_upload_to(instance, filename):
    return f"profile_pics/user_{instance.id}/{filename}"


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, blank=True, null=True)


    # "followers" = people who follow this user
    # related_name="following" lets you do: user.following.all() to see who the user follows
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def followers_count(self) -> int:
        return self.followers.count()

    def following_count(self) -> int:
        return self.following.count()

    def __str__(self):
        return self.username