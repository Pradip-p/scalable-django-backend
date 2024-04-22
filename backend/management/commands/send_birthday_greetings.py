import logging
from django.core.management.base import BaseCommand
from datetime import datetime
from backend.models import User
from django.core.mail import send_mail
from smtplib import SMTPException
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send birthday greetings to users'

    def handle(self, *args, **kwargs):
        try:
            load_dotenv()  # Load environment variables from .env file

            today = datetime.now().date()
            # Get customers whose birthday is today
            users = User.objects.filter(birth_date__day=today.day, birth_date__month=today.month)
            logger.info(f"Found {len(users)} users with birthdays today.")

            for user in users:
                # Send birthday greetings
                subject = '🎉 Happy Birthday! 🎉'
                message = f"✨ Happy Birthday, {user.full_name}! ✨\n\nhopes your next year is filled with success, surprises, and excitement. Time to celebrate! 🥳"
                try:
                    # Send email using environment variables
                    send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), [user.email])
                    logger.info(f"Sent birthday greetings to {user.username} ({user.email}).")
                except SMTPException as smtp_error:
                    logger.error(f"SMTP error occurred while sending birthday greetings to {user.username} ({user.email}): {smtp_error}")
                except Exception as e:
                    logger.error(f"Failed to send birthday greetings to {user.username} ({user.email}): {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
