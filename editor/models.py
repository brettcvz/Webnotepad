from django.db import models

# Create your models here.

class Document(models.Model):
	#A hash to uniquely identify the doc
	docid = models.CharField(max_length=32, primary_key=True)
	filename = models.CharField(max_length=64, blank=True,null=True)
	contents = models.TextField()

	created = models.DateTimeField(auto_now_add=True)
	saveback_url = models.CharField(max_length=256, blank=True, null=True)
	saveback_id = models.CharField(max_length=128, blank=True, null=True)
