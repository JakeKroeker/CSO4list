from django.db import models
from django.urls import reverse
from django.utils.safestring import SafeString
from django.conf import settings

class ToDoList(models.Model):
    """ToDo list containing all ToDoItems"""
    # Fields
    owner            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name             = models.CharField(max_length=64,             help_text='List name')
    description      = models.CharField(max_length=1000,           help_text='List description', null=True, blank=True)
    created_on       = models.DateTimeField(auto_now_add=True,     help_text='Creation date')
    updated_on       = models.DateTimeField(auto_now=True,         help_text='Last updated')

    # Metadata
    class Meta:
        ordering = ['name', 'updated_on', 'created_on']

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return SafeString(self.name)
