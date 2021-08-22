from django.shortcuts import render, redirect
from .forms import BoardForm
from core.models import Board, Ticket, Group, Account, TicketAttachment, Priority
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def boards(request, pk='-1'):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
    attachment = TicketAttachment.objects.all()
    priorities = Priority.objects.all()
    search_keyword = ''
    priority = '-1'

    if request.method == 'POST':
        print(request.POST)
        keyword = request.POST.get('search_keyword')
        search_keyword = '' if keyword == None else keyword
        priority = request.POST.get('selected_priority')

    if current_user.is_superuser or current_user.is_admin:
        boards = Board.get_all()
        tickets = Ticket.searchTicket(
            search_keyword=search_keyword, priority_id=priority)

        if pk != '-1':
            selected_board = Board.objects.get(id=pk)
        else:
            selected_board = None
    else:
        group = Group.objects.filter(users=current_user)
        boards = Board.filter_all(group=group)
        if pk != '-1':
            tickets = Ticket.searchTicket(group=group,
                                          search_keyword=search_keyword, priority_id=priority)
            selected_board = Board.objects.get(id=pk)
        else:
            tickets = Ticket.searchTicket(user=current_user,
                                          search_keyword=search_keyword, priority_id=priority)
            selected_board = None

    (todo, progress, review, completed) = Ticket.get_tickets(
        tickets=tickets, selected_board=selected_board)

    context = {'activate_board': 'active',
               "boards": boards, 'todo': todo, 'progress': progress, 'review': review,
               'completed': completed,
               'selected_priority': priority,
               'priorities': priorities,
               'search_keyword': search_keyword,
               'board': selected_board, 'attachments': attachment}
    return render(request, 'board/board.html', context)


@login_required(login_url='/login')
def create_board(request):
    form = BoardForm()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/boards')
    context = {'activate_create_board': 'active', 'form': form}
    return render(request, 'board/board_form.html', context)


@login_required(login_url='/login')
def get_users(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        ticket = Ticket.objects.get(id=pk)
        ticket_group = ticket.assigned_group

        print(ticket.assigned_group.users.all())
        users = serializers.serialize(
            'json', ticket.assigned_group.users.all())

        return JsonResponse({"status": True, "users": users})
    return JsonResponse({"status": False})


@login_required(login_url='/login')
def claim_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    # user_instance = Account.objects.filter(pk__in=users)
    if request.user not in ticket.assigned_user.all():
        ticket.assigned_user.add(request.user)

    # ticket.assigned_user.add(request.user)
    # ticket.assigned_user = request.user
    ticket.state = 1
    ticket.save()
    return redirect('/boards')
