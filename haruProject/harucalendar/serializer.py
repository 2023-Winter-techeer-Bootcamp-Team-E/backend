from .models import Harucalendar, Harucalendarsticker
from rest_framework import serializers


class HarucalendarAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harucalendar
        fields = '__all__'


class HarucalendarstickerAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harucalendarsticker
        fields = '__all__'


class HarucalendarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harucalendar
        fields = ['year_month_day']

    def create(self, validated_data):
        return Harucalendar.objects.create(**validated_data)



class HarucalendarStickerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harucalendarsticker
        fields = ['calendar_id', 'sticker_image_url', 'xcoor', 'ycoor', 'width', 'height', 'rolate']  # 'rolate'가 맞습니다.

    def create(self, validated_data):
        return Harucalendarsticker.objects.create(**validated_data)

