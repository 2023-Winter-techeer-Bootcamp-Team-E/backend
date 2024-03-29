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


class DiaryStickerGetSerializer(serializers.Serializer):
    sticker_id = serializers.IntegerField()
    sticker_image_url = serializers.CharField()
    top = serializers.IntegerField()
    left = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    rotate = serializers.IntegerField()


class SwaggerDiaryCreateRequestSerializer(serializers.Serializer):
    day = serializers.CharField()
    diary_bg_id = serializers.IntegerField()


class SwaggerDiaryCreateResponseSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()


class DiaryGetResponseSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    day = serializers.IntegerField()
    diary_bg_id = serializers.CharField()
    login_id = serializers.CharField()
    is_expiry = serializers.BooleanField()
    diaryTextBoxs = DiaryTextBoxGetSerializer(many=True)
    diaryStickers = DiaryStickerGetSerializer(many=True)


class DiaryGetRequestSerializer(serializers.Serializer):
    diary_id = serializers.CharField(required=True)


class DiaryLinkRequestSerializer(serializers.Serializer):
    day = serializers.CharField(required=True)


class DiaryLinkResponseSerializer(serializers.Serializer):
    diary_id = serializers.IntegerField()
    day = serializers.IntegerField()
    sns_link = serializers.URLField()
    nickname = serializers.CharField()


class DiaryLinkGetResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()
    data = DiaryLinkResponseSerializer()


class DiaryTextBoxPostRequestSerializer(serializers.Serializer):
    content = serializers.CharField()
    diary_id = serializers.IntegerField()


class DiaryTextBoxPostResponseSerializer(serializers.Serializer):
    textbox_id = serializers.IntegerField()


class TextBoxPutRequestSerializer(serializers.Serializer):
    textbox_id = serializers.IntegerField()
    writer = serializers.CharField()
    content = serializers.CharField()
    xcoor = serializers.IntegerField()
    ycoor = serializers.IntegerField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()


class StickerPutRequestSerializer(serializers.Serializer):
    sticker_id = serializers.IntegerField()
    sticker_image_url = serializers.URLField()
    top = serializers.IntegerField()
    left = serializers.IntegerField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()
    rotate = serializers.IntegerField()


class DiaryTextBoxAndStickerPutRequestSerializer(serializers.Serializer):
    textboxs = TextBoxPutRequestSerializer(many=True)
    stickers = StickerPutRequestSerializer(many=True)


class DiarySaveRequestSerializer(serializers.Serializer):
    saved_data = DiaryTextBoxAndStickerPutRequestSerializer()


class DiaryTextBoxPutResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()


class DiaryStickerRequestSerializer(serializers.Serializer):
    content = serializers.CharField()


class DiaryStickerGetResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))

