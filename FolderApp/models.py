from django.db import models

class FolderModel(models.Model):

    #atributos
    id = models.AutoField(primary_key=True)
    folderName = models.CharField(max_length=50)
    storage = models.IntegerField(blank=True, null=True)
    userId = models.CharField(max_length=100)
    parentFolder = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.folderName
    

