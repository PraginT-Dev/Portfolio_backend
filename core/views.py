from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import *
from .serializers import *

# 💬 Handle Feedback + Send Email
class FeedbackView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.validated_data['name']
            email = serializer.validated_data['email']

            # Send confirmation email
            subject = "Thanks for your feedback!"
            message = f"""
Hi {name},

Thanks for taking the time to give your feedback.
I truly appreciate your support!

— Pragin T.
"""
            send_mail(subject, message, None, [email], fail_silently=False)
            return Response({"status": "feedback received and email sent"})

        return Response(serializer.errors, status=400)


# 📄 Public Read APIs
class SegmentList(generics.ListAPIView):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer

class CertificateList(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# 🔄 Grouped Skills by Segment
class SkillListView(APIView):
    def get(self, request):
        segments = Segment.objects.prefetch_related('skills').all()
        serializer = SegmentWithSkillsSerializer(segments, many=True, context={'request': request})
        return Response(serializer.data)
