from diary import serializers
from rest_framework import serializers


class DiaryTextBoxGetSerializer(serializers.Serializer):
    textbox_id = serializers.IntegerField()
    writer = serializers.CharField()
    content = serializers.CharField()
    xcoor = serializers.IntegerField()
    ycoor = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    rotate = serializers.IntegerField()


class DiaryStickerGetSerializer(serializers.Serializer):
    sticker_id = serializers.IntegerField()
    sticker_image_url = serializers.CharField()
    xcoor = serializers.IntegerField()
    ycoor = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    rotate = serializers.IntegerField()


class DiaryGetRequestSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()


class DiaryGetResponseSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    diary_date = serializers.CharField()
    diary_bg_url = serializers.CharField()
    is_expiry = serializers.BooleanField()
    diaryTextBoxs = DiaryTextBoxGetSerializer(many=True)
    diaryStickers = DiaryStickerGetSerializer(many=True)


class DiaryLinkResponseSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    diary_date = serializers.CharField()
    sns_link = serializers.URLField()


class DiaryLinkGetResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()
    data = DiaryLinkResponseSerializer()