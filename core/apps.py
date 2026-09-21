
from django.apps import AppConfig
from django.contrib.auth.apps import AuthConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Gestão Ambiental'  # Nome que aparecerá no menu do Admin



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Gestão Ambiental'

# Traduz o nome da secção de Autenticação no Admin
AuthConfig.verbose_name = "Autenticação e Autorização"