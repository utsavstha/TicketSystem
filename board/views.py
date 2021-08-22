from django.shortcuts import render, redirect
from .forms import BoardForm
from core.models import Board, Ticket, Group, Account, TicketAttachment, Priority
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def boards(request, pk=''):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
    attachment = TicketAttachment.objects.all()
    priorities = Priority.objects.all()
    todo = []
    progress = []
    review = []
    completed = []

    if current_user.is_superuser or current_user.is_admin:
        boards = Board.objects.all()
        tickets = Ticket.objects.all()
        print(boards)
        if pk != '':
            selected_board = Board.objects.get(id=pk)
        else:
            selected_board = None if len(boards) == 0 else boards[0]
    else:
        print(pk)
        group = Group.objects.filter(users=current_user)
        boards = Board.objects.filter(id=pk, group__in=group)
        tickets = Ticket.objects.filter(assigned_group__in=group)
        selected_board = None if len(boards) == 0 else boards[0]

    for ticket in tickets:
        for ticket_board in ticket.boards.all:
            if ticket_board.id == selected_board.id:
                if ticket.state == 0:
                    todo.append(ticket)
                elif ticket.state == 0:
                    progress.append(ticket)
                elif ticket.state == 0:
                    review.append(ticket)
                elif ticket.state == 0:
                    completed.append(ticket)

    context = {'activate_board': 'active',
               "boards": boards, 'todo': todo, 'progress': progress, 'review': review,
               'completed': completed,
               'priorities': priorities,
               'board': selected_board, 'attachments': attachment}
    return render(request, 'board/board.html', context)


# @login_required(login_url='/login')
# def search_ticket(request):
#     if request.method == 'POST':
#         search_keyword = request.POST.get('search_keyword')
#         current_user = request.user
#         if current_user.is_superuser or current_user.is_admin:
#             tickets = Ticket.objects.filter(title__contains=search_keyword)
#             context = {'activate_board': 'active',
#                        "boards": boards, 'tickets': tickets,
#                        'priorities': priorities,
#                        'board': selected_board, 'attachments': attachment}
#         return render(request, 'board/board.html', context)


@login_required(login_url='/login')
def get_board(request, pk):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
    priorities = Priority.objects.all()

    if current_user.is_superuser or current_user.is_admin:
        boards = Board.objects.all()
        tickets = Ticket.objects.all()
        selected_board = Board.objects.get(id=pk)

    else:
        group = Group.objects.filter(users=current_user)
        boards = Board.objects.filter(id=pk, group__in=group)
        tickets = Ticket.objects.filter(assigned_group__in=group)
        selected_board = None if len(boards) == 0 else boards[0]

    context = {'activate_board': 'active',
               'priorities': priorities,
               "boards": boards, 'tickets': tickets, 'board': selected_board}
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
    ticket.assigned_user = request.user
    ticket.state = 1
    ticket.save()
    return redirect('/boards')
