# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.apps import apps
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import MatchRegistration, Notification


# @receiver(post_save, sender=MatchRegistration)
# def match_registration_notification(sender, instance, created, **kwargs):
#     if created:
#         # Notification pour l'organisateur pour une nouvelle demande
#         Notification.objects.create(
#             recipient=instance.match.team.user,
#             message=f"{instance.player.user.username} souhaite rejoindre {instance.match.team.team_name}.",
#             type='join_request'
#         )
#     else:
#         # Notification pour le joueur quand sa demande est mise à jour
#         notif_type = 'request_accepted' if instance.status == 'confirmed' else 'request_refused'
#         Notification.objects.create(
#             recipient=instance.player.user,
#             message=f"Votre demande pour {instance.match.team.team_name} a été {instance.status}.",
#             type=notif_type
#         )
