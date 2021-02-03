from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from backend.settings import EMAIL_HOST_USER
from eMenu.models import Dish


class Command(BaseCommand):
    help = "Send Yesterday's Dishes Report to Other Users"

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)

        dishes_created_yesterday = Dish.objects.filter(created__date=yesterday)
        dishes_updated_yesterday = Dish.objects.filter(updated__date=yesterday)

        html_context = {}
        if dishes_created_yesterday:
            html_context['dishes_created'] = dishes_created_yesterday
        if dishes_updated_yesterday:
            html_context['dishes_updated'] = dishes_updated_yesterday

        subject_email = 'API eMenu - Database Update - {}'.format(yesterday.strftime('%d-%m-%Y'))
        html_body = render_to_string('eMenu/email.html', html_context)

        # Send e-mail to all users - every day 10 a.m.
        users = User.objects.filter(is_active=True, is_superuser=False)
        receivers = []
        for user in users:
            receivers.append(user.email)

        email = EmailMessage(subject_email, html_body, EMAIL_HOST_USER, receivers)
        email.content_subtype = 'html'
        email.send()
        self.stdout.write("E-mails Report was sent.")