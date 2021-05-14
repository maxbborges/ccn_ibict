from django.shortcuts import render, redirect,get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Postagens,Universidades,Postagens_titulo
from django.utils import timezone
from django.urls import reverse
from django.db import connection
import json
from django.contrib.sessions.backends.db import SessionStore

def index(request):
    camposConsulta ={
       'Título':'tituloproprio',
       'Assunto':'s.DES',
       'País de publicação':'p2.des',
       'Idioma do texto':'i.des',
       'Código CCN':'COD_CCN',
       'Número ISSN':'COD_ISSN',
       'Situação de publicação':'SIT_PUBL',
       'Local de edição/publicação':'l.des',
       'Editor/Publicador':'e.nome',
       'Título abreviado':'TITULO_ABREVIADO'
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
        post_list= Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'],'')
        lista = Postagens.objects.using('primary').raw(post_list)
        page_number = request.GET.get('page')
        paginator = Paginator(lista,request.session['qtdItens'])
        page_obj = paginator.page(page_number)

    if request.method == "POST":
        request.session['v1'] = (request.POST).getlist('tipo')
        request.session['v2'] = (request.POST).getlist('valor')
        request.session['v3'] = (request.POST).getlist('juncao')
        request.session['qtdItens'] = 10

        post_list= Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'],'')
        lista = Postagens.objects.using('primary').raw(post_list)

        page_number = request.GET.get('page',1)
        paginator = Paginator(lista,request.session['qtdItens'])
        page_obj = paginator.page(page_number)

    qtdPostagensPagina = int(request.session['qtdItens'])
    qtdPostagensBanco = len(list(lista))
    if (qtdPostagensPagina>qtdPostagensBanco):
        qtdPostagensPagina = qtdPostagensBanco
        
    return render(request,'busca.html',{'postagens': page_obj,'itens':numeroDeItens,'qtdPostagensBanco':qtdPostagensBanco,'qtdPostagensPagina':qtdPostagensPagina})
    

def resultado(request):
    lista_itens=''
    if request.method == "POST":
        for post in request.POST:
            if (post!='csrfmiddlewaretoken' and post!='formatoConsulta'):
                lista_itens=lista_itens+"'"+str(post)+"'"+","

        if (request.POST['formatoConsulta']=='Detalhado'):
            lista_universidades = list(Universidades.objects.using('primary').raw(Universidades().select(lista_itens[:-1])))
        lista_postagens = list(Postagens.objects.using('primary').raw(Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'],lista_itens[:-1])))
        lista_titulos = Postagens_titulo.objects.using('primary').raw(Postagens_titulo().get_titulo_completo(lista_itens[:-1]))

    return render(request, 'resultado.html',{'lista_postagens': lista_postagens,'lista_universidades':lista_universidades,'lista_titulos':lista_titulos})
