from django.db import models


class Category (models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photo/categories', blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
