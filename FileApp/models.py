from django.db import models

class FileModel(models.Model):

    #atributos
    id = models.AutoField(primary_key=True, unique=True)
    fileName = models.CharField(max_length=200)
    folderParent = models.IntegerField(default=0)
    userId = models.CharField(max_length=100)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fileName
    

    def getPath(self):
        return self.filePath
    
class FilePaths(models.Model):
    
    id = models.AutoField(primary_key=True, unique=True)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    filePath = models.CharField(max_length=500)
    
    def __str__(self):
        return self.filePath
