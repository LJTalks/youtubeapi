from django.shortcuts import render
from django.http import HttpResponse
from django.db import models


# Create your views here.
# View to Store Channel IDs in the Database
class Channel(models.Model):
    channel_id = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional if you have users

    def __str__(self):
        return self.channel_name or self.channel_id
