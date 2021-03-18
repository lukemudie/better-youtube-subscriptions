from django.db import models

# Create your models here.
class ChannelId(models.Model):
    channel_id = models.CharField(max_length=200)