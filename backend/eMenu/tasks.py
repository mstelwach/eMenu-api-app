from celery import shared_task
from django.core.management import call_command


@shared_task
def send_emails_report():
    call_command("email_report", )
