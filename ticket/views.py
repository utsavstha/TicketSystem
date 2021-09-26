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
        supervisors = request.POST.get('supervisors')

        files = [request.FILES.get('files[%d]' % i)
                 for i in range(0, len(request.FILES))]
        staff = True if staff_complete == 'true' else False
        groups = groups.split(",") if "," in groups else groups
        boards = boards.split(",") if "," in boards else boards
        users = users.split(",") if "," in users else users
        supervisors = supervisors.split(
            ",") if "," in supervisors else supervisors
        classification_instance = Classification.objects.get(
            pk=classification)

        priority_instance = Priority.objects.get(pk=priority)

        ticket = Ticket(title=ticket_name, description=description,
                        priority=priority_instance, classification=classification_instance,
                        can_staff_complete=staff)
        ticket.save()
        group_instance = Group.objects.filter(pk__in=filter(len, groups))
        board_instance = Board.objects.filter(pk__in=filter(len, boards))
        ticket.assigned_group.set(group_instance)
        ticket.board.set(board_instance)

        if len(users) > 0:
            user_instance = Account.objects.filter(pk__in=filter(len, users))
            ticket.assigned_user.set(user_instance)

        if len(supervisors) > 0:
            supervisor_instance = Account.objects.filter(
                pk__in=filter(len, supervisors))
            ticket.ticket_supervisors.set(supervisor_instance)

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
               'priority_serialized': serializers.serialize('json', priorities),
               'classification_serialized': serializers.serialize('json', classifications),
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
    print(ticket.ticket_supervisors.all())
    logs = TicketLog.objects.filter(ticket_id=pk).order_by('-timestamp')
    attachments = TicketAttachment.objects.filter(ticket=ticket)
    comments = TicketComment.objects.filter(ticket=ticket, parent=None)
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
    parent = request.POST.get('parent')
    parent_instance = TicketComment.objects.filter(id=parent)
    comment = TicketComment(
        comment=content, ticket=ticket, parent=parent_instance.first(), posted_by=request.user)
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
        supervisors = request.POST.get('supervisors')
        files = [request.FILES.get('files[%d]' % i)
                 for i in range(0, len(request.FILES))]
        staff = True if staff_complete == 'true' else False
        groups = groups.split(",") if "," in groups else groups
        boards = boards.split(",") if "," in boards else boards
        users = users.split(",") if "," in users else users
        supervisors = supervisors.split(
            ",") if "," in supervisors else supervisors

        classification_instance = Classification.objects.get(
            pk=classification)

        priority_instance = Priority.objects.get(pk=priority)
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
        print(users)
        group_instance = Group.objects.filter(pk__in=filter(len, groups))
        board_instance = Board.objects.filter(pk__in=filter(len, boards))
        ticket.assigned_group.set(group_instance)
        ticket.board.set(board_instance)

        if len(users) > 0:
            user_instance = Account.objects.filter(pk__in=filter(len, users))
            ticket.assigned_user.set(user_instance)
        else:
            ticket.assigned_user.clear()

        if len(supervisors) > 0:
            supervisor_instance = Account.objects.filter(
                pk__in=filter(len, supervisors))
            ticket.ticket_supervisors.set(supervisor_instance)
        else:
            ticket.ticket_supervisors.clear()

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
               'priority_serialized': serializers.serialize('json', priorities),
               'classification_serialized': serializers.serialize('json', classifications),
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
        if "-" in id:
            id = id.split("-")[1]
        ticket = Ticket.objects.get(id=id)
        print("before", ticket.state)
        if has_privilages(current_user, id, state):
            ticket.state = state
            ticket.save()
            print("after", state)
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})

    return JsonResponse({"status": True})


def check_supervisor(user, boards, groups, ticket_supervisors):
    for ticket_supevisor in ticket_supervisors:
        if str(user) == str(ticket_supevisor):
            return True

    board_supervisors = []

    for board in boards:
        board_supervisors += get_all_supervisors_for_board(board)

    for supervisor in board_supervisors:
        if str(user) == str(supervisor):
            return True

    group_supervisors = []
    for group in groups:
        group_supervisors += get_all_supervisors_for_group(group)

    for supervisor in group_supervisors:
        if str(user) == str(supervisor):
            return True

    return False


def get_all_supervisors_for_group(group):
    group = Group.objects.get(pk=group.id)
    return list(group.supervisor.all().values_list('email', flat=True))


def get_all_supervisors_for_board(board):
    board = Board.objects.get(pk=board.id)
    return list(board.supervisor.all().values_list('email', flat=True))


def has_privilages(user, ticketId, state):
    ticket = Ticket.objects.get(id=ticketId)
    assigned_boards = ticket.board.all()
    assigned_groups = ticket.assigned_group.all()
    ticket_supervisors = list(
        ticket.ticket_supervisors.all().values_list('email', flat=True))

    if user.is_superuser or user.is_admin:
        return True
    elif check_supervisor(user, assigned_boards, assigned_groups, ticket_supervisors):
        print("supervisor")
        return True
    else:
        # assigned_users = list(ticket.assigned_user.all().values_list('email', flat=True)))
        if int(state) == 3:
            if ticket.can_staff_complete:
                return True
            else:
                return False
        if isAssigned(user, ticket.assigned_user.all().values_list('email', flat=True)):
            print("assigned")
            return True
        '''
        groups = Group.objects.filter(users=user)
        for group in groups:
            for assgined_group in ticket.assigned_group.all():
                if assgined_group == group:
                    print("in group")
                    if int(state) == 3:
                        if isSupervisor(group.supervisor.all(), user):
                            return True
                        elif ticket.can_staff_complete:
                            if isAssigned(user, ticket.assigned_user.all()):
                                print("assigned")
                                return True
                    else:
                        if isSupervisor(group.supervisor.all(), user):
                            return True
                        elif isAssigned(user, ticket.assigned_user.all()):
                            print("assigned")
                            return True
        '''

        return False


def isSupervisor(supervisors, user):
    for supervisor in supervisors:
        if supervisor == user:
            return True
    return False


def isAssigned(user, users):
    for u in users:
        if str(u) == str(user):
            print("isAssigned", True)
            return True
    return False


@ login_required(login_url='/login')
def view_logs(request, pk):
    logs = TicketLog.objects.filter(ticket_id=pk)
    context = {'logs': logs}
    return render(request, 'ticket/ticket_log.html', context)


@ login_required(login_url='/login')
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()

    return redirect('/tickets')


@ login_required(login_url='/login')
def delete_attachment(request, pk):
    ticket = TicketAttachment.objects.get(id=pk)
    ticket.delete()
    return redirect('/boards')
