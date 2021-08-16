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


class Priority(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Classification(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50, null=True)


class Board(models.Model):
    title = models.CharField(max_length=200, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    state = models.IntegerField(default=0)
    board = models.ManyToManyField(Board)
    assigned_group = models.ManyToManyField(Group)
    assigned_user = models.ManyToManyField(Account, blank=True, null=True)
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE)
    can_staff_complete = models.BooleanField()

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
