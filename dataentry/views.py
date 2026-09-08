import csv
import io
from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib import messages
from dataentry.utils import get_all_custom_models, check_csv_errors
from uploads.models import Upload
from django.conf import settings
from .tasks import export_data_task, import_data_task
from django.core.management import call_command


def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        
        # The frontend sends a value like "app_label.ModelName"
        model_name = request.POST.get('model_name')

        #store this file inside the upload model
        upload =  Upload.objects.create(file=file_path, model_name=model_name)

        # construct the full path
        relative_path = str(upload.file.url)
        base_url =  str(settings.BASE_DIR)
        file_path =  base_url + relative_path

        # check for the csv error
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # handle the import data task here handled by celery task in tasks.py
        import_data_task.delay(file_path,model_name)


        # show message to the user
        messages.success(request, "Your data is being imported, you will be notified once it is done.")
        return redirect('import_data')

    else:
        # Only handle GET requests here
        all_models = get_all_custom_models()
        context = {
            'model_list': all_models
        }
        return render(request, 'dataentry/importdata.html', context)




def export_data(request):

    if request.method == "POST":
        model_name = request.POST.get('model_name')

        # handle the export data task here handled by celery task in tasks.py
        export_data_task.delay(model_name)
        # show message to the user
        messages.success(request, "Your data is being exported, you will be notified once it is done.")
        return redirect('export_data')
    
    else:
        # Only handle GET requests here
        all_models = get_all_custom_models()
        context = {
            'model_list': all_models
        }
    
    return render(request,'dataentry/exportdata.html', context)