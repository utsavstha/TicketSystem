from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os


class TicketAccountManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(verbose_name="manager", default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = TicketAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Group(models.Model):
    name = models.CharField(max_length=100, null=True)
    users = models.ManyToManyField(Account, blank=True)
    supervisor = models.ManyToManyField(
        Account, blank=True, related_name='supervisors')

    def __str__(self):
        return self.name

    @property
    def number_of_users(self):
        return len(self.users.all())


class State(models.Model):
    name = models.CharField(max_length=50, null=True)


'''
class Board(models.Model):
    title = models.CharField(max_length=200, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_all():
        all_boards = []
        boards = Board.objects.all()
        all_boards.append({"title": "General", "id": -1})

        for i in range(len(boards)):
            all_boards.append(boards[i])
        return all_boards

    def filter_all(group):
        all_boards = []
        boards = Board.objects.filter(group__in=group)
        all_boards.append({"title": "General", "id": -1})
        for i in range(len(boards)):
            all_boards.append(boards[i])
        return all_boards
'''


class Board(models.Model):
    title = models.CharField(max_length=200, null=True)
    group = models.ManyToManyField(Group)
    supervisor = models.ManyToManyField(
        Account, blank=True, related_name='board_supervisors')

    def __str__(self):
        return self.title

    def get_general():
        return {"title": "General", "id": -1}

    def remove_general(boards):
        if boards != None:
            new_boards = []
            for board in boards:
                if type(board) != dict:
                    new_boards.append(board)
            return new_boards

    def get_all():
        all_boards = []
        boards = Board.objects.all()
        all_boards.append({"title": "General", "id": -1})

        for i in range(len(boards)):
            all_boards.append(boards[i])
        return all_boards

    def filter_by_ids(ids):
        general_board_found = False
        print("filter_by_ids", ids)
        if '-1' in ids:
            ids.remove('-1')
            general_board_found = True
        if -1 in ids:
            ids.remove(-1)
            general_board_found = True
        boards = Board.objects.filter(id__in=ids)
        all_boards = []
        if general_board_found:
            all_boards.append({"title": "General", "id": -1})
        for i in range(len(boards)):
            all_boards.append({"title": boards[i].title, "id": boards[i].id})
        return all_boards

    def filter_all(group):
        all_boards = []
        boards = Board.objects.filter(group__in=group)
        all_boards.append({"title": "General", "id": -1})
        for i in range(len(boards)):
            all_boards.append(boards[i])
        return all_boards


class Priority(models.Model):
    name = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=10, null=True)
    priority_value = models.IntegerField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_id(self):
        return int(self.id)


class Classification(models.Model):
    name = models.CharField(max_length=200, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    state = models.IntegerField(default=0)
    board = models.ManyToManyField(Board)
    assigned_group = models.ManyToManyField(Group)
    assigned_user = models.ManyToManyField(Account)
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE)
    can_staff_complete = models.BooleanField()

    def searchTicket(group=None, search_keyword='', user=None, boards=None):
        tickets = []
        boards = Board.remove_general(boards)
        # print(boards)
        # if boards != None:
        #     tickets = Ticket.objects.filter(
        #         title__icontains=search_keyword, board__in=boards)
        # else:
        #     tickets = Ticket.objects.filter(title__icontains=search_keyword)

        # if user != None:
        #     tickets = Ticket.objects.filter(
        #         assigned_user=user)

        if group != None:
            if boards != None:
                tickets = Ticket.objects.filter(
                    title__icontains=search_keyword, board__in=boards)
            else:
                tickets = Ticket.objects.filter(
                    title__icontains=search_keyword)
        else:
            if user != None:
                if boards != None:
                    tickets = Ticket.objects.filter(
                        assigned_user=user, title_icontains=search_keyword, board__in=boards)
                else:
                    tickets = Ticket.objects.filter(
                        assigned_user=user, title_icontains=search_keyword)
            else:
                if boards != None:
                    tickets = Ticket.objects.filter(
                        title__icontains=search_keyword, board__in=boards)
                else:
                    tickets = Ticket.objects.filter(
                        title__icontains=search_keyword)

        return tickets

    def get_assigned_users(self):
        users = ', '.join(self.assigned_user.values_list('email', flat=True))
        return users if len(self.assigned_user.all()) > 0 else "Unassgined"

    def get_board(self):
        boards = ', '.join(self.board.values_list('title', flat=True))
        return boards if len(self.board.all()) > 0 else "Unassgined"

    def get_assigned_group(self):
        assigned_group = ', '.join(
            self.assigned_group.values_list('name', flat=True))
        print(assigned_group)
        return assigned_group if len(self.assigned_group.all()) > 0 else "Unassgined"

    def get_state(self):
        state = "Todo"
        if self.state == 0:
            state = "Todo"
        elif self.state == 1:
            state = "In Progress"
        elif self.state == 1:
            state = "In Review"
        else:
            state = "Completed"
        return state

    def get_all_assigned_tickets(tickets):
        todo = []
        progress = []
        review = []
        completed = []
        for ticket in tickets:
            if ticket.state == 0:
                todo.append(ticket)
            elif ticket.state == 1:
                progress.append(ticket)
            elif ticket.state == 2:
                review.append(ticket)
            elif ticket.state == 3:
                completed.append(ticket)

        return (todo, progress, review, completed)

    def get_tickets(tickets, selected_boards):
        todo = []
        progress = []
        review = []
        completed = []
        for ticket in tickets:
            for ticket_board in ticket.board.all():
                for selected_board in selected_boards:
                    if selected_board['id'] == -1:
                        if ticket.state == 0:
                            todo.append(ticket)
                        elif ticket.state == 1:
                            progress.append(ticket)
                        elif ticket.state == 2:
                            review.append(ticket)
                        elif ticket.state == 3:
                            completed.append(ticket)
                    elif ticket_board.id == int(selected_board['id']):
                        if ticket.state == 0:
                            todo.append(ticket)
                        elif ticket.state == 1:
                            progress.append(ticket)
                        elif ticket.state == 2:
                            review.append(ticket)
                        elif ticket.state == 3:
                            completed.append(ticket)
        return (set(todo), set(progress), set(review), set(completed))

    def __str__(self):
        return self.title


class TicketLog(models.Model):
    ticket_name = models.CharField(max_length=200, null=True)
    ticket_id = models.IntegerField()
    timestamp = models.DateTimeField(verbose_name="timestamp", auto_now=True)
    title = models.CharField(max_length=200, null=True)
    updated_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return self.title


class TicketComment(models.Model):
    comment = models.CharField(max_length=1000, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name="timestamp", auto_now=True)
    posted_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.comment

    def children(self):
        return TicketComment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class TicketAttachment(models.Model):
    file = models.FileField(blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def filename(self):
        print(self.file.name)
        return os.path.basename(self.file)


class EmailSettings(models.Model):
    model_name = models.CharField(max_length=50, null=True)
    create = models.BooleanField()
    update = models.BooleanField()
    delete = models.BooleanField()

    def __str__(self):
        return self.model_name
