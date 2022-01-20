from django.db import models

class Postagens(models.Model):
    class Meta:
        db_table='"ccn"."publicacao"'

    cod = models.IntegerField(primary_key=True) #cod
    pais = models.CharField(max_length=100,db_column='pai_cod') #pai_cod
    _frequencia = models.CharField(max_length=100,db_column='freq') #freq
    tit_proprio = models.CharField(max_length=100) #tit_proprio
    titulo_abreviado = models.CharField(max_length=100) #tit_abreviado
    cod_ccn = models.CharField(max_length=100) #cod_ccn
    cod_issn = models.CharField(max_length=100) #cod_issn
    cod_issn_online = models.CharField(max_length=100,db_column='cod_issn_l') #cod_issn_l
    home_page = models.CharField(max_length=100) #home_page
    situacao = models.CharField(max_length=100,db_column='sit_publ') #sit_publ

    @property
    def frequencia(self):
        if self._frequencia == 'Q':
            return 'TRIMESTRAL'
        if self._frequencia == 'M':
            return 'MENSAL'
        if self._frequencia == 'B':
            return 'BIMESTRAL'
        if self._frequencia == 'B':
            return 'BIMESTRAL'
        if self._frequencia == 'S':
            return 'BIMENSAL'
        if self._frequencia == '?':
            return 'DESCONHECIDO'
        if self._frequencia == 'A':
            return 'ANUAL'
        if self._frequencia == 'T':
            return 'QUADRIMESTRAL'
        if self._frequencia == 'K':
            return 'IRREGULAR'
        if self._frequencia == 'Z':
            return 'OUTRAS'
        if self._frequencia == 'W':
            return 'SEMANAL'
        if self._frequencia == 'H':
            return 'TRIENAL'
        if self._frequencia == 'I':
            return 'TRÊS VEZES NA SEMANA'
        if self._frequencia == 'J':
            return 'TRÊS VEZES NO MES'
        if self._frequencia == 'D':
            return 'DIARIA'
        if self._frequencia == 'C':
            return 'BISSEMANAL'
        if self._frequencia == 'E':
            return 'QUINZENAL'
        if self._frequencia == 'G':
            return 'BIENAL'
		
        return self._frequencia
    
    ###### DOCUMENTAÇÃO DA FUNÇÃO SELECT ######
    # self: os parametros internos
    # tipo: valor da option do select .slc-chave-tipo (ARRAY COM CADA OPTION PREENCHIDA)
    # valor: valor do campo input .ipt-valor (ARRAY CADA TEXTO PREENCHIDO)
    # juncao: valor da option do select .slc-chave-juncao (ARRAY COM CADA OPTION PREENCHIDA)
    def select (self,tipo,valor,juncao):
        textoWhere = f''
        temp=''
        consulta = f'''select 
            cod as cod,
            tit_proprio, 
            titulo_abreviado, 
            cod_ccn,
            cod_issn,
            cod_issn_l as cod_issn_online,
            home_page, 
            sit_publ as situacao, 
            pai_cod as pais 
            from ccn.publicacao WHERE '''
        for i,val in enumerate(valor):
            if val:
                textoWhere = textoWhere+f'''contains(idx_clob,'{val} within {tipo[i]}')>0 {juncao[i]} '''
                temp=juncao[i]
        textoWhere=textoWhere[:-(len(temp)+1)]

        consulta = consulta+textoWhere+'ORDER by cod'
        print (consulta)
        return consulta

class Titulos(models.Model):
    class Meta:
        db_table='"ccn"."publicacao_titulo"'    

    publ_cod = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=100,db_column='tipo')
    titulo = models.CharField(max_length=100,db_column='titulo')
    seq = models.IntegerField(db_column='seq')
    titulo_completo = models.TextField(db_column='TITULO_COMPLETO')

class Universidades(models.Model):
    seq = models.IntegerField(primary_key=True)
    publ_cod = models.CharField(max_length=100)
    bibl_cod = models.CharField(max_length=100)
    conteudo = models.CharField(max_length=500)
    uf_cod = models.CharField(max_length=100)
    sigla = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    des = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    def select (self,codigo):
        consulta = f'''
        SELECT DISTINCT
        pc.PUBL_COD, bc.BIBL_COD, pc.SEQ , l.UF_COD, b.SIGLA, b.NOME, b.LOGRADOURO,
        b.BAIRRO, l.DES, b.CEP, bc.NUMERO, bc.TIPO , pc.CONTEUDO
        FROM ccn.PUBLICACAO_COLECAO pc
        INNER JOIN ccn.BIBLIOTECA b ON b.COD = pc.BIBL_COD
        INNER JOIN ccn.BIBLIOTECA_CONTATO bc ON pc.BIBL_COD = bc.BIBL_COD
        INNER JOIN ccn.LOCALIDADE l ON l.COD = b.MUNI_COD
        WHERE
        pc.PUBL_COD IN ({codigo})
        ORDER BY l.UF_COD, b.SIGLA,pc.SEQ  ;'''
        return consulta

class Impretas(models.Model):
    class Meta:
        db_table='"ccn"."publicacao_imprenta"'

    publ_cod=models.IntegerField(primary_key=True)
    edto_cod=models.CharField(max_length=100,db_column='edto_cod')
    muni_cod=models.CharField(max_length=100,db_column='muni_cod')

class Editoras(models.Model):
    class Meta:
        db_table='"ccn"."editora"'

    cod=models.CharField(primary_key=True,max_length=100)
    nome=models.CharField(max_length=100,db_column='nome')

class Localidades(models.Model):
    class Meta:
        db_table='"ccn"."localidade"'

    cod=models.IntegerField(primary_key=True)
    des=models.CharField(max_length=100,db_column='des')
    pai_cod=models.CharField(max_length=100,db_column='pai_cod')

class Spine(models.Model):
    class Meta:
        db_table='"ccn"."publicacao_spines"'

    publ_cod=models.IntegerField(primary_key=True)
    spin_cod=models.IntegerField(db_column='spin_cod')

class Assuntos(models.Model):
    class Meta:
        db_table='"ccn"."spines"'

    cod=models.IntegerField(primary_key=True)
    des=models.CharField(max_length=100,db_column='des')

class Designacao(models.Model):
    class Meta:
        db_table='"ccn"."PUBLICACAO_DESIGNACAO"'

    publ_cod=models.IntegerField(primary_key=True)
    designacao=models.CharField(max_length=100,db_column='designacao')



    


