from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Priority, EmailSettings, Account
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Priority)
def create_priority(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Priorities")
    if len(settings) <= 0:
        return
    if settings[0].create:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created:
            users = Account.objects.filter(
                is_superuser=True).values_list('email', flat=True)
            message = f"Priority Created\nName: {instance.name}"
            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                list(users),
                fail_silently=False,
            )


@receiver(post_save, sender=Priority)
def update_priority(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Priorities")
    if len(settings) <= 0:
        return
    if settings[0].update:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created == False:
            users = Account.objects.filter(
                is_superuser=True).values_list('email', flat=True)
            message = f"Priority Updated\nName: {instance.name}"
            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                list(users),
                fail_silently=False,
            )
