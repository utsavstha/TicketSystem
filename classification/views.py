from django.shortcuts import render, redirect
from core.models import Classification
from .forms import ClassificationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def classification(request):
    classification = Classification.objects.all()
    context = {'activate_classification': 'active',
               "classifications": classification}
    return render(request, 'classification/classification.html', context)


@login_required(login_url='/login')
def create_classification(request):
    form = ClassificationForm()
    if request.method == 'POST':
        form = ClassificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/classification')
    context = {'activate_classification': 'active', 'form': form}
    return render(request, 'classification/classification_form.html', context)


@login_required(login_url='/login')
def update_classification(request, pk):
    classification = Classification.objects.get(id=pk)
    form = ClassificationForm(instance=classification)
    if request.method == 'POST':
        form = ClassificationForm(request.POST, instance=classification)
        if form.is_valid():
            form.save()
            return redirect('/classification')
    context = {'activate_classification': 'active', 'form': form}
    return render(request, 'classification/classification_form.html', context)


@login_required(login_url='/login')
def delete_classification(request, pk):
    classification = Classification.objects.get(id=pk)
    classification.delete()

    return redirect('/classification')
