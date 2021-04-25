from django.db import models

class Postagens(models.Model):
    codigo = models.IntegerField(primary_key=True)
    frequencia = models.CharField(max_length=100)
    titulo_proprio = models.CharField(max_length=100)
    titulo_abreviado = models.CharField(max_length=100)
    codigo_ccn = models.CharField(max_length=100)
    codigo_issn = models.CharField(max_length=100)
    situacao = models.CharField(max_length=100)
    titulo_completo = models.CharField(max_length=100)
    designacao = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    des = models.CharField(max_length=100)
    uf = models.CharField(max_length=100)

    def select (self,tipo,valor,juncao):
        consulta = '''
        SELECT 
            p.COD AS codigo , 
                CASE
		        WHEN p.FREQ = 'F' THEN 'SEMESTRAL'
		        WHEN p.FREQ = 'M' THEN 'MENSAL'
		        WHEN p.FREQ = 'Q' THEN 'TRIMESTRAL'
		        WHEN p.FREQ = 'B' THEN 'BIMESTRAL'
		        WHEN p.FREQ = 'S' THEN 'BIMENSAL'
		        WHEN p.FREQ = '?' THEN 'DESCONHECIDO' 
		        WHEN  p.FREQ = 'A' THEN 'ANUAL'
		        WHEN  p.FREQ = 'T' THEN 'QUADRIMESTRAL'
		        WHEN  p.FREQ = 'K' THEN 'IRREGULAR'
		        WHEN  p.FREQ = 'Z' THEN 'OUTRAS'
		        WHEN  p.FREQ = 'W' THEN 'SEMANAL'
		        WHEN  p.FREQ = 'H' THEN 'TRIENAL'
		        WHEN  p.FREQ = 'I' THEN 'TRÊS VEZES NA SEMANA'
		        WHEN  p.FREQ = 'J' THEN 'TRÊS VEZES NO MES'
		        WHEN  p.FREQ = 'D' THEN 'DIARIA'
		        WHEN  p.FREQ = 'C' THEN 'BISSEMANAL'
		        WHEN  p.FREQ = 'E' THEN 'QUINZENAL'
		        WHEN  p.FREQ = 'G' THEN 'BIENAL'
		        ELSE p.FREQ 
            END AS frequencia, 
            p.TIT_PROPRIO, 
            p.TITULO_ABREVIADO, 
            p.COD_CCN,
            p.COD_ISSN,
            p.HOME_PAGE,
            CASE
           	WHEN p.SIT_PUBL='D' THEN 'N SEI'
           	ELSE p.SIT_PUBL 
           	END AS situacao,
            pt.TITULO_COMPLETO, 
            pd.DESIGNACAO, 
            e.NOME, 
            l.DES, 
            l.UF_COD,
            p2.DES AS pais,
            i.DES AS idioma
        FROM ccn.publicacao p, 
            ccn.PUBLICACAO_TITULO pt , 
            ccn.PUBLICACAO_DESIGNACAO pd,
            ccn.PUBLICACAO_IMPRENTA pub_i, 
            ccn.EDITORA e , 
            ccn.LOCALIDADE l,
            ccn.PAIS p2,
            ccn.PUBLICACAO_IDIOMA pi2,
            ccn.IDIOMA i 
        WHERE
            pt.PUBL_COD=p.COD 
            AND TITULO_COMPLETO IS NOT NULL 
            AND pd.PUBL_COD=p.COD 
            AND pub_i.PUBL_COD = p.COD 
            AND e.COD = pub_i.EDTO_COD 
            AND l.COD = pub_i.MUNI_COD
            AND p2.COD = p.PAI_COD
            AND p.COD = pi2.PUBL_COD
            AND pi2.IDIO_COD = i.COD
            AND'''
        
        for i,k1 in enumerate(valor):
            if(k1):
                if (i>0):
                    consulta=consulta+f'''{juncao[i]}'''

                if (tipo[i]=='tituloproprio'):
                    consulta=consulta+f''' contains(idx_clob,' {k1} within {tipo[i]}')>0 '''
                else:
                    consulta=consulta+f''' regexp_like({tipo[i]},'{k1}', 'i') '''
        consulta = consulta+f'''ORDER BY tit_proprio;'''
        return self.__class__.objects.using('primary').raw(consulta)

    def select2 (self,tipo,valor,juncao,codigo):
        consulta = '''
        SELECT 
            p.COD AS codigo , 
                CASE
		        WHEN p.FREQ = 'F' THEN 'SEMESTRAL'
		        WHEN p.FREQ = 'M' THEN 'MENSAL'
		        WHEN p.FREQ = 'Q' THEN 'TRIMESTRAL'
		        WHEN p.FREQ = 'B' THEN 'BIMESTRAL'
		        WHEN p.FREQ = 'S' THEN 'BIMENSAL'
		        WHEN p.FREQ = '?' THEN 'DESCONHECIDO' 
		        WHEN  p.FREQ = 'A' THEN 'ANUAL'
		        WHEN  p.FREQ = 'T' THEN 'QUADRIMESTRAL'
		        WHEN  p.FREQ = 'K' THEN 'IRREGULAR'
		        WHEN  p.FREQ = 'Z' THEN 'OUTRAS'
		        WHEN  p.FREQ = 'W' THEN 'SEMANAL'
		        WHEN  p.FREQ = 'H' THEN 'TRIENAL'
		        WHEN  p.FREQ = 'I' THEN 'TRÊS VEZES NA SEMANA'
		        WHEN  p.FREQ = 'J' THEN 'TRÊS VEZES NO MES'
		        WHEN  p.FREQ = 'D' THEN 'DIARIA'
		        WHEN  p.FREQ = 'C' THEN 'BISSEMANAL'
		        WHEN  p.FREQ = 'E' THEN 'QUINZENAL'
		        WHEN  p.FREQ = 'G' THEN 'BIENAL'
		        ELSE p.FREQ 
            END AS frequencia, 
            p.TIT_PROPRIO, 
            p.TITULO_ABREVIADO, 
            p.COD_CCN,
            p.COD_ISSN,
            p.HOME_PAGE,
            CASE
           	WHEN p.SIT_PUBL='D' THEN 'D'
           	ELSE 'C'
           	END AS situacao,
            pt.TITULO_COMPLETO, 
            pd.DESIGNACAO, 
            e.NOME, l.DES , 
            l.UF_COD,
            p2.DES 
        FROM ccn.publicacao p, 
            ccn.PUBLICACAO_TITULO pt , 
            ccn.PUBLICACAO_DESIGNACAO pd,
            ccn.PUBLICACAO_IMPRENTA pub_i, 
            ccn.EDITORA e , 
            ccn.LOCALIDADE l,
            ccn.PAIS p2 
        WHERE
            pt.PUBL_COD=p.COD 
            AND TITULO_COMPLETO IS NOT NULL 
            AND pd.PUBL_COD=p.COD 
            AND pub_i.PUBL_COD = p.COD 
            AND e.COD = pub_i.EDTO_COD 
            AND l.COD = pub_i.MUNI_COD
            AND p2.COD = p.PAI_COD
            AND'''
        
        for i,k1 in enumerate(valor):
            if(k1):
                if (i>0):
                    consulta=consulta+f'''{juncao[i]}'''

                if (tipo[i]=='tituloproprio'):
                    consulta=consulta+f''' contains(idx_clob,' {k1} within {tipo[i]}')>0 '''
                else:
                    consulta=consulta+f''' regexp_like({tipo[i]},'{k1}', 'i') '''
        consulta = consulta+f''' AND p.COD ={codigo} ORDER BY tit_proprio;'''
        return self.__class__.objects.using('primary').raw(consulta)


class Universidades(models.Model):
    seq = models.IntegerField(primary_key=True)
    conteudo = models.CharField(max_length=500)
    uf_cod = models.CharField(max_length=100)
    sigla = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    des = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    publ_cod = models.CharField(max_length=100)

    def select (self,codigo):
        consulta = '''SELECT pc.SEQ , pc.CONTEUDO, l.UF_COD, b.SIGLA, b.NOME, b.LOGRADOURO, b.BAIRRO, l.DES, b.CEP, PUBL_COD FROM ccn.PUBLICACAO_COLECAO pc, ccn.BIBLIOTECA b, ccn.LOCALIDADE l WHERE PUBL_COD = '''+codigo+''' AND b.COD = pc.BIBL_COD AND l.COD = b.MUNI_COD  ORDER BY l.UF_COD, b.SIGLA ;'''
        return self.__class__.objects.using('primary').raw(consulta)

class Assuntos(models.Model):
    cod = models.IntegerField(primary_key=True)
    assunto = models.CharField(max_length=100)

    def select (self,codigo):
        consulta = '''SELECT p.COD,WM_CONCAT(DES) AS assunto FROM ccn.PUBLICACAO p, ccn.SPINES s, ccn.PUBLICACAO_SPINES ps WHERE p.COD = '''+codigo+''' AND ps.PUBL_COD = p.COD AND s.COD = ps.SPIN_COD GROUP BY p.COD ;'''
        return self.__class__.objects.using('primary').raw(consulta)
        
    


