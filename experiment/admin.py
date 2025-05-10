from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.

from . import models

admin.site.register(models.Graph)
admin.site.register(models.X_Vertice)
admin.site.register(models.U_chain)
admin.site.register(models.Const_visual)
admin.site.register(Permission)