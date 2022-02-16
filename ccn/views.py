from django.shortcuts import render, redirect,get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Postagens,Universidades,Titulos,Impretas,Editoras,Localidades,Spine,Assuntos,Designacao,Relacionadas,TermoLivre
from django.utils import timezone
from django.urls import reverse
from django.db import connection
from django.db.models import Q
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
    arrayTitulosAdicionais=[]
    arrayTitulosExpandido=[]
    arrayRelacoes=[]
    valid=False
    if request.method == "POST":
        for post in request.POST:
            if (post!='csrfmiddlewaretoken' and post!='formatoConsulta'):
                valid=True
                lista_itens2.append(str(post))

        if(valid):
            request.session.setdefault('formatoConsulta', '')
            request.session.setdefault('postagens', '')

            request.session['postagens'] = ','.join(lista_itens2)
            request.session['formatoConsulta'] = request.POST['formatoConsulta']
        else:
            lista_itens2=(request.session['postagens']).split(',')

        try:
            formatoConsulta = request.POST['formatoConsulta']
        except:
            try:
                formatoConsulta=request.session['formatoConsulta']
            except:
                print ('erro')
                
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
        arrayTitulosAdicionais=montaTitulosAdicionais(lista_itens2)
        arrayTitulosExpandido=montaTitulosExpandido(lista_itens2)
        arrayRelacoes=buscaRelacoes(lista_itens2)

        if (formatoConsulta=='Detalhado'):
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
        'titulos_adicionais':arrayTitulosAdicionais,
        'titulos_expandidos':arrayTitulosExpandido,
        'imprentas':arrayImprenta,
        'assuntos':arrayAssuntos,
        'designacoes':arrayDesignacoes,
        'formatoConsulta':formatoConsulta,
        'relacoes':arrayRelacoes})

def relacao(request):
    publicacao ={
        'cod':'',
        'cod_ccn':'',
        'cod_issn':'',
        'cod_issn_online':'',
        'titulo':'',
        'home_page':'',
        'designacoes':'',
        'imprentas':'',
        'assunto':'',
        'frequencia':'',
        'titulo_abreviado':'',
        'titulos_expandidos':'',
        'titulos_adicionais':'',
        'relacoes':'',
        'lista_universidades':''
    }
    publ_cod=request.POST.get("publ_cod")
    lista_postagens = list(Postagens.objects.using('primary').filter(cod=publ_cod))[0]
    arrayDesignacoes=montaDesignacoes([publ_cod])[0]
    arrayImprenta=montaImprenta([publ_cod])[0]
    arrayAssuntos=montaAssuntos([publ_cod])[0]
    arrayTitulos=montaTitulos([publ_cod])[0]
    arrayTitulosAdicionais=montaTitulosAdicionais([publ_cod])[0]
    arrayTitulosExpandido=montaTitulosExpandido([publ_cod])[0]
    arrayRelacoes=buscaRelacoes([publ_cod])[0]
    arrayUniversidades=montaColecao([publ_cod])

    publicacao['cod']=lista_postagens.cod
    publicacao['cod_ccn']=lista_postagens.cod_ccn
    publicacao['cod_issn']=lista_postagens.cod_issn
    publicacao['cod_issn_online']=lista_postagens.cod_issn_online
    publicacao['titulo']=arrayTitulos
    publicacao['home_page']=lista_postagens.home_page
    publicacao['designacoes']=arrayDesignacoes
    publicacao['imprentas']=arrayImprenta
    publicacao['assunto']=arrayAssuntos
    publicacao['frequencia']=lista_postagens.frequencia
    publicacao['titulo_abreviado']=''
    publicacao['titulos_expandidos']=arrayTitulosExpandido
    publicacao['titulos_adicionais']=arrayTitulosAdicionais
    publicacao['relacoes']=arrayRelacoes
    publicacao['lista_universidades']=arrayUniversidades


    print (arrayRelacoes)
    return render(request, 'relacao.html',{
        'postagem':publicacao
    })

def montaTitulos(listaCodPublicacoes):
    arrayTitulos=[]
    for cod in listaCodPublicacoes:
        titulosRetorno = Titulos.objects.using('primary').filter(publ_cod=cod,tipo=16)
        titulo=''
        tipos=[]
        for titulos in titulosRetorno:
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
            if (localidade[0].uf_cod != 'XX'):
                texto=texto+localidade[0].uf_cod+': '
            else:
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
            termo_livre=''
            if (spine.tlv_cod!=None):
                termo_livre = list(TermoLivre.objects.using('primary').filter(cod=spine.tlv_cod))
            for assunto in lista_assuntos:
                if (termo_livre!=''):
                    textoSpine=textoSpine+assunto.des+' - '+termo_livre[0].des+', '
                else:
                    textoSpine=textoSpine+assunto.des+', '
        
        arrayAssuntos.append(textoSpine[:-2])
    return arrayAssuntos

def montaTitulosAdicionais(lista):
    arrayTitulosAdicionais=[]
    for cod in lista:
        titulosRetorno = Titulos.objects.using('primary').filter(publ_cod=cod,tipo='09')
        texto=''

        for titulo in titulosRetorno:
            texto = texto+titulo.titulo+'\n'
        arrayTitulosAdicionais.append(texto)
    
    return arrayTitulosAdicionais

def montaTitulosExpandido(lista):
    arrayTitulosExpandido=[]
    for cod in lista:
        titulosRetorno = Titulos.objects.using('primary').filter(publ_cod=cod,tipo='12')
        texto=''

        for titulo in titulosRetorno:
            texto = texto+titulo.titulo+'\n'

        arrayTitulosExpandido.append(texto)
    
    return arrayTitulosExpandido

def buscaRelacoes(lista):
    arrayRelacoes=[]
    for cod in lista:
        arrayRelacoesTemp=[]
        relacoesPubl_cod = Relacionadas.objects.using('primary').filter(publ_cod=cod)
        relacoesPubl_cod_rel = Relacionadas.objects.using('primary').filter(publ_cod_rel=cod)
        for rel in relacoesPubl_cod:
            novoRel = montaRelacoes(rel,cod)
            arrayRelacoesTemp.append(novoRel)
        for rel in relacoesPubl_cod_rel:
            novoRel = montaRelacoes(rel,cod)
            arrayRelacoesTemp.append(novoRel)
        arrayRelacoes.append(arrayRelacoesTemp)
    return arrayRelacoes

def montaRelacoes(rel,cod):
    novoRel = {
        'titulo':'',
        'publ_cod':'',
        'tipo':rel.tipo
    }

    if (rel.publ_cod == int(cod)):
        if (rel.tipo=='A'):
            novoRel["tipo"]='E Subsérie de'
        if (rel.tipo=='B'):
            novoRel["tipo"]='É Suplemento de'
        if (rel.tipo=='C'):
            novoRel["tipo"]='Continuação de'
        if (rel.tipo=='D'):
            novoRel["tipo"]='Continuação Parcial de'
        if (rel.tipo=='E'):
            novoRel["tipo"]='Formado pela fusão de'
        if (rel.tipo=='F'):
            novoRel["tipo"]='Absorveu'
        if (rel.tipo=='G'):
            novoRel["tipo"]='Absorveu em parte'
        if (rel.tipo=='H'):
            novoRel["tipo"]='Formado pela Subdivisão de'
        if (rel.tipo=='I'):
            novoRel["tipo"]='Notas de Indexação'
        if (rel.tipo=='J'):
            novoRel["tipo"]='E Edição em outro idioma'
        if (rel.tipo=='K'):
            novoRel["tipo"]='Fundiu com'
        if (rel.tipo=='L'):
            novoRel["tipo"]='Para formar'

        novoRel['titulo']=montaTitulos([rel.publ_cod_rel])[0]
        novoRel['publ_cod']=rel.publ_cod_rel
    else:
        if (rel.tipo=='A'):
            novoRel["tipo"]='Tem subsérie'
        if (rel.tipo=='B'):
            novoRel["tipo"]='Tem suplemento'
        if (rel.tipo=='C'):
            novoRel["tipo"]='Continuado por'
        if (rel.tipo=='D'):
            novoRel["tipo"]='Continuado em parte por'
        if (rel.tipo=='E'):
            novoRel["tipo"]='Para formar'
        if (rel.tipo=='F'):
            novoRel["tipo"]='Absorvido por'
        if (rel.tipo=='G'):
            novoRel["tipo"]='bsorvido em parte por'
        if (rel.tipo=='H'):
            novoRel["tipo"]='Subdividiu-se em'
        if (rel.tipo=='I'):
            novoRel["tipo"]='Subdividiu-se em'
        if (rel.tipo=='J'):
            novoRel["tipo"]='Tem edição em outro idioma'
        if (rel.tipo=='K'):
            novoRel["tipo"]='Formado pela fusão de'

        novoRel['titulo']=montaTitulos([rel.publ_cod])[0]
        novoRel['publ_cod']=rel.publ_cod
    
    return novoRel

def montaColecao(lista):
    lista_universidades = list(Universidades.objects.using('primary').raw(Universidades().select(','.join(lista))))
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
    
    return lista_universidades