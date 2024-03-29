from django.contrib import admin
from api.models import User, PlayerProfile, Team, Match, MatchRegistration, SportActivity, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'weight',
                    'favorite_sports', 'skill_level')
    list_filter = ('gender', 'favorite_sports', 'skill_level')
    search_fields = ('user__username', 'user__email',
                     'user__first_name', 'user__last_name')
    ordering = ('user__username',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team_name', 'sport',
                    'skill_level', 'description', 'location')
    list_filter = ('sport', 'skill_level')
    search_fields = ('user__username', 'user__email',
                     'user__first_name', 'user__last_name')
    ordering = ('user__username',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'sport', 'date_time', 'location')
    list_filter = ('sport', 'date_time')
    search_fields = ('team__team_name', 'team__user__username',
                     'team__user__email', 'team__user__first_name', 'team__user__last_name')
    ordering = ('team__team_name',)


class MatchRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'player', 'status')
    list_filter = ('status',)
    search_fields = ('match__sport', 'player__user__username', 'player__user__email',
                     'player__user__first_name', 'player__user__last_name')
    ordering = ('match__sport',)


class SportActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'sport', 'duration', 'calories_burned')
    list_filter = ('sport',)
    search_fields = ('player__user__username', 'player__user__email',
                     'player__user__first_name', 'player__user__last_name')
    ordering = ('sport',)


class MessageAdmin(admin.ModelAdmin):

    list_display = ('id', 'sender', 'recipient', 'content', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('sender__username', 'sender__email',
                     'recipient__username', 'recipient__email')
    ordering = ('sent_at',)


admin.site.register(User, UserAdmin)
admin.site.register(PlayerProfile, PlayerProfileAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchRegistration, MatchRegistrationAdmin)
admin.site.register(SportActivity, SportActivityAdmin)
admin.site.register(Message, MessageAdmin)
