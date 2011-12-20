from django.db import models

class Post(models.Model):
    titel = models.CharField(max_length=200)
    date = models.DateTimeField('Erstellungsdatum')
    content = models.TextField("Inhalt", blank=True)
    
class Comment(models.Model):
	post = models.ForeignKey(Post)
	user = models.CharField(max_length=30)
	mail = models.CharField(max_length=50)
	content = models.TextField("Inhalt", blank=True)
