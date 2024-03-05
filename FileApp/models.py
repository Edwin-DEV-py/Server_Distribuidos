from django.db import models

class FileModel(models.Model):

    #atributos
    id = models.AutoField(primary_key=True, unique=True)
    fileName = models.CharField(max_length=200)
    folderParent = models.IntegerField(default=0)
    file = models.FileField(upload_to='example/', null=True, blank=True)
    filePath = models.CharField()
    userId = models.CharField(max_length=100)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fileName
    

    def getPath(self):
        return self.filePath
