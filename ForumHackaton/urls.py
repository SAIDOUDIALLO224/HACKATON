from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil_public, name='accueil_public'),  
    path('about/', views.about, name='about'),   # Page "À propos"
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    path('mes_signalements/', views.mes_signalements, name='mes_signalements'),  
    path('nouveau_signalement/', views.nouveau_signalement, name='nouveau_signalement'),  
    path('map/', views.map_view, name='map'),
    path('profil/', views.profil, name='profil'), 
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/lu/', views.marquer_comme_lu, name='marquer_comme_lu'),
    path('api/carte_data/', views.carte_data, name='carte_data'),
]