from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Group, EmailSettings
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Groups")
    if len(settings) <= 0:
        return
    if settings[0].create:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created:
            users = instance.users.all().values_list('email', flat=True)
            supervisors = instance.supervisor.all().values_list('email', flat=True)
            message = f"Group Created\nName: {instance.name} \nUsers: {list(users)}\nSupervisor: {list(supervisors)}"
            email_users = list(users) + list(supervisors)
            unique_users = set(email_users)
            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                list(unique_users),
                fail_silently=False,
            )


@receiver(post_save, sender=Group)
def update_group(sender, instance, created, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Groups")
    if len(settings) <= 0:
        return
    if settings[0].update:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created == False:
            users = instance.users.all().values_list('email', flat=True)
            supervisors = instance.supervisor.all().values_list('email', flat=True)
            message = f"Group Updated\nName: {instance.name} \nUsers: {list(users)}\nSupervisor: {list(supervisors)}"
            email_users = list(users) + list(supervisors)
            unique_users = set(email_users)
            send_mail(
                APP_NAME,
                message,
                'ticketingsystem@gmail.com',
                list(unique_users),
                fail_silently=False,
            )
