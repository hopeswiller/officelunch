from django.contrib import admin

from .models import Product, Setting, Employs,Order,Feedback

# Register your models here.
admin.site.register(Product)
admin.site.register(Employs)
admin.site.register(Order)
admin.site.register(Feedback)

# Register your models here.
#delete admin
#from django.contrib.auth.models import User
#User.objects.get(username="NameHere", is_superuser=True).delete()
#
#You should replace the name of the superuser you created with NameHere in the last command.




@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    # You really shouldn't add random settings
    def has_add_permission(self, request):
        return False

    # Deleting a setting seems odd...
    def has_delete_permission(self, *args, **kwargs):
        return False
