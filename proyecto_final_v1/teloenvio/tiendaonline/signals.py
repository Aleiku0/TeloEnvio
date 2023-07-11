from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tiendaonline.models import Carrito


@receiver(post_save, sender=User)
def create_carrito(sender, instance, created, **kwargs):
    if created:
        Carrito.objects.create(usuario=instance)