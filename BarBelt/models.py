from django.db import models
import json

class User(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.JSONField()  # Storing the face encoding as a list

    def __str__(self):
        return self.name