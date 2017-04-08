"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Ovpn_server(models.Model):
    
    class Meta:
        verbose_name = u'сервер'
        verbose_name_plural = u'серверы'
    server_title = models.CharField(max_length = 30)
    server_address  = models.TextField() 
    
    def __str__(self):
        return self.server_title
        #return u'{}'.format(self.reg_title)