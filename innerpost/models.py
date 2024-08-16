from django.db import models


class Mail(models.Model):


    login = models.CharField(max_length=100)
    password = models.TextField()
    last_uid = models.PositiveIntegerField(null=True, blank=True, default=None) 


    def __str__(self):
        return self.login





class Letter(models.Model):


    subject = models.CharField(max_length=100)
    posting_time = models.DateTimeField()
    receiving_time = models.DateTimeField()
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments/')
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE)

    def __str__(self):
        return f"Letter {self.pk}: {self.mail} {str(self.posting_time)[:10]}"