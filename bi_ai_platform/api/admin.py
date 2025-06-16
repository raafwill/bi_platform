from django.contrib import admin
from django.contrib.auth.models import Group
from .models import DatabaseConnection, TabelaSemantica

admin.site.register(DatabaseConnection)
admin.site.register(TabelaSemantica)
