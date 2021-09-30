from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta(object):
        abstract = True
