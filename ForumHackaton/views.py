from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Utilisateur, Notification, Signalement

def accueil_public(request):
    return render(request, 'user/pagPublic.html')

def inscription(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        numero_tel = request.POST['numero_tel']
        password = request.POST['password']
        role = request.POST['role']

        if Utilisateur.objects.filter(email=email).exists():
            return render(request, 'user/inscription.html', {'error': 'Cet email est déjà utilisé.'})

        user = Utilisateur.objects.create_user(
            username=username,
            email=email,
            numero_tel=numero_tel,
            password=password,
            role=role
        )
        login(request, user)
        return redirect('tableau_de_bord')

    return render(request, 'user/inscription.html')

def connexion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('tableau_de_bord')
        else:
            return render(request, 'user/connexion.html', {'error': 'Email ou mot de passe incorrect.'})

    return render(request, 'user/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def tableau_de_bord(request):
    return render(request, 'user/tableau_de_bord.html', {'user': request.user})
    
@login_required
def mes_signalements(request):
    signalements = Signalement.objects.filter(utilisateur=request.user)
    return render(request, 'user/mes_signalements.html', {'signalements': signalements})
    
@login_required
def nouveau_signalement(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        type_probleme = request.POST.get('type_probleme')
        latitude = request.POST.get('latitude')  # Récupérer la latitude
        longitude = request.POST.get('longitude')  # Récupérer la longitude

        # Créer le signalement
        Signalement.objects.create(
            utilisateur=request.user,
            titre=titre,
            description=description,
            type_probleme=type_probleme,
            statut='En attente',
            latitude=latitude,
            longitude=longitude
        )

        return redirect('mes_signalements')

    return render(request, 'user/nouveau_signalement.html')

def about(request):
    return render(request, 'user/Apropos.html')

@login_required
def map_view(request):
    return render(request, 'user/map.html')

@login_required
def profil(request):
    return render(request, 'user/profil.html', {'user': request.user})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    return render(request, 'user/notifications.html', {'notifications': notifications})

@login_required
def marquer_comme_lu(request, notification_id):
    notification = Notification.objects.get(id=notification_id, utilisateur=request.user)
    notification.lu = True
    notification.save()
    return redirect('notifications')

## Vue pour la carte
def carte_data(request):
    signalements = Signalement.objects.all()
    features = []

    for signalement in signalements:
        feature = {
            "type": "Feature",
            "properties": {
                "id": signalement.id,
                "category": signalement.category,
                "description": signalement.description,
                "status": signalement.status,
                "reported_by": signalement.reported_by,
                "date_reported": signalement.date_reported.isoformat(),
                "admin_reviewed": signalement.admin_reviewed,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [signalement.longitude, signalement.latitude],
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(geojson)