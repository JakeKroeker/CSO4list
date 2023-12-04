from django.db import models
from django.urls import reverse
from django.utils.safestring import SafeString
from .ToDoList import ToDoList

class ToDoItem(models.Model):
    """A single ToDo item"""
    # Fields
    due_date         = models.DateTimeField(auto_now_add=False, help_text='Due date', null=True, blank=True)
    name             = models.CharField(max_length=64,          help_text='Task name')
    description      = models.CharField(max_length=1000,        help_text='Task description', null=True, blank=True)
    complete         = models.BooleanField(default=False,       help_text='Task is completed')
    created_on       = models.DateTimeField(auto_now_add=True,  help_text='Creation date')
    updated_on       = models.DateTimeField(auto_now=True,      help_text='Last updated')
    to_do_list       = models.ForeignKey(ToDoList,              on_delete=models.CASCADE)

    # Metadata
    class Meta:
        ordering = ['complete', '-due_date', 'name']

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return SafeString(self.name)
