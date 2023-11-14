from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_machine", views.add_machine, name="add_machine"),
    path("add_user", views.add_user, name="add_user"),
    path("add_oid", views.add_oid, name="add_oid"),
    path("add_graphique", views.add_graphique, name="add_graphique"),
    path('machines', views.liste_machines, name='liste_machines'),
    path('oids', views.liste_oids, name='liste_oids'),
    path('graphiques', views.liste_graphiques, name='liste_graphiques'),
    path('users', views.liste_users, name='liste_users'),
    path('logs', views.logs, name='logs'),
    path('edit_machine/<int:machine_id>/', views.edit_machine, name='edit_machine'),
    path('delete_machine/<int:machine_id>/', views.delete_machine, name='delete_machine'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('edit_oid/<int:oid_id>/', views.edit_oid, name='edit_oid'),
    path('edit_graphique/<int:graphique_id>/', views.edit_graphique, name='edit_graphique'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_oid/<int:oid_id>/', views.delete_oid, name='delete_oid'),
    path('delete_graphique/<int:graphique_id>/', views.delete_graphique, name='delete_graphique'),
    path('donnees_machines', views.donnees_machines, name='donnees_machines'),
]