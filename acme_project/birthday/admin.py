from django.contrib import admin

from .models import Birthday


@admin.register(Birthday)
class Birthday(admin.ModelAdmin):
    list_display: tuple = (
        'first_name',
        'last_name',
        'birthday'
    )
