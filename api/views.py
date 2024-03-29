from django.shortcuts import render
from rest_framework import generics, status, views
from api.models import User, PlayerProfile, Team, Match, MatchRegistration, SportActivity, Message
from api.serializers import RegisterSerializer, UserSerializer, PlayerProfileSerializer, TeamSerializer, MatchSerializer, MatchRegistrationSerializer, SportActivitySerializer, MessageSerializer, MessageDetailSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerProfileListView(generics.ListCreateAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer


class PlayerProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer


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


class MatchRegistrationListView(generics.ListCreateAPIView):
    queryset = MatchRegistration.objects.all()
    serializer_class = MatchRegistrationSerializer


class MatchRegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MatchRegistration.objects.all()
    serializer_class = MatchRegistrationSerializer


class SportActivityListView(generics.ListCreateAPIView):
    queryset = SportActivity.objects.all()
    serializer_class = SportActivitySerializer


class SportActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SportActivity.objects.all()
    serializer_class = SportActivitySerializer


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer


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
