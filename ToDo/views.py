from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from datetime import datetime
from .forms import AddToDoItem, LoginCreate
from .models.ToDoItem import ToDoItem
from .models.ToDoList import ToDoList


def index(request):
    """View function for main todo list page."""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))

    # Currently users only have a single list.
    lists = request.user.todolist_set.all()
    if not lists:
        list = ToDoList(name="list", 
                        description="Your first list", 
                        owner=request.user)
        list.save()
    else:
        list = lists[0]

    entries = list.todoitem_set.all()

    context = {
        'entries': entries,
    }

    return render(request, 'index.html', context=context)


#logs in user or creates them if that name is available, kind of lazy
@csrf_protect
def login_create_user(request):
    context = {
        'message': '',
    }
    if request.method == 'POST':
        form = LoginCreate(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('todo_list'))
            #well let's just create them
            else:
                if User.objects.filter(username = form.cleaned_data['username']).exists():
                    context = {
                        'message': 'Wrong password.',
                    }
                    return render(request, 'login.html', context=context)
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['username'], form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('todo_list'))
                else:
                    context = {
                        'message': 'You need a username and password. They can be anything as long as they are not empty.',
                    }

    return render(request, 'login.html', context=context)


#logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_create_user'))


#view list item
def item(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))

    """View and edit todo list item."""
    lists = request.user.todolist_set.all()

    if not lists:
        raise PermissionDenied()
    
    list = lists[0]
    item = get_object_or_404(ToDoItem, pk=pk)
    #check this list belongs to the current user
    if list != item.to_do_list:
        raise PermissionDenied()

    context = {
        'item': item,
    }
    return render(request, 'item.html', context=context)


#create a new ToDo list item
@csrf_protect
def create_list_item(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))

    list = request.user.todolist_set.all()[0]

    if request.method == 'POST':
        form = AddToDoItem(request.POST)
        if form.is_valid():
            try:
                due = datetime.strptime(form.cleaned_data['due_date'],
                                        '%Y-%m-%dT%H:%M')
            except ValueError:
                due = None
            newItem = ToDoItem(name        = form.cleaned_data['item_name'], 
                               description = form.cleaned_data['item_description'], 
                               due_date    = due,
                               to_do_list  = list)
            newItem.save() 

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


#update the ToDo list item given by the pk
@csrf_protect
def update_list_item(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('todo_list'))
    
    lists = request.user.todolist_set.all()

    if not lists:
        raise PermissionDenied()
    
    list = lists[0]
    item = get_object_or_404(ToDoItem, pk=pk)
    #check this list belongs to the current user
    if list != item.to_do_list:
        raise PermissionDenied()

    if request.method == 'POST':
        form = AddToDoItem(request.POST)
        if form.is_valid():
            try:
                due = datetime.strptime(form.cleaned_data['due_date'],
                                        '%Y-%m-%dT%H:%M')
            except ValueError:
                due = None
            item.name = form.cleaned_data['item_name']
            item.description = form.cleaned_data['item_description']
            item.due_date = due
            item.complete = form.cleaned_data['complete']
            item.save() 


    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


#toggles complete value
@csrf_protect
def toggle_list_item(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('todo_list'))

    lists = request.user.todolist_set.all()

    if not lists:
        raise PermissionDenied()
    
    list = lists[0]
    item = get_object_or_404(ToDoItem, pk=pk)
    #check this list belongs to the current user
    if list != item.to_do_list:
        raise PermissionDenied()

    item.complete = not item.complete 
    item.save() 

    return HttpResponseRedirect(reverse('todo_list'))

#delete an item from the ToDo list
@csrf_protect
def delete_list_item(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login_create_user'))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('todo_list'))

    lists = request.user.todolist_set.all()

    if not lists:
        raise PermissionDenied()
    
    list = lists[0]
    item = get_object_or_404(ToDoItem, pk=pk)
    #check this list belongs to the current user
    if list != item.to_do_list:
        raise PermissionDenied()
    
    item.delete() 

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
