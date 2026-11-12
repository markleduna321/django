from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm


@login_required
def home(request):
    context = {'tasks': request.user.tasks.all(), 'form': TaskForm()}
    return render(request, 'pages/home.html', context)


@login_required
@require_POST
def task_create(request):
    form = TaskForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=204)
    task = form.save(commit=False)
    task.user = request.user
    task.save()
    return render(request, 'pages/partials/task_item.html', {'task': task})


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(request.user.tasks, pk=pk)
    task.is_done = not task.is_done
    task.save(update_fields=['is_done'])
    return render(request, 'pages/partials/task_item.html', {'task': task})


@login_required
@require_POST
def task_delete(request, pk):
    get_object_or_404(request.user.tasks, pk=pk).delete()
    return HttpResponse('')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
