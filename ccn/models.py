from django.db import models
import urllib

class Postagens_titulo(models.Model):
    codigo = models.IntegerField(primary_key=True)
    titulo_completo = models.CharField(max_length=100)
    def get_titulo_completo (self,codigo):
        consulta = f'''SELECT p.COD as codigo, pt.TITULO_COMPLETO FROM ccn.PUBLICACAO p ,ccn.PUBLICACAO_TITULO pt WHERE p.COD = pt.PUBL_COD AND pt.PUBL_COD IN ({codigo}) AND pt.TITULO_COMPLETO IS NOT NULL;'''
        return consulta


class Postagens(models.Model):
    codigo = models.IntegerField(primary_key=True)
    frequencia = models.CharField(max_length=100)
    tit_proprio = models.CharField(max_length=100)
    titulo_abreviado = models.CharField(max_length=100)
    cod_ccn = models.CharField(max_length=100)
    cod_issn = models.CharField(max_length=100)
    cod_issn_online = models.CharField(max_length=100)
    home_page = models.CharField(max_length=100)
    situacao = models.CharField(max_length=100)
    designacoes = models.CharField(max_length=100)
    imprentas = models.TextField(max_length=100)
    pais = models.CharField(max_length=100)
    idioma = models.CharField(max_length=100)
    assunto = models.CharField(max_length=100)
    titulo_adicional = models.CharField(max_length=100)
    titulo_completo = models.CharField(max_length=100)

    def select (self,tipo,valor,juncao,codigo):
        consulta = f'''
            SELECT DISTINCT
            p.COD as codigo ,
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
            p.TIT_PROPRIO as ,
            p.TITULO_ABREVIADO as titulo_abreviado,
            p.COD_CCN as cod_ccn,
            p.COD_ISSN as cod_issn,
            p.COD_ISSN_L as cod_issn_online,
            p.HOME_PAGE as home_page,
            CASE WHEN p.SIT_PUBL='D' THEN 'N SEI' 
            ELSE p.SIT_PUBL END AS situacao,
            WM_CONCAT(DISTINCT pd.DESIGNACAO || '$$') AS designacoes,
            CASE l.UF_COD WHEN 'XX' THEN
            WM_CONCAT(DISTINCT l.DES || ', ' || p.PAI_COD ||': '|| e.NOME || '$$')
            ELSE (SELECT WM_CONCAT(DISTINCT l.DES || ', ' || l.UF_COD ||': '|| e.NOME || '$$')
            FROM ccn.publicacao p
            LEFT JOIN ccn.PUBLICACAO_TITULO pt ON pt.PUBL_COD=p.COD AND pt.TIPO = '01'
            INNER JOIN ccn.PUBLICACAO_DESIGNACAO pd
            ON p.COD=pd.PUBL_COD
            INNER JOIN ccn.PUBLICACAO_IMPRENTA pub_i
            ON p.COD = pub_i.PUBL_COD
            INNER JOIN ccn.EDITORA e
            ON pub_i.EDTO_COD = e.COD
            INNER JOIN ccn.LOCALIDADE l
            ON pub_i.MUNI_COD = l.COD
            WHERE contains(idx_clob,'102250-4 within codccn')>0) END AS imprentas,
            p2.DES AS pais,
            WM_CONCAT(DISTINCT i.DES) AS idioma,
            WM_CONCAT(DISTINCT s.DES) AS assunto,
            pt.TITULO as titulo_adicional
            FROM ccn.publicacao p LEFT JOIN ccn.PUBLICACAO_TITULO pt
            ON pt.PUBL_COD=p.COD AND pt.TIPO = '01'
            INNER JOIN ccn.PUBLICACAO_DESIGNACAO pd
            ON p.COD=pd.PUBL_COD
            INNER JOIN ccn.PUBLICACAO_IMPRENTA pub_i
            ON p.COD = pub_i.PUBL_COD
            INNER JOIN ccn.EDITORA e
            ON pub_i.EDTO_COD = e.COD
            INNER JOIN ccn.LOCALIDADE l
            ON pub_i.MUNI_COD = l.COD
            INNER JOIN ccn.PAIS p2
            ON p.PAI_COD = p2.COD
            INNER JOIN ccn.PUBLICACAO_IDIOMA pi2
            ON p.COD = pi2.PUBL_COD
            INNER JOIN ccn.IDIOMA i
            ON pi2.IDIO_COD = i.COD
            INNER JOIN ccn.PUBLICACAO_SPINES ps
            ON p.COD=ps.PUBL_COD
            INNER JOIN ccn.SPINES s
            ON ps.SPIN_COD = s.COD
            WHERE '''

        for i,k1 in enumerate(valor):
            if(k1):
                if (tipo[i]=='tituloproprio'):
                    consulta=consulta+f''' contains(idx_clob,' {k1} within {tipo[i]}')>0 '''
                elif (tipo[i]=='s.DES'):
                    consulta=consulta+f''' UPPER({tipo[i]}) LIKE UPPER('{k1}') '''
                else:
                    consulta=consulta+f''' regexp_like({tipo[i]},'{k1}', 'i') '''

                if (juncao[i-1]=='OR'):
                    posicao = (30+len(k1)+29+(len(valor[i-1])))*-1
                    consulta = consulta[:posicao]+'('+consulta[posicao:]+') '
                
                if (juncao[i]=='NOT'):
                    consulta=consulta+f'''AND'''

                if (i<(len(valor)-1)):
                    consulta=consulta+f''' {juncao[i]} '''

        if (codigo!=''):
            consulta = consulta+f''' AND p.COD in ({codigo}) '''
        
        consulta = consulta+f'''
            GROUP BY p.COD, p2.DES,p.FREQ,p.TIT_PROPRIO,p.TITULO_ABREVIADO,p.COD_CCN,p.COD_ISSN,
            p.COD_ISSN_L, p.HOME_PAGE,p.SIT_PUBL,p2.DES,pt.TITULO,l.UF_COD,p.PAI_COD
            ORDER BY tit_proprio
        '''
        # consulta = '''
        # SELECT 
        #     p.COD AS codigo , 
        #         CASE
		#         WHEN p.FREQ = 'F' THEN 'SEMESTRAL'
		#         WHEN p.FREQ = 'M' THEN 'MENSAL'
		#         WHEN p.FREQ = 'Q' THEN 'TRIMESTRAL'
		#         WHEN p.FREQ = 'B' THEN 'BIMESTRAL'
		#         WHEN p.FREQ = 'S' THEN 'BIMENSAL'
		#         WHEN p.FREQ = '?' THEN 'DESCONHECIDO' 
		#         WHEN  p.FREQ = 'A' THEN 'ANUAL'
		#         WHEN  p.FREQ = 'T' THEN 'QUADRIMESTRAL'
		#         WHEN  p.FREQ = 'K' THEN 'IRREGULAR'
		#         WHEN  p.FREQ = 'Z' THEN 'OUTRAS'
		#         WHEN  p.FREQ = 'W' THEN 'SEMANAL'
		#         WHEN  p.FREQ = 'H' THEN 'TRIENAL'
		#         WHEN  p.FREQ = 'I' THEN 'TRÊS VEZES NA SEMANA'
		#         WHEN  p.FREQ = 'J' THEN 'TRÊS VEZES NO MES'
		#         WHEN  p.FREQ = 'D' THEN 'DIARIA'
		#         WHEN  p.FREQ = 'C' THEN 'BISSEMANAL'
		#         WHEN  p.FREQ = 'E' THEN 'QUINZENAL'
		#         WHEN  p.FREQ = 'G' THEN 'BIENAL'
		#         ELSE p.FREQ 
        #         END AS frequencia, 
        #     p.TIT_PROPRIO, 
        #     p.TITULO_ABREVIADO, 
        #     p.COD_CCN,
        #     p.COD_ISSN,
        #     p.HOME_PAGE,
        #     CASE
        #    	    WHEN p.SIT_PUBL='D' THEN 'D'
        #    	    ELSE 'C'
        #         END AS situacao, 
        #     WM_CONCAT(DISTINCT pd.DESIGNACAO || '$$') AS designacoes, 
        #     CASE l.UF_COD WHEN 'XX' THEN 
        #     WM_CONCAT(DISTINCT l.DES || ', ' || p.PAI_COD ||': '|| e.NOME || '$$')
        #     ELSE
        #     WM_CONCAT(DISTINCT l.DES || ', ' || l.UF_COD ||': '|| e.NOME || '$$')
        #     END AS imprentas, 
        #     p2.DES AS pais,
        #     WM_CONCAT(DISTINCT i.DES) AS idioma,
        #     WM_CONCAT(DISTINCT s.DES) AS assunto,
        #     pt.TITULO AS titulo_adicional
        # FROM ccn.publicacao p
        #     LEFT JOIN ccn.PUBLICACAO_TITULO pt
        # 		ON pt.PUBL_COD=p.COD AND pt.TIPO = '09'
        #     LEFT JOIN ccn.PUBLICACAO_DESIGNACAO pd
        #         ON p.COD=pd.PUBL_COD
        #     LEFT JOIN ccn.PUBLICACAO_IMPRENTA pub_i
        #         ON p.COD = pub_i.PUBL_COD
        #     LEFT JOIN ccn.EDITORA e
        #         ON pub_i.EDTO_COD = e.COD
        #     LEFT JOIN ccn.LOCALIDADE l
        #         ON pub_i.MUNI_COD = l.COD
        #     LEFT JOIN ccn.PAIS p2
        #         ON p.PAI_COD = p2.COD
        #     LEFT JOIN ccn.PUBLICACAO_IDIOMA pi2
        #         ON p.COD = pi2.PUBL_COD
        #     LEFT JOIN ccn.IDIOMA i
        #         ON pi2.IDIO_COD = i.COD
        #     LEFT JOIN ccn.PUBLICACAO_SPINES ps
        #    		ON p.COD=ps.PUBL_COD 
        #   	LEFT JOIN ccn.SPINES s
        #    		ON ps.SPIN_COD = s.COD
        #    WHERE '''

        # for i,k1 in enumerate(valor):
        #     if(k1):
        #         if (tipo[i]=='tituloproprio'):
        #             consulta=consulta+f''' contains(idx_clob,' {k1} within {tipo[i]}')>0 '''
        #         else:
        #             consulta=consulta+f''' regexp_like({tipo[i]},'{k1}', 'i') '''

        #         if (juncao[i-1]=='OR'):
        #             posicao = (30+len(k1)+29+(len(valor[i-1])))*-1
        #             consulta = consulta[:posicao]+'('+consulta[posicao:]+') '
                
        #         if (juncao[i]=='NOT'):
        #             consulta=consulta+f'''AND'''

        #         if (i<(len(valor)-1)):
        #             consulta=consulta+f''' {juncao[i]} '''
        # if (codigo!=''):
        #     consulta = consulta+f''' AND p.COD in ({codigo}) '''

        # consulta = consulta+f'''
        # GROUP BY p.COD, p2.DES,p.FREQ,p.TIT_PROPRIO,p.TITULO_ABREVIADO,p.COD_CCN,p.COD_ISSN, p.HOME_PAGE,p.SIT_PUBL, p2.DES,pt.TITULO,l.UF_COD
        # ORDER BY tit_proprio;'''
        result = consulta.find('%')
        if (result != -1):
            consulta=consulta.replace('%','%%')
        print (consulta)
        return consulta

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
        consulta = f'''SELECT pc.SEQ , pc.CONTEUDO, l.UF_COD, b.SIGLA, b.NOME, b.LOGRADOURO, b.BAIRRO, l.DES, b.CEP, PUBL_COD FROM ccn.PUBLICACAO_COLECAO pc, ccn.BIBLIOTECA b, ccn.LOCALIDADE l WHERE PUBL_COD IN ({codigo}) AND b.COD = pc.BIBL_COD AND l.COD = b.MUNI_COD  ORDER BY l.UF_COD, b.SIGLA ;'''
        return consulta
        
    


