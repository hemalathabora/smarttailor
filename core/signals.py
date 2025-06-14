from django.db.models.signals import post_migrate
from .models import Fabric, Tailor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name == 'core':
        # Add default Fabrics
        if Fabric.objects.count() == 0:
            Fabric.objects.create(name="Cotton", quantity_in_meters=100, price_per_meter=150)
            Fabric.objects.create(name="Silk", quantity_in_meters=50, price_per_meter=300)
            Fabric.objects.create(name="Linen", quantity_in_meters=70, price_per_meter=200)
            print("✅ Default fabrics added")

        # Add default Tailors
        if Tailor.objects.count() == 0:
            Tailor.objects.create(
                name="Ravi Kumar",
                shop_name="Ravi’s Tailors",
                phone="9876543210",
                email="ravi@example.com"
            )
            Tailor.objects.create(
                name="Sita Devi",
                shop_name="Stitch Queen",
                phone="9876543211",
                email="sita@example.com"
            )
            print("✅ Default tailors added")
