from django.contrib import admin

# Register your models here.
from .models import Client, Order, Drug


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Client)
admin.site.register(Drug)
