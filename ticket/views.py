from django.shortcuts import render, redirect
from core.models import Ticket, Group, TicketAttachment, TicketLog, Priority, Classification, Account, Board
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
        file_form = TicketAttachmentForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')  # field name in model

        if form.is_valid() and file_form.is_valid():
            ticket_instance = form.save(commit=False)
            ticket_instance.save()
            for f in files:
                file_instance = TicketAttachment(
                    file=f, ticket=ticket_instance)
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
def update_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)
    ticketAttachments = TicketAttachment.objects.filter(ticket=ticket)

    file_form = TicketAttachmentForm()

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
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
               'form': form, 'file_form': file_form, 'attachments': ticketAttachments}
    return render(request, 'ticket/ticket_update_form.html', context)


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
    print
    context = {'logs': logs}
    return render(request, 'ticket/ticket_log.html', context)


@login_required(login_url='/login')
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.is_deleted = False
    ticket.save()

    return redirect('/tickets')


@login_required(login_url='/login')
def delete_attachment(request, pk):
    ticket = TicketAttachment.objects.get(id=pk)
    ticket.delete()
    return redirect('/boards')
