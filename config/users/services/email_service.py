from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging



logger = logging.getLogger(__name__)

class EmailService:

    @staticmethod
    def send_welcome_email(user):

        subject = f'Welcome to FitTrack!, {user.username}'
        message = f'Hi {user.username}, Welcome to FitTrack! Your Role is {user.role}'
        try:

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            return False

    @staticmethod
    def send_coach_application_status(user,approved=True):
        try:
            status = 'approved' if approved else 'rejected'
            subject = f"Your Coach application has been {status.title()}"

            html_message = render_to_string('email/application_status.html', {
                'username': user.username,
                'approved': approved,
                'dashboard_url': f"{settings.SITE_URL}/{'coach' if approved else 'trainee'}/dashboard",
            })

            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
            )
            return True

        except Exception as e:
            logger.error(f"Failed to send application status email to {user.email}: {str(e)}")
            return False


