from django.db import models

# Create your models here.
class AppInfo(models.Model):
    name = models.CharField(max_length=30)
    priority = models.CharField(max_length=10)
    srcip = models.CharField(max_length=40)
    desip = models.CharField(max_length=40)
    status = models.CharField(max_length=10)
    health = models.CharField(max_length=20)
    action = models.CharField(max_length=20)
    routes = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.name
    
   
class Nodes(models.Model):
    name = models.CharField(max_length=30)
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    status = models.IntegerField()
    
    def __unicode__(self):
        return self.name


    
class LinkNodes(models.Model):
    nameL = models.CharField(max_length=30)
    sourceN = models.IntegerField()
    targetN = models.IntegerField()
    statusL = models.IntegerField()
    
    def __unicode__(self):
        return self.nameL