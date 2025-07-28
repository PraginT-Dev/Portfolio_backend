from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from decouple import config
import requests
import logging
from django.http import JsonResponse

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
            <p>Hey <strong>{name}</strong> 👋,</p>
            <p>Your message has safely landed in my inbox (with a soft ‘thud’ and zero error codes—success! ✅).</p>
            <p>I gave it a read, smiled like a human (because I totally am one 🤖), and made a mental note that you're awesome.</p>
            <p><strong>Your Message:</strong><br>{message_text}</p>
            <p>He’s currently busy wrangling pixels or debugging the matrix, but expect a proper reply from him soon! 🤓</p>
            <p>Until then, stay cool and keep the vibes high!<br>— Pragin's Boty 🤖 </p>
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


# 🩺 Health check endpoint for uptime/ping monitoring
def health_check(request):
    return JsonResponse({"status": "ok"})
