from django.contrib import admin

from .models import Birthday, Tag


class BirthdayInline(admin.StackedInline):
    model = Birthday
    extra = 0
    fields = {'first_name', 'last_name', 'birthday', 'image'}


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)


class BirthdayAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'birthday',
        'image',
    )
    filter_horizontal = ('tags',)


admin.site.register(Birthday, BirthdayAdmin)
admin.site.register(Tag, TagAdmin)
