from django.db import models

class List(models.Model):
    email_list = models.CharField(max_length=255)

    def __str__(self):
        return self.email_list



class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='subscribers')
    email_address = models.EmailField(max_length=255)
    

    def __str__(self):
        return self.email_address



class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    attachments = models.FileField(upload_to='email_attachments/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
