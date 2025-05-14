from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Utilisateur personnalisé
class Utilisateur(AbstractUser):
    ROLES = (
        ('citoyen', 'Citoyen'),
        ('admin', 'Administrateur'),
        ('touriste', 'Touriste'),
    )
    email = models.EmailField(unique=True)
    numero_tel = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES, default='citoyen')
    est_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. Signalement
class Signalement(models.Model):
    TYPES = (
        ('Route', 'Route endommagée'),
        ('Electricite', 'Panne électrique'),
        ('Dechets', 'Déchets non collectés'),
    )
    STATUTS = (
        ('En attente', 'En attente'),
        ('Valide', 'Validé'),
        ('Resolue', 'Résolu'),
    )

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='signalements/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)  # Permet les valeurs NULL
    longitude = models.FloatField(null=True, blank=True)  # Permet les valeurs NULL
    type_probleme = models.CharField(max_length=20, choices=TYPES)
    statut = models.CharField(max_length=20, choices=STATUTS, default='En attente')
    date_signalement = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.titre} - {self.type_probleme}"


# 3. Vote
class Vote(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    signalement = models.ForeignKey(Signalement, on_delete=models.CASCADE)
    date_vote = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'signalement')


# 4. Condition Routière
class ConditionRoutiere(models.Model):
    signalement = models.ForeignKey(Signalement, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    etat = models.CharField(max_length=20, choices=(
        ('Bon', 'Bon'),
        ('Degrade', 'Dégradé'),
        ('Barre', 'Barré'),
    ))
    date_mise_a_jour = models.DateTimeField(auto_now=True)


# 5. Statistiques par zone
class StatistiqueZone(models.Model):
    zone_nom = models.CharField(max_length=100)
    nombre_signalements = models.IntegerField(default=0)
    date_calcul = models.DateField(auto_now_add=True)


# 6. API Token pour accès externe
class APIToken(models.Model):
    organisation_nom = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
    date_expiration = models.DateTimeField()
    actif = models.BooleanField(default=True)


# 7. Historique d’envoi de mails
class EmailNotification(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_email = models.CharField(max_length=30)  # Ex: inscription, alerte
    sujet = models.CharField(max_length=255)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)


# 8. Token de vérification (activation, reset password, etc.)
class TokenVerification(models.Model):
    TYPES = (
        ('activation', 'Activation de compte'),
        ('reset_password', 'Réinitialisation mot de passe'),
    )

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPES)
    expiration = models.DateTimeField()
    est_utilise = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.email} - {self.type}"


# 9. Notification
class Notification(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    signalement = models.ForeignKey('Signalement', on_delete=models.CASCADE, null=True, blank=True)
    lu = models.BooleanField(default=False)  # Indique si la notification a été lue
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.utilisateur.username} - {self.message[:20]}"
