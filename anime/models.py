from django.db import models

class Anime(models.Model):
    uid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.CharField(max_length=255)
    aired = models.CharField(max_length=255)
    episodes = models.IntegerField()
    members = models.IntegerField()
    popularity = models.IntegerField()
    ranked = models.CharField(max_length=255)
    score = models.FloatField()
    img_url = models.URLField()
    link = models.URLField()
    
    star_html = ""
