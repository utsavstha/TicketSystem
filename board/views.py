from django.shortcuts import render, redirect
from .forms import BoardForm
from core.models import Board, Ticket, Group, Account, TicketAttachment
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def boards(request):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
    attachment = TicketAttachment.objects.all()

    if current_user.is_superuser or current_user.is_admin:
        boards = Board.objects.all()
        tickets = Ticket.objects.all()
        selected_board = None if len(boards) == 0 else boards[0]
    else:
        group = Group.objects.filter(users=current_user)
        boards = Board.objects.filter(group__in=group)
        tickets = Ticket.objects.filter(assigned_group__in=group)
        selected_board = None if len(boards) == 0 else boards[0]

    context = {'activate_board': 'active',
               "boards": boards, 'tickets': tickets, 'board': selected_board, 'attachments': attachment}
    return render(request, 'board/board.html', context)


@login_required(login_url='/login')
def get_board(request, pk):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
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
