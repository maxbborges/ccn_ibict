from django.shortcuts import render, redirect,get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.paginator import Paginator
# from .forms import PostagensForm,PostagensForm1
from .models import Postagens,Universidades, Assuntos
from django.utils import timezone
from django.urls import reverse
from django.db import connection
import json
from django.contrib.sessions.backends.db import SessionStore

def index(request):
    camposConsulta ={
       'Titulo':'tituloproprio',
    #    'Assunto':'a',
       'Pais de publicação':'p2.des',
       'Idioma do Texto':'i.des',
       'Código CCN':'COD_CCN',
       'Número ISSN':'COD_ISSN',
       'Situação de publicação':'SIT_PUBL',
       'Local de Edição/Publicação':'l.des',
       'Editor/Publicador':'e.nome',
       'Titulo Abreviado':'TITULO_ABREVIADO'
    }
    return render(request,'index.html',{'campos':camposConsulta})

def busca(request):
    numeroDeItens={
        '10':'10',
        '20':'20',
        '30':'30',
        '40':'40',
        '50':'50',
        '60':'60'
    }
    if(request.GET.get('qtdItens')):
        request.session['qtdItens'] =request.GET.get('qtdItens') 
    if request.method == "GET":
        post_list= Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'])
        page_number = request.GET.get('page')
        paginator = Paginator(post_list,request.session['qtdItens'])
        page_obj = paginator.page(page_number)

    if request.method == "POST":
        request.session['v1'] = (request.POST).getlist('tipo')
        request.session['v2'] = (request.POST).getlist('valor')
        request.session['v3'] = (request.POST).getlist('juncao')
        request.session['qtdItens'] = 10

        post_list= Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'])
        page_number = request.GET.get('page',1)
        paginator = Paginator(post_list,request.session['qtdItens'])
        page_obj = paginator.page(page_number)
    
    return render(request,'busca.html',{'postagens': page_obj,'itens':numeroDeItens})
    

def resultado(request):
    lista_postagens=[]
    lista_universidades=[]
    lista_assuntos=[]
    formatoConsulta = request.POST['formatoConsulta']
    if request.method == "POST":
        for post in request.POST:
            if (post!='csrfmiddlewaretoken' and post!='formatoConsulta'):
                a= Postagens().select2(request.session['v1'],request.session['v2'],request.session['v3'],post)
                lista_postagens.append(a)
                if (formatoConsulta=='Detalhado'):
                    lista_universidades.append(Universidades().select(post))
                if (formatoConsulta!='Simples'):
                    lista_assuntos.append(Assuntos().select(post))


    return render(request, 'resultado.html',{'lista_postagens': lista_postagens,'lista_universidades':lista_universidades,'lista_assuntos':lista_assuntos})
