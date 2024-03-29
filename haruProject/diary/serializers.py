from rest_framework import serializers

from .models import Diary, DiaryTextBox, DiarySticker, HaruRoom


class DiaryTextBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryTextBox
        fields = ['textbox_id', 'writer', 'content', 'xcoor', 'ycoor', 'width', 'height']


class DiaryStickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarySticker
        fields = ['sticker_id', 'sticker_image_url', 'top', 'left', 'width', 'height', 'rotate']


class DiaryStickerModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarySticker
        fields = ['sticker_image_url', 'top', 'left', 'width', 'height', 'rotate']

    def create(self, validated_data):
        return DiarySticker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sticker_image_url = validated_data.get('sticker_image_url', instance.sticker_image_url)
        instance.top = validated_data.get('top', instance.top)
        instance.left = validated_data.get('left', instance.left)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.rotate = validated_data.get('rotate', instance.rotate)
        instance.save()
        return instance


class DiaryTextBoxModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryTextBox
        fields = ['content', 'writer', 'xcoor', 'ycoor', 'width', 'height']

    def create(self, validated_data):
        return DiaryTextBox.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.writer = validated_data.get('writer', instance.writer)
        instance.xcoor = validated_data.get('xcoor', instance.xcoor)
        instance.ycoor = validated_data.get('ycoor', instance.ycoor)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance


class DiaryDetailSerializer(serializers.ModelSerializer):
    diaryTextBoxs = DiaryTextBoxSerializer(many=True, read_only=True)
    diaryStickers = DiaryStickerSerializer(many=True, read_only=True)

    class Meta:
        model = Diary
        fields = ['diary_id', 'year_month', 'diary_bg_id', 'is_expiry', 'diaryTextBoxs', 'diaryStickers']


class HaruRoomDetailSerializer(serializers.ModelSerializer):
    diaryTextBoxs = DiaryTextBoxSerializer(many=True, read_only=True)
    diaryStickers = DiaryStickerSerializer(many=True, read_only=True)

    class Meta:
        model = Diary
        fields = ['diaryTextBoxs', 'diaryStickers']


class DiarySnsLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['diary_id', 'day', 'sns_link']


class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['diary_bg_id', 'day', 'year_month']

    def create(self, validated_data):
        return Diary.objects.create(**validated_data)


class DiaryTextBoxCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryTextBox
        fields = ['writer', 'content', 'xcoor', 'ycoor', 'width', 'height', 'rotate']

    def create(self, validated_data):
        return DiaryTextBox.objects.create(**validated_data)


class DiaryStickerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarySticker
        fields = ['top', 'left', 'width', 'height', 'rotate']

    def update(self, instance, validated_data):
        print(validated_data)
        instance.top = validated_data.get('top', instance.top)
        instance.left = validated_data.get('left', instance.left)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.rotate = validated_data.get('rotate', instance.rotate)
        instance.save()
        print(instance.top, instance.left, instance.width, instance.height, instance.rotate)
        return instance


class DiaryTextBoxUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryTextBox
        fields = ['writer', 'content', 'xcoor', 'ycoor', 'width', 'height']

    def update(self, instance, validated_data):
        instance.writer = validated_data.get('writer', instance.writer)
        instance.content = validated_data.get('content', instance.content)
        instance.xcoor = validated_data.get('xcoor', instance.xcoor)
        instance.ycoor = validated_data.get('ycoor', instance.ycoor)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance


class DiaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['sns_link']

    def update(self, instance, validated_data):
        instance.sns_link = validated_data.get('sns_link', instance.sns_link)
        instance.save()
        return instance




