from django.db import models
from member.models import Member


class StaticImage(models.Model):
    st_image_id = models.AutoField(primary_key=True)
    st_image_url = models.CharField(max_length=500)