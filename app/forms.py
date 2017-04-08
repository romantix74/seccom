"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

#form for generating config
class ConfGenForm(forms.Form):
    servers = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'ip серверов через пробел'}) )
    net_card = forms.CharField(max_length=10,
                              widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'сетевая карта, например: eth0'}) )
#form for Mysql SUM
class MonSqlSumForm(forms.Form):
    date_start = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'дата начала периода',
                                   'id' : 'id_sumsql_date_start' }))
    date_end = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'дата конца периода',
                                   'id' : 'id_sumsql_date_end' }))