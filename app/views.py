"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date, time
import subprocess

from django.views.generic import View, TemplateView, FormView
from django.views.generic.edit import FormMixin
from django.contrib import auth
from django.contrib.auth.models import User

import MySQLdb

from app.forms import ConfGenForm, MonSqlSumForm
from django.urls import reverse

from app.engine import conf_gen_ovpn, conf_iptables, conf_summary  #, conf_gen_systemctl
from .models import Ovpn_server

from django.conf import settings
# output from bash command
def run(command):
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return output

class CommonView(TemplateView):
    """ 
    commmon class for views with date args an etc
    """
    template_name = 'app/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(CommonView, self).get_context_data(**kwargs)
        context['year'] = datetime.now().year
        # pass username to see: is user authenticated ?
        context['username'] = auth.get_user(self.request).username
        return context

# main page
class HomeView(CommonView):
    """main page"""
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        # output from radwho
        radwho_list_out = run('radwho -F /var/log/freeradius/radutmp').split('\n')
        radwho_list_head = radwho_list_out.pop(0)  # cut head of table
        
        context = super(HomeView, self).get_context_data(**kwargs)
        
        context['radwho_list_head'] = radwho_list_head.split()
        context['radwho_list'] = radwho_list_out         
        context['radwho_count'] = radwho_list_out.__len__() - 1
        context['title'] = 'Monitoring page'        
        print(radwho_list_out)   
        #print(Ovpn_server.objects.all()) 
        for i,row in enumerate(radwho_list_out):
            if row != '':                     #check string is not empty
                server_in_row = row.split()[-2]     # field with server ip
                #print(server_in_row)
                for s in Ovpn_server.objects.all():
                    if server_in_row in s.server_address:
                        #print('Sovpadenie {0}, {1} \n'.format(row, server_in_row))
                        new_row = row + ' ' + s.server_title
                        #print(new_row)
                        radwho_list_out[i] = new_row                    
        print(radwho_list_out)

        return context

#monitoring from sql db
class MonSqlView(CommonView):
    template_name = 'app/monsql.html'

    def get_context_data(self, **kwargs):
        # sql command       
        context = super(MonSqlView, self).get_context_data(**kwargs)
        context['title'] = 'Monitoring users from SQL'

        db=MySQLdb.connect(host="localhost", user=settings.MYSQL_USER, \
                  passwd=settings.MYSQL_PASS, db=settings.MYSQL_TB)
        c=db.cursor()
        query = """ SELECT `radacctid`,`username`,`nasipaddress`,`acctstarttime`,`acctstoptime` FROM `radacct` WHERE acctstoptime is NULL ORDER BY `radacctid`; """
        try:
            c.execute(query)
            out_sql = c.fetchall()
        except Exception as e:
            out_sql = 'Error {}'.format(e)
        #print(type(out_sql) 
        context['out_sql'] = out_sql
        context['count_all'] = len(out_sql)
        return context

#SUM query from sql db
class MonSqlSum_GET_View(CommonView):
    template_name = 'app/monsqlsum.html'

    def get_context_data(self, **kwargs):               
        context = super(MonSqlSum_GET_View, self).get_context_data(**kwargs)
        context['title'] = 'SUM query from SQL'
        if 'date_start' in kwargs: 
            date_start = str(kwargs['date_start'])                     
        else:
            date_start = '2017-01-01'            
        context['date_start'] = date_start             
        if 'date_end' in kwargs:
            print(str(kwargs['date_end']))
            date_end = str(kwargs['date_end'])               
        else:           
            date_end = "{:%Y-%m-%d}".format(datetime.now())      
        context['date_end'] = date_end

        context['form'] = MonSqlSumForm        

        db=MySQLdb.connect(host="localhost", user=settings.MYSQL_USER, \
                  passwd=settings.MYSQL_PASS, db=settings.MYSQL_TB)
        c=db.cursor()
        
        query = """SELECT username,SUM(acctsessiontime)/3600,SUM(acctinputoctets)/(1024*1024),SUM(acctoutputoctets)/(1024*1024)  \
                FROM radacct WHERE acctstarttime > "{0}" AND acctstoptime < "{1}" group by username ORDER BY radacct.username ASC;""".format(date_start, date_end)
        #query = """SELECT username,SUM(acctsessiontime)/3600,SUM(acctinputoctets)/(1024*1024), \
         #           SUM(acctoutputoctets)/(1024*1024) , (UNIX_TIMESTAMP( acctstoptime ) - UNIX_TIMESTAMP( acctstarttime ) )/3600  \
          #      FROM radacct \
           #     WHERE acctstarttime > "{0}" AND acctstoptime < "{1}" group by username ORDER BY radacct.username ASC;""".format(date_start, date_end)
        try:
            c.execute(query)
            out_sql = c.fetchall()
            print(list(out_sql))
            print('-----out_sql on top---')
        except Exception as e:
            out_sql = 'Error {}'.format(e)         
        context['out_sql'] = out_sql       # dfdf  
        context['count_all'] = len(out_sql)

        return context

class MonSqlSum_POST_View(FormView):
    template_name = 'app/monsqlsum.html'
    form_class = MonSqlSumForm

    # def get_success_url(self, **kwargs):
    #     print(self)
    #     print('---into get succes----')
    #     print(kwargs)
    #     #print( request.POST['servers'] )
    #     return reverse('config_generator' , kwargs={'servers': '2222'} )

    def post(self, request, *args, **kwargs):
        print(request)
        print('===============')
        form = self.get_form()
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        #self.object = self.get_object()
        
        print( request.POST['date_start'] )    #form.cleaned_data['servers'])
        # передаем параметр и редиректим в GET
        return redirect(reverse('mon_sql_sum', kwargs={'date_start': request.POST['date_start'], 'date_end': request.POST['date_end']}))
        # if form.is_valid():
        #     print('----success----')
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super(MonSqlSum_POST_View, self).form_valid(form)

class MonSqlSumView(View):

    def get(self, request, *args, **kwargs):
        view = MonSqlSum_GET_View.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MonSqlSum_POST_View.as_view()
        return view(request, *args, **kwargs)

#openvpn config genrator
# след 3 класса работают в связке , один для GET , второй для POST, 3ий для объединения
class ConfGen_GET_View(CommonView):
    template_name = 'app/conf_generator.html'
    
    def get_context_data(self, **kwargs):              
        context = super(ConfGen_GET_View, self).get_context_data(**kwargs)        
        context['form'] = ConfGenForm
        print('---into get----')
        print(kwargs) 
        context['title'] = 'Config generator page'  
        
        # если функция вызвана из POST запроса и передан параметр
        if 'servers' in kwargs:      
           _servers =  kwargs['servers'].split(' ')   
           context['servers_ip'] = kwargs['servers']
           
           context['configs'] = conf_gen_ovpn.generate( _servers )   #, 'tcp')  
           context['iptables'] = conf_iptables.generate_iptables( _servers, kwargs['net_card'])
           context['summary_view'] = conf_summary.generate( _servers, kwargs['net_card'])
        if 'net_card' in kwargs: 
            context['net_card'] = kwargs['net_card']

        return context
    

class ConfGen_POST_View(FormView):
    template_name = 'app/conf_generator.html'
    form_class = ConfGenForm

    def get_success_url(self, **kwargs):
        print(self)
        print('---into get succes----')
        print(kwargs)
        #print( request.POST['servers'] )
        return reverse('config_generator', kwargs={'servers': request.POST['servers']})   #reverse('config_generator' , kwargs={'servers': '2222'} )

    def post(self, request, *args, **kwargs):
        print(request)
        print('===============')
        form = self.get_form()
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        #self.object = self.get_object()
        
        #print( request.POST['servers'] )    #form.cleaned_data['servers'])
        #print( request.POST['net_card'] )
        # передаем параметр и редиректим в GET
        return redirect(reverse('config_generator',  kwargs={'servers': request.POST['servers'], 'net_card': request.POST['net_card'] }))
        # if form.is_valid():
        #     print('----success----')
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super(ConfGen_POST_View, self).form_valid(form)

class ConfGeneratorView(View):

    def get(self, request, *args, **kwargs):
        view = ConfGen_GET_View.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ConfGen_POST_View.as_view()
        return view(request, *args, **kwargs)




def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
