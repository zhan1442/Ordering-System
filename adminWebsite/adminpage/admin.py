from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .models import Order, Drug, Wish_List, Product, Shopping_Cart


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time', 'modified_time',)


admin.site.register(Order, OrderAdmin)

admin.site.register(Shopping_Cart)
admin.site.register(Drug)
admin.site.register(Wish_List)
admin.site.register(Product)

admin.site.site_title = "Purdue Pharmacy Ordering System UserManagement"
admin.site.site_header = "Purdue Pharmacy Ordering System UserManagement"


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# class UserCreationFormExtended(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationFormExtended, self).__init__(*args, **kwargs)
#         self.fields[Profile.user_type] = forms.CharField(label=_("user_type"))


class CustomUserAdmin(UserAdmin):
    # UserAdmin.add_form = UserCreationFormExtended
    # UserAdmin.add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('user_type', 'username', 'password1', 'password2',)
    #     }),
    # )

    # restrictions for staff users...
    def queryset(self, request):
        qs = admin.ModelAdmin.queryset(self, request)
        if request.user.is_superuser:
            return qs
        # Only allow viewing/editing users who are not superusers
        return qs.filter(is_superuser=False)

    def get_readonly_fields(self, request, obj=None):
        # Deny editing groups, permissions and the superuser status
        return () if request.user.is_superuser else ('is_superuser',
                                                     'is_staff',
                                                     'is_active',
                                                     'groups',
                                                     )

    # restrict permission list...
    def get_form(self, request, obj=None, **kwargs):
        # Get form from original UserAdmin.
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        if 'user_permissions' in form.base_fields:
            permissions = form.base_fields['user_permissions']
            permissions.queryset = permissions.queryset.filter(content_type__model__in=['user'])
        return form

    # inline the profile field...
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
