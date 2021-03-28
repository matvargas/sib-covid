from django.urls import path
from covid_data_viewer import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("supported_datasets", views.supported_datasets, name="supported_datasets"),
    path("about_data", views.about_data, name="about_data"),
    path("view/notificacoes", views.view_notifications, name="view_notifications"),
    path("view/casos", views.view_cases, name="view_cases"),
    path("view/evolucao", views.view_evolution, name="view_evolution"),
    path("contact", views.contact, name="contact"),

]