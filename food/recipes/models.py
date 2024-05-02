from django.db import models

# Create your models here.
class FinalRecipe(models.Model):
    id = models.IntegerField(primary_key=True,blank=True, null=False)
    recipe_name = models.TextField(db_column='Recipe Name', blank=True, null=True)
    ingredients = models.TextField(db_column='Ingredients', blank=True, null=True) 
    cuisine = models.TextField(db_column='Cuisine', blank=True, null=True) 
    instructions = models.TextField(db_column='Instructions', blank=True, null=True) 
    totaltimeinmins = models.BigIntegerField(db_column='TotalTimeInMins', blank=True, null=True)  
    imageurl = models.TextField(db_column='Imageurl', blank=True, null=True)
    ingredientcount = models.IntegerField(db_column='Ingredientcount', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'final recipe'