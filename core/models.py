from django.db import models

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
    image = models.ImageField(upload_to='skills/')
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='skills')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    title = models.CharField(max_length=200)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='certificates')
    description = models.TextField()
    image = models.ImageField(upload_to='certificates/')
    verify_link = models.URLField(blank=True, null=True) 
    skills = models.ManyToManyField(Skill, blank=True, related_name='certificates')  # ✅ Link multiple skills
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]  # Limit title length for better readability



# 📷 Project and images
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)        # ✅ already present
    live_preview_link = models.URLField(blank=True, null=True)  # ✅ new field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"
