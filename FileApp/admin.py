from django.contrib import admin
from .models import FileModel

class FileModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("Objeto a guardar:", obj.__dict__)

        super().save_model(request, obj, form, change)

admin.site.register(FileModel, FileModelAdmin)
