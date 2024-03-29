from django.db import models
from harucalendar.models import Harucalendar


# Create your models here

class Diary(models.Model):
    diary_id = models.AutoField(primary_key=True)
    calendar = models.ForeignKey(Harucalendar, related_name='calendar', on_delete=models.CASCADE)
    year_month = models.CharField(max_length=10)  # 2021-08
    day = models.CharField(max_length=30)  # 2021-08-01
    sns_link = models.CharField(max_length=500, blank=True)
    diary_bg_id = models.CharField(max_length=10)
    is_expiry = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class DiaryTextBox(models.Model):
    textbox_id = models.AutoField(primary_key=True)
    diary = models.ForeignKey(Diary, related_name='diaryTextBoxs', on_delete=models.CASCADE)
    writer = models.CharField(max_length=20, blank=True)
    content = models.TextField(blank=True)
    xcoor = models.IntegerField(blank=True,null=True)
    ycoor = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class DiarySticker(models.Model):
    sticker_id = models.AutoField(primary_key=True)
    diary = models.ForeignKey(Diary, related_name="diaryStickers", on_delete=models.CASCADE)
    sticker_image_url = models.CharField(max_length=500)
    top = models.IntegerField(blank=True, null=True)
    left = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    rotate = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class HaruRoom(models.Model):
    room_id = models.AutoField(primary_key=True)
    user_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    diary = models.OneToOneField(Diary, related_name='diary', on_delete=models.CASCADE)



