from typing import List
from django.apps import apps


def get_all_custom_models():
    excluded_apps = {'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'authtoken', 'uploads'}
    custom_models = []


    for model in apps.get_models():
        if model._meta.app_label not in excluded_apps:
            model_string = model.__name__
            custom_models.append(model_string)
            
    return custom_models