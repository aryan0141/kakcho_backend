from django.db import models
from django.contrib.auth.models import User
import jsonfield
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CSVFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_path = models.FileField(blank=False, upload_to="csvfiles/")
    all_apps = ArrayField(jsonfield.JSONField(null=True), default=list)
    free_apps = ArrayField(jsonfield.JSONField(null=True), default=list)
    paid_apps = ArrayField(jsonfield.JSONField(null=True), default=list)
    everyone  = ArrayField(jsonfield.JSONField(null=True), default=list)
    teen = ArrayField(jsonfield.JSONField(null=True), default=list)
    mature_17_plus = ArrayField(jsonfield.JSONField(null=True), default=list)
    everyone_10_plus = ArrayField(jsonfield.JSONField(null=True), default=list)
    adults_18_plus = ArrayField(jsonfield.JSONField(null=True), default=list)
    unrated = ArrayField(jsonfield.JSONField(null=True), default=list)

    def __str__(self):
        return self.csv_path.name
    def path(self):
        return self.url
    


   