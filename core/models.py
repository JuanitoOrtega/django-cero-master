from django.db import models
from django.conf import settings


# Modelo para auditoría
class BaseModel(models.Model):
  user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation', blank=True, null=True)
  date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_updated', blank=True, null=True)
  date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

  class Meta:
    abstract = True