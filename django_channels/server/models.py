import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validators import validate_image_icon_size


def category_upload_path(instance, filename):
    return f"category_icons/{instance.name}/{filename}"


def channer_banner_upload_path(instance, filename):
    return f"channel_icons/{instance.name}/{filename}"


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    desciption = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_upload_path, blank=True, null=True, validators=[validate_image_icon_size]
    )

    def save(self, *args, **kwargs):
        if self.id:
            EXISTING = get_object_or_404(Category, id=self.id)
            if EXISTING and EXISTING.icon != self.icon:
                os.remove(EXISTING.icon.path)
        super().save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_file(sender, instance, **kwargs):
        if instance.icon:
            os.remove(instance.icon.path)

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    desription = models.CharField(max_length=250, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="server_members")

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100, null=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")
    banner = models.ImageField(
        upload_to=channer_banner_upload_path,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            if existing.banner and existing.banner != self.banner:
                os.remove(existing.banner.path)
        super().save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Channel")
    def channel_delete_file(sender, instance, **kwargs):
        if instance.banner:
            os.remove(instance.banner.path)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "server")
        verbose_name = " Channel"
