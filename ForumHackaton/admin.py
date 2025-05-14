from django.contrib import admin
from .models import Utilisateur, Signalement, Vote, ConditionRoutiere, StatistiqueZone, APIToken, EmailNotification, TokenVerification

# 1. Configuration pour le modèle Utilisateur
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'numero_tel', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'numero_tel')

# 2. Configuration pour le modèle Signalement
@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_probleme', 'statut', 'date_signalement', 'utilisateur')
    list_filter = ('type_probleme', 'statut', 'date_signalement')
    search_fields = ('titre', 'description', 'utilisateur__username')

# 3. Configuration pour le modèle Vote
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'signalement', 'date_vote')
    list_filter = ('date_vote',)
    search_fields = ('utilisateur__username', 'signalement__titre')

# 4. Configuration pour le modèle Condition Routière
@admin.register(ConditionRoutiere)
class ConditionRoutiereAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'etat', 'date_mise_a_jour')
    list_filter = ('etat', 'date_mise_a_jour')
    search_fields = ('latitude', 'longitude')

# 5. Configuration pour le modèle StatistiqueZone
@admin.register(StatistiqueZone)
class StatistiqueZoneAdmin(admin.ModelAdmin):
    list_display = ('zone_nom', 'nombre_signalements', 'date_calcul')
    list_filter = ('date_calcul',)
    search_fields = ('zone_nom',)

# 6. Configuration pour le modèle APIToken
@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('organisation_nom', 'token', 'date_expiration', 'actif')
    list_filter = ('actif', 'date_expiration')
    search_fields = ('organisation_nom', 'token')

# 7. Configuration pour le modèle EmailNotification
@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_email', 'sujet', 'date_envoi')
    list_filter = ('type_email', 'date_envoi')
    search_fields = ('utilisateur__username', 'sujet')

# 8. Configuration pour le modèle TokenVerification
@admin.register(TokenVerification)
class TokenVerificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type', 'expiration', 'est_utilise')
    list_filter = ('type', 'est_utilise', 'expiration')
    search_fields = ('utilisateur__username', 'token')
