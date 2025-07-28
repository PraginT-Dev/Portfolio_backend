from django.db import models
from cloudinary.models import CloudinaryField  # ✅ Cloudinary import

# 🎯 Feedback model
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# 📁 Segment (Skill grouping)
class Segment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 🧠 Skill under a segment
class Skill(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')  # ✅ Replaced with Cloudinary
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='skills')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    title = models.CharField(max_length=200)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='certificates')
    description = models.TextField()
    image = CloudinaryField('image')  # ✅ Replaced with Cloudinary
    verify_link = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='certificates')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]


# 📷 Project and images
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)
    live_preview_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')  # ✅ Replaced with Cloudinary

    def __str__(self):
        return f"Image for {self.project.title}"
