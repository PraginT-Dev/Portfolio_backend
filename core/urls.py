from django.urls import path
from .views import (
    FeedbackView,
    SegmentList, CertificateList, ProjectList,
    SkillListView,
)

urlpatterns = [
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('segments/', SegmentList.as_view(), name='segments'),
    path('certificates/', CertificateList.as_view(), name='certificates'),
    path('projects/', ProjectList.as_view(), name='projects'),
    path('skills/', SkillListView.as_view(), name='skills'),  # final route for frontend
]
