from django.contrib import admin
from .models import (
    Feedback, Segment, Certificate,
    Project, ProjectImage, Skill
)

class ProjectImageInline(admin.TabularInline):  # or StackedInline
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'created_at')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback)
admin.site.register(Segment)
admin.site.register(Certificate)
admin.site.register(Skill)


