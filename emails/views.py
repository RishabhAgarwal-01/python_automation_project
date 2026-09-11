from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task


# Create your views here.

def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form  = email_form.save()  # Save the email to the database

            # send an email
            mail_subject = request.POST.get('subject')
            message =  request.POST.get('body')
            email_list = request.POST.get('email_list').split(',')  # Split the comma-separated emails into a list

            # access the selected email list 
            email_list = email_form.email_list  # Assuming email_list is a ManyToManyField in the EmailForm model

            # extract email addresses from the Subscribers model in the selected email list
            subscribers =  Subscriber.objects.filter(email_list=email_list)

            to_email =   [sub.email_address for sub in subscribers]

            if email_form.attachments:
                attachment = email_form.attachments.path
            else:
                attachment = None

            # handover task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)


            messages.success(request, 'Email being sent!')
            return redirect('send_email')  # Redirect to the same page or another page after sending
    else:
        email_form = EmailForm()


    context = {'email_form': email_form}
    return render(request, 'emails/send_email.html', context)
