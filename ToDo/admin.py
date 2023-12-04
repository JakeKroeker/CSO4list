from django.contrib import admin
from .models import ToDoList, ToDoItem

admin.site.register(ToDoItem)
admin.site.register(ToDoList)
