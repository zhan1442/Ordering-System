from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    USER_TYPE_CHOICES = (
        ('Vendor', 'Customer'),
        ('Administrator', 'Administrator')
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='Vendor')

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# class Client(models.Model):
#     client_name = models.CharField(max_length=1000,help_text="i.e. david")
#     phone_number= models.IntegerField(help_text="i.e. 7651111111")
#     contact_email= models.CharField(max_length=200,help_text="i.e. david@purdue.edu")
#     #login = models.ForeignKey(Login, blank=True, null=True)
#     def __str__(self):
#         return self.client_name
#     def __unicode__(self):
#         return self.client_name

class Order(models.Model):
    def __str__(self):
        return '%09d' % self.pk

    def __unicode__(self):
        return '%09d' % self.pk

    def get_order_number(self):  # for future generating order number
        return '%09d' % self.pk

        # associates to one Client table line

    client_obj = models.ForeignKey(User, blank=True, null=True)

    # order info
    # order_number = get_order_number()  # for future generating order number
    ORDER_STATUS_CHOICES = (
        ('new', 'Products Ordered'),
        ('filled', 'Orders Filled'),
        ('remove', 'Taken Out of Inventory'),
        ('ready', 'Order Ready for Pick Up'),
        ('billing', 'Order Delivered'),
        ('complete', 'Billing Complete')
    )
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='new')
    comment = models.TextField(max_length=1000, blank=True, help_text="If you have any comments, please add it here")
    date_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Drug(models.Model):  # This is the Drug table for detailed drug info

    # class functions
    def __str__(self):
        return self.brand + " - " + self.name

    def __unicode__(self):
        return self.brand + " - " + self.name

    # associate to one Order table line
    order_obj = models.ForeignKey(Order, blank=True, null=True)

    # drug info
    brand = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    strength = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)


class Product(models.Model):
    brand = models.CharField(max_length=200, help_text="Drug brand of the product")
    name = models.CharField(max_length=200, help_text="Drug name of the product")
    strength = models.CharField(max_length=50, help_text="Product stregnth of the pack: mg, ml etc.")
    price = models.FloatField(help_text="Price of the product in dollar: xx.xx")
    CIN = models.IntegerField(help_text="CIN number of the product with digits")
    description = models.TextField(max_length=2000, blank=True,
                                   null=True, help_text="You can add product description here")
    date_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    # class functions
    def __str__(self):
        return self.brand + " - " + self.name + " - " + self.strength

    def __unicode__(self):
        return self.brand + " - " + self.name + " - " + self.strength


class Wish_List(models.Model):
    client_obj_wish = models.ForeignKey(User, blank=True, null=True)
    wish_drug_name = models.CharField(max_length=200)
    wish_drug_brand = models.CharField(max_length=200)
    wish_drug_strength = models.CharField(max_length=50)
    wish_drug_price = models.FloatField(max_length=50)


class Shopping_Cart(models.Model):
    client_obj_shopping = models.ForeignKey(User)
    shopping_drug_brand = models.CharField(max_length=200)
    shopping_drug_name = models.CharField(max_length=200)
    shopping_strength = models.FloatField(max_length=50)
    shopping_quantity = models.IntegerField(default=0)


class Wish_To_Order(models.Model):
    client_obj_WTO = models.ForeignKey(User, blank=True, null=True)
    WTO_drug_name = models.CharField(max_length=200)
    WTO_drug_brand = models.CharField(max_length=200)
    WTO_drug_strength = models.CharField(max_length=50)
