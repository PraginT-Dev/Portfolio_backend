from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from decouple import config
import requests
import logging

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)

# ✅ Email Sending via Brevo API
def send_email_via_brevo(to_email, subject, html_content):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": config("BREVO_API_KEY"),
        "content-type": "application/json"
    }
    data = {
        "sender": {
            "name": "Portfolio Contact",
            "email": config("EMAIL_HOST_USER")  # Must match verified Brevo sender
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()

# 💬 Handle Feedback + Send Email
class FeedbackView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message_text = serializer.validated_data.get('message', '')

            subject = "Thanks for connecting with me!"
            html_content = f"""
            <p>Yo <strong>{name}</strong> 😄,</p>
            <p>Thanks for reaching out — your message just made my inbox 10x cooler!</p>
            <p>I’ve read your note, smiled a little, and nodded like a wise old owl 🦉.</p>
            <p><strong>Your Message:</strong><br>{message_text}</p>
            <p>Thanks, legend! Your message made my day—and possibly increased my dopamine by 5% 📈😂<br>
            Let’s keep the bytes flowing and the bugs crashing!</p>
            <p>Catch ya in the debug zone!<br>— Pragin T. 🐞💥</p>

            """

            try:
                status_code, result = send_email_via_brevo(email, subject, html_content)
                if status_code == 201:
                    logger.info(f"Feedback email sent to {email}")
                    return Response({"status": "feedback received and email sent"})
                else:
                    logger.error(f"Brevo error: {result}")
                    return Response({"error": result}, status=500)

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
