from django.shortcuts import render, redirect
from core.models import Group
from .forms import GroupForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def groups(request):
    groups = Group.objects.all()
    print(groups)
    context = {'activate_groups': 'active', 'groups': groups}
    return render(request, 'group/groups.html', context)


@login_required(login_url='/login')
def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            group = Group.objects.filter(name=form.cleaned_data['name'])
            print(group)
            users = form.cleaned_data['users']

            return redirect('/groups')

    context = {'activate_groups': 'active', 'form': form}
    return render(request, 'group/group_form.html', context)


@login_required(login_url='/login')
def update_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('/groups')
    context = {'activate_groups': 'active', 'form': form}
    return render(request, 'group/group_form.html', context)


@login_required(login_url='/login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    group.delete()

    return redirect('/groups')
