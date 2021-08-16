from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Account, Ticket, Group, Board, EmailSettings, TicketLog
from django.core.mail import send_mail
from django.conf import settings
from TicketingSystem.email_task import *
import inspect


@receiver(post_save, sender=Ticket)
def create_ticket(sender, instance, created, **kwargs):
    if created:
        settings = EmailSettings.objects.filter(model_name="Ticket")
        if len(settings) <= 0:
            return
        request = None
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        message = f'''A new ticket has been created for {instance.assigned_group}
                \nTitle: {instance.title}
                \nDescription: {instance.description}
                \nPriority: {instance.priority}
                \nState: {instance.get_state()}
                \nBoard: {instance.board}
                \nClassification: {instance.classification}
                \nAssigned User: {instance.assigned_user}
                \nAssigned Group: {instance.assigned_group}

                '''
        log = TicketLog(ticket_name=instance.title, ticket_id=instance.id, title="Ticket Created",
                        updated_by=request.user, description=message)
        log.save()

        if settings[0].create:
            APP_NAME = getattr(settings, "APP_NAME", None)
            URL = getattr(settings, "URL", None)
            users = []
            admin_and_managers = Account.objects.filter(
                is_superuser=True, is_admin=True).values_list('email', flat=True)
            group_members = instance.assigned_group.users.all().values_list('email', flat=True)
            users = list(admin_and_managers) + list(group_members)
            unique_users = set(users)
            notify_user(message, list(unique_users))
            process_tasks()


@receiver(post_save, sender=Ticket)
def update_ticket(sender, instance, created, **kwargs):
    if created == False:
        settings = EmailSettings.objects.filter(model_name="Ticket")
        if len(settings) <= 0:
            return
        request = None
        for frame_record in inspect.stack():
            3
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        message = f'''A ticket has been updated for {instance.assigned_group}
                \nTitle: {instance.title}
                \nDescription: {instance.description}
                \nPriority: {instance.priority}
                \nState: {instance.get_state()}
                \nBoard: {instance.board}
                \nClassification: {instance.classification}
                \nAssigned User: {instance.assigned_user}
                \nAssigned Group: {instance.assigned_group}

                '''
        log = TicketLog(ticket_name=instance.title, ticket_id=instance.id, title="Ticket Updated",
                        updated_by=request.user, description=message)
        log.save()

        if settings[0].update:
            APP_NAME = getattr(settings, "APP_NAME", None)
            URL = getattr(settings, "URL", None)

            if created == False:

                users = []
                admin_and_managers = Account.objects.filter(
                    is_superuser=True, is_admin=True).values_list('email', flat=True)
                group_members = instance.assigned_group.users.all().values_list('email', flat=True)
                users = list(admin_and_managers) + list(group_members)
                unique_users = set(users)

                notify_user(message, list(unique_users))
                process_tasks()


@receiver(post_delete, sender=Ticket)
def delete_ticket(sender, instance, **kwargs):
    settings = EmailSettings.objects.filter(model_name="Ticket")
    if len(settings) <= 0:
        return
    request = None
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    message = f'''A ticket has been deleted for {instance.assigned_group}
            \nTitle: {instance.title}
            \nDescription: {instance.description}
            \nPriority: {instance.priority}
            \nState: {instance.get_state()}
            \nBoard: {instance.board}
            \nClassification: {instance.classification}
            \nAssigned User: {instance.assigned_user}
            \nAssigned Group: {instance.assigned_group}

            '''
    log = TicketLog(ticket_name=instance.title, ticket_id=instance.id, title="Ticket Deleted",
                    updated_by=request.user, description=message)
    log.save()

    if settings[0].delete:
        APP_NAME = getattr(settings, "APP_NAME", None)
        URL = getattr(settings, "URL", None)

        if created == False:

            users = []
            admin_and_managers = Account.objects.filter(
                is_superuser=True, is_admin=True).values_list('email', flat=True)
            group_members = instance.assigned_group.users.all().values_list('email', flat=True)
            users = list(admin_and_managers) + list(group_members)
            unique_users = set(users)

            notify_user(message, list(unique_users))
            process_tasks()
