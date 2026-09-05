from django.contrib import admin
from .models import Student, Customer


# Register your models here.
admin.site.register(Student)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'country')