from django.shortcuts import render
from rest_framework import generics, status, views
from api.models import User, PlayerProfile, Team, Match, MatchRegistration, SportActivity, Message, Notification
from api.serializers import RegisterSerializer, UserSerializer, PlayerProfileSerializer, TeamSerializer, MatchSerializer, MatchRegistrationSerializer, SportActivitySerializer, MessageSerializer, MessageDetailSerializer, NotificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .permissions import IsOrganisatorOrAdmin, IsOwnerOrAdmin, MessagePermission
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerProfileListView(generics.ListCreateAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsAuthenticated]


class PlayerProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    permission_classes = [IsAuthenticated]


class TeamListView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchListView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchRequestsListView(generics.ListAPIView):
    serializer_class = MatchRegistrationSerializer
    permission_classes = [IsAuthenticated, IsOrganisatorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            teams_owned_by_organisator = Team.objects.filter(user=user)
            matches_of_organisator = Match.objects.filter(
                team__in=teams_owned_by_organisator)
            # Retourner les demandes pour ces matchs
            return MatchRegistration.objects.filter(match__in=matches_of_organisator)
        else:
            # Si l'utilisateur n'est pas authentifié, ne retourner aucune demande
            return MatchRegistration.objects.none()


class OrganisatorMatchesListView(ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'team_profile'):
            # Si l'utilisateur est un organisateur, filtrer les matchs par ses équipes
            teams = Team.objects.filter(user=user)
            return Match.objects.filter(team__in=teams)
        else:
            # Si l'utilisateur n'est pas un organisateur, ne retourner aucun match
            return Match.objects.none()


class MatchRegistrationCreateView(generics.ListCreateAPIView):
    queryset = MatchRegistration.objects.all()
    serializer_class = MatchRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class SportActivityListView(generics.ListCreateAPIView):
    queryset = SportActivity.objects.all()
    serializer_class = SportActivitySerializer
    permission_classes = [IsAuthenticated]


class SportActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SportActivity.objects.all()
    serializer_class = SportActivitySerializer
    permission_classes = [IsOwnerOrAdmin]


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
    permission_classes = [MessagePermission]


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user, read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response(user_data)


class LoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        # Vérifiez si les champs username et password sont présents
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # Construisez la réponse
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'location': user.location,
            }
            response_data['user'] = user_data

            return Response(response_data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsOrganisatorOrAdmin])
def accept_match_request(request, pk):
    try:
        match_request = MatchRegistration.objects.get(pk=pk)
        if request.user != match_request.match.team.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        match_request.status = 'confirmed'
        match_request.save()
        return Response({'status': 'accepted'})
    except MatchRegistration.DoesNotExist:
        return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsOrganisatorOrAdmin])
def reject_match_request(request, pk):
    try:
        match_request = MatchRegistration.objects.get(pk=pk)
        if request.user != match_request.match.team.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        match_request.status = 'refused'
        match_request.save()
        return Response({'status': 'rejected'})
    except MatchRegistration.DoesNotExist:
        return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserMatchRequestsView(generics.ListAPIView):
    serializer_class = MatchRegistrationSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Cette vue retourne une liste des demandes pour rejoindre les matchs
        pour l'utilisateur connecté.
        """
        user = self.request.user

        return MatchRegistration.objects.filter(user=user)


@api_view(['DELETE'])
def clear_user_requests(request):
    """
    Efface toutes les demandes de l'utilisateur actuel pour rejoindre des matchs.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Authentification requise"}, status=status.HTTP_401_UNAUTHORIZED)

    MatchRegistration.objects.filter(user=request.user).delete()
    return Response({"message": "Vos demandes ont été supprimées."}, status=status.HTTP_204_NO_CONTENT)


class MatchSearchView(APIView):
    """
    API view pour rechercher des matchs par emplacement géographique et sport.
    """

    def get(self, request, sport, location):
        matches = Match.objects.filter(
            sport__iexact=sport, location__icontains=location)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
