from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import (
    UserListView, UserDetailView,
    PlayerProfileListView, PlayerProfileDetailView,
    TeamListView, TeamDetailView,
    MatchListView, MatchDetailView,
    MatchRegistrationListView, MatchRegistrationDetailView,
    SportActivityListView, SportActivityDetailView,
    MessageListView, MessageDetailView,
    RegisterView, LoginView, NotificationListView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="YallaShoot API",
        default_version='v1',
        description="YallaShoot est une API pour la gestion des matchs de football. Elle permet aux utilisateurs de s'inscrire, de créer et de gérer des équipes, de planifier des matchs, de s'inscrire à des matchs existants et de suivre leurs activités sportives. Elle offre également une fonctionnalité de messagerie pour permettre aux utilisateurs de communiquer entre eux.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('accounts/', include('allauth.urls')),

    # Authentification JWT-------------------------------------------------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inscription et Connexion-------------------------------------------------------------
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    # Utilisateurs-------------------------------------------------------------
    path('api/users/', UserListView.as_view()),
    path('api/users/<uuid:pk>/', UserDetailView.as_view()),

    # Profils de Joueurs-------------------------------------------------------------
    path('api/player-profiles/', PlayerProfileListView.as_view()),
    path('api/player-profiles/<uuid:pk>/', PlayerProfileDetailView.as_view()),

    # Équipes-------------------------------------------------------------
    path('api/teams/', TeamListView.as_view(), name='team-list'),
    path('api/teams/<uuid:pk>/', TeamDetailView.as_view()),

    # Matchs-------------------------------------------------------------
    path('api/matches/', MatchListView.as_view()),
    path('api/matches/<uuid:pk>/', MatchDetailView.as_view()),

    # Inscriptions aux Matchs-------------------------------------------------------------
    path('api/match-registrations/', MatchRegistrationListView.as_view()),
    path('api/match-registrations/<uuid:pk>/',
         MatchRegistrationDetailView.as_view()),

    # Activités Sportives-------------------------------------------------------------
    path('api/sport-activities/', SportActivityListView.as_view()),
    path('api/sport-activities/<uuid:pk>/', SportActivityDetailView.as_view()),

    # notifications-------------------------------------------------------------
    path('api/notifications/', NotificationListView.as_view(),
         name='notification-list'),


    # Messages-------------------------------------------------------------
    path('api/messages/', MessageListView.as_view()),
    path('api/messages/<uuid:pk>/', MessageDetailView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
