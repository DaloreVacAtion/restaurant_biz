from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import MyUserCreationForm
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Введите номер телефона пользователя, а также Имя по желанию. Пароль устанавливается опционально, если"
                " Вы хотите задать суперпользователя."
            ),
            'fields': ('username', 'name'),
        }),
        ('Password', {
            'description': "Опционально. Вы можете ввести Пароль пользователя, чтобы создать суперпользователя",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    list_display = ['username', 'name', 'is_superuser']
    ordering = ['username']
    search_fields = ['username']
    search_help_text = 'Телефон пользователя'
    fieldsets = (
        (_('Личная информация'), {'fields': ('username', 'name')}),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions',
                       ),
        }),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
