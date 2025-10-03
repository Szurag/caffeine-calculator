from django.core.management.base import BaseCommand
from products.models import Product
from django.contrib.auth.models import User
from media.models import Media
from pathlib import Path


class Command(BaseCommand):
    help = "Seed products with initial data"

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.WARNING("No superuser found. Please create one."))
            return

        BASE_DIR = Path(__file__).resolve().parent.parent  # goes to products/
        images_dir = BASE_DIR / "seed_images"

        products_data = [
            {"name": "Red Bull Classic", "caffeine_mg": 80, "image": "red_bull.jpg"},
            {"name": "Monster Classic", "caffeine_mg": 160, "image": "monster.jpg"},
            {"name": "Dzik Classic", "caffeine_mg": 200, "image": "dzik_classic.jpg"},
        ]

        for data in products_data:
            media = None
            if data["image"]:
                path = images_dir / data["image"]
                if path.exists():
                    with path.open("rb") as f:
                        from django.core.files import File
                        media = Media.objects.create(file=File(f, name=path.name), uploaded_by=admin_user)
                else:
                    self.stdout.write(self.style.WARNING(f"Image not found: {data['image']}"))

            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "caffeine_mg": data["caffeine_mg"],
                    "is_global": True,
                    "created_by": admin_user,
                    "photo": media
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(self.style.NOTICE(f"Product already exists: {product.name}"))

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
