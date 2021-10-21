from django.shortcuts import render, redirect
from .forms import BoardForm
from core.models import Board, Ticket, Group, Account, TicketAttachment, Priority, BoardSuperuser
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import re
from django.db.models import Q
from django.http import HttpResponseRedirect


@login_required(login_url='/login')
def boards(request):
    current_user = request.user
    context = {}
    board = None
    selected_board = None
    tickets = None
    attachment = TicketAttachment.objects.all()
    priorities = Priority.objects.all()
    search_keyword = ''
    priority = '-1'
    selected_boards = [-1]

    if request.method == 'POST':
        keyword = request.POST.get('search_keyword')
        search_keyword = '' if keyword == None else keyword
        priority = request.POST.get('selected_priority')
        selected_boards = request.POST.get('selected_boards')
        print("value", selected_boards)
        # print("len", len(selected_boards))
        # print("check int", check_int(selected_boards))
        #
        print("value", selected_boards)
        if "," in selected_boards:
            selected_boards = selected_boards.replace('[', '').replace(']', '')
            selected_boards = selected_boards.split(",")
        elif len(selected_boards) > 0:
            selected_boards = selected_boards.replace('[', '').replace(']', '')
            print("removed", selected_boards)
            selected_boards = [int(selected_boards)]
        else:
            selected_boards = []
        print(selected_boards)

    if current_user.is_superuser or current_user.is_admin:
        boards = Board.get_all()
        print(search_keyword)
        tickets = Ticket.searchTicket(
            search_keyword=search_keyword)

        selected_boards = Board.filter_by_ids(selected_boards)
    else:
        group = Group.objects.filter(
            Q(users=current_user) | Q(supervisor=current_user))
        boards = Board.filter_all(group=group)
        if '-1' in selected_boards or -1 in selected_boards:
            print(group)
            tickets = Ticket.searchTicket(group=group,
                                          search_keyword=search_keyword, boards=boards)
            # selected_board = Board.objects.get(id=pk)
        else:
            print("user passed")
            tickets = Ticket.searchTicket(user=current_user,
                                          search_keyword=search_keyword, boards=boards)
            # selected_board = None
        selected_boards = Board.filter_by_ids(selected_boards)

    (todo, progress, review, completed) = Ticket.get_tickets(
        tickets=tickets, selected_boards=selected_boards)

    # (todo_general, progress_general, review_general, completed_general) = Ticket.get_all_assigned_tickets(
    #     tickets=tickets)

    # superuser = BoardSuperuser.filter(
    #     boards=selected_boards, user=current_user)
    # print(superuser)

    context = {'activate_board': 'active',
               "boards": boards,
               'todo': todo, 'progress': progress, 'review': review, 'completed': completed,
               #    'todo_general': todo_general, 'progress_general': progress_general, 'review_general': review_general, 'completed_general': completed_general,
               'selected_priority': priority,
               'priorities': priorities,
               'search_keyword': search_keyword,
               'selected_boards': list(map(lambda x: x['id'], selected_boards)),

               'board': ', '.join(list(map(lambda x: x['title'], selected_boards))), 'attachments': attachment}
    return render(request, 'board/board.html', context)


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


@login_required(login_url='/login')
def manage_board(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    return render(request, 'board/manage_board.html', context)


@login_required(login_url='/login')
def manage_superusers(request, pk):
    board = Board.objects.get(id=pk)

    users = Account.objects.raw(
        f'''
        SELECT DISTINCT core_account.id, core_account.email, core_boardsuperuser.board_id, core_boardsuperuser.can_complete_ticket, core_boardsuperuser.can_create_ticket FROM core_account
        JOIN core_group_users ON core_group_users.account_id = core_account.id
        JOIN core_board_group ON core_board_group.group_id = core_group_users.group_id
        LEFT  JOIN core_boardsuperuser ON core_account.id = core_boardsuperuser.user_id
        WHERE core_board_group.board_id = {board.id};
        ''')
    # 'SELECT core_account.id, core_account.email, core_boardsuperuser.board_id, core_boardsuperuser.can_complete_ticket, core_boardsuperuser.can_create_ticket  FROM core_account  LEFT  JOIN core_boardsuperuser ON core_account.id = core_boardsuperuser.user_id;')
    superusers = BoardSuperuser.objects.filter(board=board)
    if request.method == 'POST':
        for user in users:
            create = request.POST.get(f'create_{user.id}')
            complete = request.POST.get(f'complete_{user.id}')
            p, created = BoardSuperuser.objects.get_or_create(
                user=Account.objects.get(id=user.id),
                board=board,
            )
            p.can_create_ticket = statusToBool(create)
            p.can_complete_ticket = statusToBool(complete)
            p.save()
        return redirect(f'/update_board/{board.id}')

    context = {
        'board': board,
        'users': users,
        'superusers': superusers
    }
    print("no return")
    return render(request, 'board/superusers.html', context)


def statusToBool(value):
    if value == "on":
        return True
    else:
        print(False)
        return False


def update_board(request, pk):
    board = Board.objects.get(id=pk)
    form = BoardForm(instance=board)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('/manage_board')
    context = {'activate_classification': 'active',
               'form': form, 'board': board}
    return render(request, 'board/board_form.html', context)


def delete_board(request, pk):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    return render(request, 'board/manage_board.html', context)


@ login_required(login_url='/login')
def create_board(request):
    form = BoardForm()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/boards')
    context = {'activate_create_board': 'active', 'form': form}
    return render(request, 'board/board_form.html', context)


@ login_required(login_url='/login')
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


@ login_required(login_url='/login')
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
