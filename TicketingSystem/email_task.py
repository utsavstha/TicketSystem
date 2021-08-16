import subprocess
import shlex
from background_task import background
from django.core.mail import send_mail
from django.conf import settings


@background(schedule=1)
def notify_user(message, recipients):
    APP_NAME = getattr(settings, "APP_NAME", None)
    print("sending")
    send_mail(
        APP_NAME,
        message,
        'ticketingsystem@gmail.com',
        recipients,
        fail_silently=False,
    )
    print("sent")


def process_tasks():
    process_tasks_cmd = "python manage.py process_tasks --duration 60"
    process_tasks_args = shlex.split(process_tasks_cmd)
    process_tasks_subprocess = subprocess.Popen(process_tasks_args)
