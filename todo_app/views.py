"""from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'Acceuil.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('-created_at'), Task.objects.filter(user=request.user)
    print(f"Found {tasks.count()} tasks for user {request.user}")  # Debug
    for task in tasks:
        print(f"Task {task.id}: {task.title}")  # Debug
    return render(request, 'task_list.html', {'tasks': tasks})
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'task_detail.html', {'task': task})

    return render(request, 'task_detail.html', {'task': task})
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tache ajoutee!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'task': None})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tache misa a jour!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tache supprimee')
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        messages.success(request, f'Tache {"completee" if task.completed else "incomplete"}!')
        return redirect('task_list')"""




"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'Acceuil.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        # Personnaliser les textes d'aide
        form.fields['username'].help_text = 'Requis. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.'
        form.fields['password1'].help_text = [
            'Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.\n',
            'Votre mot de passe doit contenir au moins 8 caractères.',
            'Votre mot de passe ne peut pas être un mot de passe couramment utilisé.',
            'Votre mot de passe ne peut pas être entièrement numérique'

        ]
        form.fields['password2'].help_text = 'Entrez le même mot de passe que précédemment, pour vérification.'

    return render(request, 'registration/signup.html', {'form': form})
@login_required
def task_list(request):
    # CORRECTION: Supprimez la virgule et utilisez seulement filter par utilisateur
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    print(f"Found {tasks.count()} tasks for user {request.user}")  # Debug
    for task in tasks:
        print(f"Task {task.id}: {task.title}")  # Debug
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tache ajoutee!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'task': None})

@login_required  # Ajoutez ce décorateur
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ajoutez user=request.user
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tache misa a jour!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'task': task})

@login_required  # Ajoutez ce décorateur
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ajoutez user=request.user
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tache supprimee')
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

@login_required  # Ajoutez ce décorateur
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # Ajoutez user=request.user
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        messages.success(request, f'Tache {"completee" if task.completed else "incomplete"}!')
        return redirect('task_list')
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    """Home page showing available apps"""
    apps = [
        {
            'name': 'TODO APP',
            'url': 'todo_app:task_list',  # Your existing TODO app
            'description': 'Manage your tasks and to-do lists'
        },
        {
            'name': 'CAR PREDICTION APP',
            'url': 'car_prediction:home',  # New car prediction app
            'description': 'Predict car purchase amounts based on customer data'
        },
    ]

    return render(request, 'Acceuil.html', {'apps': apps})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        # Personnaliser les textes d'aide
        form.fields['username'].help_text = 'Requis. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement.'
        form.fields['password1'].help_text = [
            'Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.\n',
            'Votre mot de passe doit contenir au moins 8 caractères.',
            'Votre mot de passe ne peut pas être un mot de passe couramment utilisé.',
            'Votre mot de passe ne peut pas être entièrement numérique'
        ]
        form.fields['password2'].help_text = 'Entrez le même mot de passe que précédemment, pour vérification.'

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def task_list(request):
    # CORRECTION: Supprimez la virgule et utilisez seulement filter par utilisateur
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    print(f"Found {tasks.count()} tasks for user {request.user}")  # Debug
    for task in tasks:
        print(f"Task {task.id}: {task.title}")  # Debug
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tache ajoutee!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'task': None})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tache misa a jour!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tache supprimee')
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        messages.success(request, f'Tache {"completee" if task.completed else "incomplete"}!')
        return redirect('task_list')