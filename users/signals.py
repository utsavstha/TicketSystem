from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Account, EmailSettings
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Account)
def create_account(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Users")
    if len(settings) <= 0:
        return
    if settings[0].create:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created:
            message = f"Account Created:\nName: {instance.first_name} {instance.last_name}\nPlease login to: {URL}"

            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                [instance.email],
                fail_silently=False,
            )


@receiver(post_save, sender=Account)
def update_account(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Users")
    if len(settings) <= 0:
        return
    if settings[0].update:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created == False:
            message = f"Account Updated:\nName: {instance.first_name} {instance.last_name}\nPlease login to: {URL}"
            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                [instance.email],
                fail_silently=False,
            )
