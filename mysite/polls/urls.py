from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register', views.register, name='register'),
    path('login', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('create', views.create, name='create')
]