# -*- coding: utf-8 -*-
#created 17.08.2015 by myself

from django.contrib import admin 
from django.contrib.admin import AdminSite

from app.models import Ovpn_server

# Ovpn server
class Ovpn_server_Admin(admin.ModelAdmin):    
    list_display =  ['server_title', 'server_address']

admin.site.register(Ovpn_server,Ovpn_server_Admin)