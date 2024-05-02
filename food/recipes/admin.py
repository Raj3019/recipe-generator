from django.contrib import admin
from .models import FinalRecipe
# Register your models here.

class finalRecipe(admin.ModelAdmin):
    list_display = ['id','recipe_name','ingredients','cuisine','instructions',
                    'totaltimeinmins','imageurl','ingredientcount']
    ordering = ['id']

admin.site.register(FinalRecipe,finalRecipe)
