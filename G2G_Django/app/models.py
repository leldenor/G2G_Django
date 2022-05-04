"""
Definition of models.
"""

from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


# Create your models here.

CATEGORY_CHOICES = (
    ('D', 'Drink'),
    ('F', 'Food')
)

CONSUMABLE_CHOICES = (
    ('BK', 'Baked'),
    ('CF', 'Coffee'),
    ('JC', 'Juice'),
    ('FR', 'Fruit'),
    ('TE', 'Tea')
)

SIZE_CHOICES = (
    ('SM', 'Small'),
    ('MD', 'Medium'),
    ('LG', 'Large'),
    ('DF', 'Default')
)

DRINK_CHOICES = (
    ('C', 'Coffee'),
    ('J', 'Juice'),
    ('T', 'Tea')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)

    def __str__(self):
        return self.title
    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)