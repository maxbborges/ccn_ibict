from django.shortcuts import render, redirect,get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Postagens,Universidades,Titulos,Impretas,Editoras,Localidades,Spine,Assuntos,Designacao
from django.utils import timezone
from django.urls import reverse
from django.db import connection
import json
from django.contrib.sessions.backends.db import SessionStore

def index(request):
    camposConsulta ={
       'Título':'tituloproprio',
       'Assunto':'assunto',
       'País de publicação':'pais',
       'Idioma do texto':'idioma',
       'Código CCN':'codccn',
       'Número ISSN':'cod_issn',
       'Situação de publicação':'sitpubl',
       'Local de edição/publicação':'imprenta',
       'Editor/Publicador':'local',
       'Título abreviado':'tituloabreviado'
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

    if request.method == "POST":
        request.session['v1'] = (request.POST).getlist('tipo')
        request.session['v2'] = (request.POST).getlist('valor')
        request.session['v3'] = (request.POST).getlist('juncao')
        request.session['qtdItens'] = 10
    
    # RECUPERA AS POSTAGENS DO MODEL POSTAGEM
    post_list= Postagens().select(request.session['v1'],request.session['v2'],request.session['v3'])
    lista = Postagens.objects.using('primary').raw(post_list)
    
    if (len(lista)<=0):
        return render(request,'busca.html',{'postagens': [],'titulos':[],'itens':numeroDeItens,'qtdPostagensBanco':0,'qtdPostagensPagina':0})
    # RECUPERA OS TITULOS DO MODEL TITULOS
    listaCodPublicacoes=[]
    for l in lista:
        listaCodPublicacoes.append(l.cod)
        
    paginator = Paginator(lista,request.session['qtdItens'])
    page = request.GET.get('page')
    pageLista = paginator.get_page(page)

    qtdPostagensPagina = int(request.session['qtdItens'])
    qtdPostagensBanco = len(list(lista))

    if (page=='1' or not page):
        arrayTitulos=montaTitulos(listaCodPublicacoes[0:qtdPostagensPagina-1])
    else:
        arrayTitulos=montaTitulos(listaCodPublicacoes[qtdPostagensPagina*(int(page)-1):(qtdPostagensPagina*int(page))-1])

    if (qtdPostagensPagina>qtdPostagensBanco):
        qtdPostagensPagina = qtdPostagensBanco
        
    return render(request,'busca.html',{'postagens': pageLista,'titulos':arrayTitulos,'itens':numeroDeItens,'qtdPostagensBanco':qtdPostagensBanco,'qtdPostagensPagina':qtdPostagensPagina})
    

def resultado(request):
    lista_itens2=[]
    lista_postagens=[]
    lista_universidades=[]
    arrayTitulos=[]
    arrayAssuntos=[]
    arrayDesignacoes=[]
    arrayImprenta = []
    if request.method == "POST":
        for post in request.POST:
            if (post!='csrfmiddlewaretoken' and post!='formatoConsulta'):
                lista_itens2.append(str(post))
        
        # Recupera todas as publicações selecionadas
        lista_postagens = list(Postagens.objects.using('primary').filter(cod__in=lista_itens2))

        # Recupera as designacoes/Área de numeração
        arrayDesignacoes=montaDesignacoes(lista_itens2)

        # Recupera todas as imprentas das publicações
        arrayImprenta=montaImprenta(lista_itens2)

        # Recupera todos os assuntos das publicações
        arrayAssuntos=montaAssuntos(lista_itens2)

        # Formata os titulos para o padrão de exibição
        arrayTitulos=montaTitulos(lista_itens2)

        if (request.POST['formatoConsulta']=='Detalhado'):
            lista_universidades = list(Universidades.objects.using('primary').raw(Universidades().select(','.join(lista_itens2))))
            _tempNumero = []
            _tempTipo = []
            _tempPos =[]
            for i,universidade in enumerate(lista_universidades):
                if lista_universidades[i].seq != lista_universidades[i-1].seq and i!=0:
                    lista_universidades[i-1].numero = _tempNumero
                    _tempNumero =[]
                else:
                    if i!=0:
                        _tempPos.append(i-1)
                
                if (int(lista_universidades[i].tipo) == 1 or  int(lista_universidades[i].tipo) == 2):
                    _tempNumero.append("<b>Telefone:</b> "+lista_universidades[i].numero)
                if (int(lista_universidades[i].tipo) == 3):
                    _tempNumero.append(f"<b>Email:</b> <a href='mailto:{lista_universidades[i].numero}' target='_blank'>"+lista_universidades[i].numero+'</a>')
                if (int(lista_universidades[i].tipo) == 4):
                    _tempNumero.append(f"<b>Home Page: </b><a href='{lista_universidades[i].numero}' target='_blank'>"+lista_universidades[i].numero+'</a>')

                if(i==(len(lista_universidades)-1)):
                    lista_universidades[i].numero = _tempNumero
                    for pos in reversed(_tempPos):
                        lista_universidades.pop(pos)

    return render(request, 'resultado.html',{
        'lista_postagens': lista_postagens,
        'lista_universidades':lista_universidades,
        'lista_titulos':arrayTitulos,
        'imprentas':arrayImprenta,
        'assuntos':arrayAssuntos,
        'designacoes':arrayDesignacoes,
        'formatoConsulta':request.POST['formatoConsulta']})

def montaTitulos(listaCodPublicacoes):
    arrayTitulos=[]
    for cod in listaCodPublicacoes:
        titulosRetorno = Titulos.objects.using('primary').filter(publ_cod=cod,tipo=16)
        titulo=''
        tipos=[]
        for titulos in titulosRetorno:
            # if titulos.tipo not in tipos:
            #     tipos.append(titulos.tipo)
            # else:
            #     titulo=titulo+' ; '+titulos.titulo
            #     continue

            # if (titulos.tipo=='01'):
            #     titulo=titulo+titulos.titulo
            # if (titulos.tipo=='02'):
            #     titulo=titulo+' ('+titulos.titulo+')'
            # if (titulos.tipo=='07'):
            #     titulo=titulo+' : '+titulos.titulo
            # if (titulos.tipo=='08'):
            #     titulo=titulo+' . '+titulos.titulo
            # if (titulos.tipo=='11'):
            #     titulo=titulo+' = '+titulos.titulo
            # if (titulos.tipo=='14'):
            #     titulo=titulo+' / '+titulos.titulo
            # if (titulos.tipo=='15'):
            #     titulo=titulo+' . '+titulos.titulo
        
            arrayTitulos.append(titulos.titulo_completo)
    return arrayTitulos

def montaDesignacoes(lista):
    arrayDesignacoes=[]
    for cod in lista:
        lista_designacoes = Designacao.objects.using('primary').filter(publ_cod=cod)
        texto=''
        for designacoes in lista_designacoes:
            texto = texto + designacoes.designacao + '\n'
        
        arrayDesignacoes.append(texto)
    return arrayDesignacoes

def montaImprenta(lista):
    arrayImprenta=[]
    for cod in lista:
        lista_imprentas = Impretas.objects.using('primary').filter(publ_cod=cod)
        editoras=[]
        localidades=[]

        for imprentas in lista_imprentas:
            editoras.append(imprentas.edto_cod)
            localidades.append(imprentas.muni_cod)

        texto=''
        for i,codEditora in enumerate(editoras):
            editora = list(Editoras.objects.using('primary').filter(cod=codEditora))
            localidade = list(Localidades.objects.using('primary').filter(cod=localidades[i]))
            texto=texto+localidade[0].des+', '
            texto=texto+localidade[0].pai_cod+': '
            texto=texto+editora[0].nome+'\n'
        
        arrayImprenta.append(texto)
    return arrayImprenta

def montaAssuntos(lista):
    arrayAssuntos=[]
    for cod in lista:
        lista_spine=Spine.objects.using('primary').filter(publ_cod=cod)
        textoSpine=''
        for spine in lista_spine:
            lista_assuntos=Assuntos.objects.using('primary').filter(cod=spine.spin_cod)
            for assunto in lista_assuntos:
                textoSpine=textoSpine+assunto.des+', '
        
        arrayAssuntos.append(textoSpine[:-2])
    return arrayAssuntos