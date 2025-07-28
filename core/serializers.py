from rest_framework import serializers
from .models import (
    Feedback, Segment, Certificate, Project, ProjectImage, Skill
)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = '__all__'


# 🔁 Skill Serializer (used below as well)
class SkillSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['name', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ''


# ✅ Updated Certificate Serializer with skills
class CertificateSerializer(serializers.ModelSerializer):
    segment = serializers.CharField(source='segment.name')  # Show segment name instead of ID
    skills = SkillSerializer(many=True, read_only=True)     # Nested skills list
    image = serializers.SerializerMethodField()             # Add this line

    class Meta:
        model = Certificate
        fields = ['id', 'title', 'description', 'image', 'verify_link', 'created_at', 'segment', 'skills']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ''


class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return ''


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


# 📦 Segments with grouped skills
class SegmentWithSkillsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Segment
        fields = ['name', 'description', 'skills']
