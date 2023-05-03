from django.db import models


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    hit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    insert_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def update_hit(self):
        self.hit = self.hit+1
        self.save()