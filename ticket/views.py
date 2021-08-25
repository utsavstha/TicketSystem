from django.shortcuts import render, redirect
from core.models import Ticket, Group, TicketAttachment, TicketLog, Priority, Classification, Account, Board, TicketComment
from .forms import TicketAttachmentForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers


@login_required(login_url='/login')
def tickets(request):
    tickets = Ticket.objects.all()
    context = {'activate_tickets': 'active', "tickets": tickets}
    return render(request, 'ticket/tickets.html', context)


@login_required(login_url='/login')
def create_ticket(request):
    priorities = Priority.objects.all()
    classifications = Classification.objects.all()
    groups = Group.objects.all()
    accounts = Account.objects.all()
    boards = Board.objects.all()
    file_form = TicketAttachmentForm()
    if request.method == 'POST':
        ticket_name = request.POST.get('ticket_name')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        groups = request.POST.get('groups')
        boards = request.POST.get('boards')
        classification = request.POST.get('classification')
        staff_complete = request.POST.get('staff_complete')
        users = request.POST.get('users')
        files = [request.FILES.get('files[%d]' % i)
                 for i in range(0, len(request.FILES))]
        staff = True if staff_complete == 'true' else False
        groups = groups.split(",") if "," in groups else groups
        boards = boards.split(",") if "," in boards else boards
        users = users.split(",") if "," in users else users

        classification_instance = Classification.objects.filter(
            name=classification).first()

        priority_instance = Priority.objects.filter(name=priority).first()

        ticket = Ticket(title=ticket_name, description=description,
                        priority=priority_instance, classification=classification_instance,
                        can_staff_complete=staff)
        ticket.save()
        group_instance = Group.objects.filter(pk__in=groups)
        board_instance = Board.objects.filter(pk__in=boards)
        ticket.assigned_group.set(group_instance)
        ticket.board.set(board_instance)

        if len(users) > 0:
            user_instance = Account.objects.filter(pk__in=users)
            ticket.assigned_user.set(user_instance)

        ticket.save()

        for f in files:
            file_instance = TicketAttachment(
                file=f, ticket=ticket)
            file_instance.save()
        return redirect('/boards')

    context = {'activate_tickets': 'active',
               'priorities': priorities, 'classifications': classifications,
               'groups': groups, 'boards': boards, 'groups_serialized': serializers.serialize('json', groups),
               'boards_serialized': serializers.serialize('json', boards),
               'accounts_serialized': serializers.serialize('json', accounts),
               'accounts': accounts, 'file_form': file_form}
    return render(request, 'ticket/ticket_form.html', context)


@login_required(login_url='/login')
def quick_attach(request, pk):
    files = request.FILES.getlist('file')
    ticket = Ticket.objects.get(id=pk)
    for f in files:
        file_instance = TicketAttachment(
            file=f, ticket=ticket)
        file_instance.save()
    return redirect('/boards')


@login_required(login_url='/login')
def ticket_info(request, pk):
    ticket = Ticket.objects.get(id=pk)
    logs = TicketLog.objects.filter(ticket_id=pk)
    attachments = TicketAttachment.objects.filter(ticket=ticket)
    comments = TicketComment.objects.filter(ticket=ticket)
    file_form = TicketAttachmentForm()

    context = {'ticket': ticket,
               'logs': logs,
               'comments': comments,
               'file_form': file_form,
               'attachments': attachments}
    return render(request, 'ticket/ticket_info.html', context)


@login_required(login_url='/login')
def post_comment(request, pk):
    ticket = Ticket.objects.get(id=pk)
    content = request.POST.get('content')
    comment = TicketComment(
        comment=content, ticket=ticket, posted_by=request.user)
    comment.save()
    return redirect('ticket_info', pk=pk)


@login_required(login_url='/login')
def update_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    priorities = Priority.objects.all()
    classifications = Classification.objects.all()
    groups = Group.objects.all()
    accounts = Account.objects.all()
    boards = Board.objects.all()
    ticketAttachments = TicketAttachment.objects.filter(ticket=ticket)

    file_form = TicketAttachmentForm()

    if request.method == 'POST':
        ticket_name = request.POST.get('ticket_name')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        groups = request.POST.get('groups')
        boards = request.POST.get('boards')
        classification = request.POST.get('classification')
        staff_complete = request.POST.get('staff_complete')
        users = request.POST.get('users')
        files = [request.FILES.get('files[%d]' % i)
                 for i in range(0, len(request.FILES))]
        staff = True if staff_complete == 'true' else False
        groups = groups.split(",") if "," in groups else groups
        boards = boards.split(",") if "," in boards else boards
        users = users.split(",") if "," in users else users

        classification_instance = Classification.objects.filter(
            name=classification).first()

        priority_instance = Priority.objects.filter(name=priority).first()
        ticket = Ticket.objects.get(id=pk)
        ticket.title = ticket_name
        ticket.description = description
        ticket.priority = priority_instance
        ticket.classification = classification_instance
        ticket.can_staff_complete = staff
        # ticket = Ticket(title=ticket_name, description=description,
        #                 priority=priority_instance, classification=classification_instance,
        #                 can_staff_complete=staff)
        ticket.save()
        group_instance = Group.objects.filter(pk__in=groups)
        board_instance = Board.objects.filter(pk__in=boards)
        ticket.assigned_group.set(group_instance)
        ticket.board.set(board_instance)

        if len(users) > 0:
            user_instance = Account.objects.filter(pk__in=users)
            ticket.assigned_user.set(user_instance)

        ticket.save()

        for f in files:
            file_instance = TicketAttachment(
                file=f, ticket=ticket)
            file_instance.save()
        return redirect('/boards')

    context = {'activate_tickets': 'active',
               'priorities': priorities, 'classifications': classifications,
               'groups': groups,
               'ticket_serialized': serializers.serialize('json', [ticket, ]),
               'boards': boards, 'groups_serialized': serializers.serialize('json', groups),
               'boards_serialized': serializers.serialize('json', boards),
               'accounts_serialized': serializers.serialize('json', accounts),
               'accounts': accounts, 'file_form': file_form, 'ticket': ticket, 'attachments': ticketAttachments}
    return render(request, 'ticket/ticket_update_form.html', context)


'''
def update_ticket(request, pk):

    priorities = Priority.objects.all()
    classifications = Classification.objects.all()
    groups = Group.objects.all()
    accounts = Account.objects.all()
    boards = Board.objects.all()

    ticket = Ticket.objects.get(id=pk)
    # form = TicketForm(instance=ticket)
    ticketAttachments = TicketAttachment.objects.filter(ticket=ticket)

    file_form = TicketAttachmentForm()

    if request.method == 'POST':
        # form = TicketForm(request.POST, instance=ticket)
        file_form = TicketAttachmentForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model
        if form.is_valid() and file_form.is_valid():
            form.save()
            for f in files:
                file_instance = TicketAttachment(
                    file=f, ticket=ticket)
                file_instance.save()
            return redirect('/boards')
    context = {'activate_tickets': 'active',
               'priorities': priorities, 'classifications': classifications,
               'groups': groups,
               'ticket_serialized': serializers.serialize('json', [ticket, ]),
               'boards': boards, 'groups_serialized': serializers.serialize('json', groups),
               'boards_serialized': serializers.serialize('json', boards),
               'accounts_serialized': serializers.serialize('json', accounts),
               'accounts': accounts, 'file_form': file_form, 'ticket': ticket, 'attachments': ticketAttachments}

    return render(request, 'ticket/ticket_update_form.html', context)

'''


@login_required(login_url='/login')
def change_state(request):
    current_user = request.user

    if request.method == 'POST':
        state = request.POST.get('state')
        id = request.POST.get('id')
        ticket = Ticket.objects.get(id=id)
        if has_privilages(current_user, id, state) or ticket.can_staff_complete:
            ticket.state = state
            ticket.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})

    return JsonResponse({"status": True})


def has_privilages(user, ticketId, state):
    if user.is_superuser or user.is_admin:
        return True
    else:
        print(state)
        groups = Group.objects.filter(users=user)
        ticket = Ticket.objects.get(id=ticketId)
        for group in groups:
            if ticket.assigned_group == group:
                if int(state) == 3:
                    for supervisor in group.supervisor.all():
                        if supervisor == user:
                            return True
                else:
                    return True
        return False


@login_required(login_url='/login')
def view_logs(request, pk):
    logs = TicketLog.objects.filter(ticket_id=pk)
    context = {'logs': logs}
    return render(request, 'ticket/ticket_log.html', context)


@login_required(login_url='/login')
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()

    return redirect('/tickets')


@login_required(login_url='/login')
def delete_attachment(request, pk):
    ticket = TicketAttachment.objects.get(id=pk)
    ticket.delete()
    return redirect('/boards')
