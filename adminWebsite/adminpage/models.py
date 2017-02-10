from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Client(models.Model):  # This Client model only used for demonstration and subject to change!

    # class functions
    def __str__(self):
        return self.client_name

    def __unicode__(self):
        return self.client_name

    client_name = models.CharField(max_length=100, default="i.e. david")
    phone_number = models.IntegerField(default="i.e. 7651111111")
    contact_email = models.CharField(max_length=100, default="i.e. david@purdue.edu")


class Order(models.Model):  # This is the Order table for all order info

    # class functions
    def __str__(self):
        return '%09d' % self.pk

    def __unicode__(self):
        return '%09d' % self.pk

    # def get_order_number(self):  # for future generating order number
    #     return '%09d' % self.pk

    # associates to one Client table line
    client_obj = models.ForeignKey(Client, blank=True, null=True)

    # order info
    # order_number = get_order_number()  # for future generating order number
    ORDER_STATUS_CHOICES = (
        ('new', 'Products Ordered'),
        ('filled', 'Order Filled'),
        ('remove', 'Taken Out of Inventory'),
        ('ready', 'Order Ready for Pick Up'),
        ('billing', 'Order Delivered'),
        ('complete', 'Billing Complete')
    )
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='new')
    comment = models.TextField(max_length=1000, help_text="Any additional information")
    date_time = models.DateTimeField(auto_now_add=True)
    # doctor_name = models.CharField(max_length=1000, default="i.e. Paul1027")
    # doctor_email = models.CharField(max_length=1000, default="i.e. Paul1027@purdue.edu")


class Drug(models.Model):  # This is the Drug table for detailed drug info

    # class functions
    def __str__(self):
        return self.brand + " - " + self.name

    def __unicode__(self):
        return self.brand + " - " + self.name

    # associate to one Order table line
    order_obj = models.ForeignKey(Order, blank=True, null=True)

    # drug info
    brand = models.CharField(max_length=200, help_text="i.e. Decodron")
    name = models.CharField(max_length=200, help_text="i.e. Amoxicillin")
    strength = models.CharField(max_length=50, help_text="i.e. 500ml")
    quantity = models.IntegerField(default=0)
