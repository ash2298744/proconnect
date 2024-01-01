from django.db import models

# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length = 100)
    uid = models.CharField(max_length = 100)
    room_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name