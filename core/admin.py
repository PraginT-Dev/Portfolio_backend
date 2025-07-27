from django.contrib import admin
from .models import (
    Feedback,
    Segment,
    Certificate,
    Project,
    ProjectImage,
    Skill
)

# Inline display of related ProjectImage objects in ProjectAdmin
class ProjectImageInline(admin.TabularInline):  # You can also use StackedInline
    model = ProjectImage
    extra = 1  # Number of empty image fields shown by default

# Custom admin for Project with image inlines
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'created_at')  # Show title and creation date in admin list

# Register all models in the Django admin panel
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage)
admin.site.register(Feedback)
admin.site.register(Segment)
admin.site.register(Certificate)
admin.site.register(Skill)
