from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

# 💬 Handle Feedback + Send Email
class FeedbackView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message_text = serializer.validated_data.get('message', '')

            # Prepare the email
            subject = "Thanks for your feedback!"
            message = f"""
Hi {name},

Thanks for taking the time to give your feedback.
I truly appreciate your support!

Your Message:
{message_text}

— Pragin T.
"""

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  # from_email
                    [email],                      # to_email
                    fail_silently=False,
                )
                logger.info(f"Feedback email sent to {email}")
                return Response({"status": "feedback received and email sent"})

            except BadHeaderError:
                logger.error("Invalid header found when sending email.")
                return Response({"error": "Invalid header."}, status=400)
            except Exception as e:
                logger.exception("Email sending failed.")
                return Response({"error": str(e)}, status=500)

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
