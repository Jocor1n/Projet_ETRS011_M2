from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("json_test", views.json_test, name="json_test"),
    path("add_machine", views.add_machine, name="add_machine"),
    path("add_user", views.add_user, name="add_user"),
    path('machines', views.liste_machines, name='liste_machines'),
    path('users', views.liste_users, name='liste_users'),
    path('edit_machine/<int:machine_id>/', views.edit_machine, name='edit_machine'),
    path('delete_machine/<int:machine_id>/', views.delete_machine, name='delete_machine'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('donnees_machines', views.donnees_machines, name='donnees_machines'),
]