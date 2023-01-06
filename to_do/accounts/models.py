from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Profile(models.Model):
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name="Avatar")
    git_profile = models.CharField(max_length=200, null=True, blank=True, verbose_name="Git link")
    about = models.CharField(max_length=1000, null=True, blank=True, verbose_name="About")
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name="User",
                                related_name="profile")

    def __str__(self):
        return f"{self.id}. {self.user}: {self.git_profile}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
