from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import EmailSettings
from .forms import EmailSettingsForm


@login_required(login_url='/login')
def email_settings(request):
    email_settings = EmailSettings.objects.all()
    context = {'activate_email_settings': 'active',
               'email_settings': email_settings}
    return render(request, 'email_setting/email_settings.html', context)


def create_defaults():
    models = ["Classifications", "Groups", "Priorities", "Ticket", "Users"]
    for model in models:
        setting = EmailSettings(model_name=model,
                                create=False, update=False, delete=False)
        setting.save()


@login_required(login_url='/login')
def create_email_settings(request):
    form = EmailSettingsForm()
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/email_settings')

    context = {'activate_email_settings': 'active', 'form': form}
    return render(request, 'email_setting/email_setting_form.html', context)


@login_required(login_url='/login')
def update_email_settings(request, pk):
    group = EmailSettings.objects.get(id=pk)
    form = EmailSettingsForm(instance=group)
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('/email_settings')
    context = {'activate_email_settings': 'active', 'form': form}
    return render(request, 'email_setting/email_setting_form.html', context)
