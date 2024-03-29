from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = (
        ('player', _('Player')),
        ('organisator', _('Organisator')),
        ('admin', _('Admin'))
    )
    user_type = models.CharField(
        max_length=11, choices=TYPE_CHOICES, default='player', verbose_name=_("User Type"))
    location = models.CharField(
        max_length=255, blank=True, verbose_name=_("Location"))

    image = models.ImageField(upload_to='profile_images', blank=True)


class PlayerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='player_profile', verbose_name=_("User"))
    age = models.PositiveIntegerField(verbose_name=_("Age"))
    gender = models.CharField(max_length=10, verbose_name=_("Gender"))
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Weight"))
    favorite_sports = models.CharField(
        max_length=255, verbose_name=_("Favorite Sports"))
    skill_level = models.CharField(
        max_length=255, verbose_name=_("Skill Level"))

    def __str__(self):
        return self.user.username


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='team_profile', verbose_name=_("User"))
    team_name = models.CharField(max_length=255, verbose_name=_("Team Name"))
    sport = models.CharField(max_length=255, verbose_name=_("Sport"))
    skill_level = models.CharField(
        max_length=255, verbose_name=_("Skill Level"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))

    def __str__(self):
        return self.team_name


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='matches', verbose_name=_("Team"))
    date_time = models.DateTimeField(verbose_name=_("Date and Time"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    sport = models.CharField(max_length=255, verbose_name=_("Sport"))
    required_skill_level = models.CharField(
        max_length=255, verbose_name=_("Required Skill Level"))
    players_needed = models.PositiveIntegerField(
        verbose_name=_("Players Needed"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    def __str__(self):
        return f"{self.sport} on {self.date_time}"


class MatchRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Match"))
    player = models.ForeignKey(
        PlayerProfile, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Player"))
    status = models.CharField(
        max_length=255, default='pending', verbose_name=_("Status"))
    # Suggestions for status values: 'confirmed', 'pending', 'refused'

    def __str__(self):
        return f"{self.player.user.username} - {self.match.sport} on {self.match.date_time}"


class SportActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        PlayerProfile, on_delete=models.CASCADE, related_name='activities', verbose_name=_("Player"))
    sport = models.CharField(max_length=255, verbose_name=_("Sport"))
    duration = models.PositiveIntegerField(
        verbose_name=_("Duration in Minutes"))
    calories_burned = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_("Calories Burned"))

    def __str__(self):
        return f"{self.sport} by {self.player.user.username}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_("Sender"))
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages', verbose_name=_("Recipient"))
    content = models.TextField(verbose_name=_("Content"))
    sent_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Sent At"))
    read = models.BooleanField(default=False, verbose_name=_("Read"))

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('join_request', 'Join Request'),
        ('request_accepted', 'Request Accepted'),
        ('request_refused', 'Request Refused'),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.username}: {self.message}"
