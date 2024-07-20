import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from card_manager.models import Card, Purchase


class Command(BaseCommand):
    help = 'Generate 100 cards with random amounts of bonus points and purchases'

    def handle(self, *args, **kwargs):
        def random_past_date():
            return datetime.now() - timedelta(days=random.randint(0, 365))

        def random_decimal(min_value, max_value, decimal_places):
            return round(random.uniform(min_value, max_value), decimal_places)

        for _ in range(100):
            card = Card(
                amount=random_decimal(0.01, 100.99, 2)
            )
            card.save()

            num_purchases = random.randint(1, 10)
            purchases = []

            for _ in range(num_purchases):
                purchase_date = random_past_date()
                purchase = Purchase(
                    card=card,
                    purchase_date=purchase_date,
                    amount=random_decimal(1, 5000, 2)
                )
                purchases.append(purchase)

            Purchase.objects.bulk_create(purchases)

            if purchases:
                card.last_used = max(purchases, key=lambda p: p.purchase_date).purchase_date
                card.save()

        self.stdout.write(self.style.SUCCESS('Generated 100 cards with random purchases.'))

