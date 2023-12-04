from django.urls import path
from . import views

urlpatterns = [
    path("",                  views.index, name="index"),
    path("list",              views.index, name="todo_list"),
    path("item/<int:pk>",     views.item,  name="list_item"),
    path("create",            views.create_list_item,   name="create_list_item"),
    path("update/<int:pk>",   views.update_list_item,   name="update_list_item"),
    path("delete/<int:pk>",   views.delete_list_item,   name="delete_list_item"),
    path("complete/<int:pk>", views.toggle_list_item,   name="toggle_list_item"),
    path("login_create",      views.login_create_user,  name="login_create_user"),
    path("logout",            views.logout_view,        name="logout_view"),
]