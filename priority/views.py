from django.shortcuts import render, redirect
from core.models import Priority
from .forms import PriorityForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def priorities(request):
    priority = Priority.objects.all()
    context = {'activate_priorities': 'active', "priority": priority}
    return render(request, 'priority/priority.html', context)


@login_required(login_url='/login')
def create_priority(request):
    form = PriorityForm()
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/priorities')
    context = {'activate_priorities': 'active', 'form': form}
    return render(request, 'priority/priority_form.html', context)


@login_required(login_url='/login')
def update_priority(request, pk):
    priority = Priority.objects.get(id=pk)
    form = PriorityForm(instance=priority)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect('/priorities')
    context = {'activate_priorities': 'active', 'form': form}
    return render(request, 'priority/priority_form.html', context)


@login_required(login_url='/login')
def delete_priority(request, pk):
    priority = Priority.objects.get(id=pk)
    priority.delete()

    return redirect('/priorities')
