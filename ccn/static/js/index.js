
$('#adicionarCamposDeBusca').click(function(){
    quantidade = $('.slc-chave-tipo').length
    fieldToClone = $('.campoDeBusca')[0].children[1]
    
    if ($('.append')[0].children.length==0){
        lastField=$(fieldToClone).clone().prependTo('.append');
        (lastField.find('input')).val('')
    } else {
        lastField=$(fieldToClone).clone().insertAfter('.append .row:last');
        (lastField.find('input')).val('')
    }

    if (quantidade>=4){
        $('.addCampos').css('visibility','hidden')
    }
});

function removerDiv(elemento){
    if ($('.slc-chave-tipo').length>1){
        $(elemento).parents()[4].remove();
        $('.addCampos').css('visibility','visible')
    } else {
        alert('Impossivel remover todos os elementos!');
    }
}

$('.limparFormulario').click(function(){
    campos = $('.append')[0].children
    for (i=campos.length-1;i>=0;i--){
        campos[i].remove()
    }

    $('.addCampos').css('visibility','visible')
    $('.ipt-valor').val('');
});




$('.visualizarRegistros').click(function(){
    valores = $('.tabelaResultado tr input[type=checkbox]')
    check = false
    for (i=0;i<valores.length;i++){
        if ($(valores[i]).is(":checked")){
            check=true
            posicao = $(valores[i]).parents()[1]
            // window.open("/resultado",'_blank')
            console.log(posicao)
        }
    }
    if (!check){
        alert ('Selecione algum elemento')
    }
    
})


$( document ).ready(function() {
    
});

function ajuda(elemento){
    var parents = $(elemento).parents().find('[name="tipo"] option:selected').html()
    var teste = $($(window.event.target).parents()[1]).find('[name="tipo"] option:selected').html()
    camposConsulta ={
        'Título':'Informe as palavras SIGNIFICATIVAS do título separadas por operadores boleanos ou digite o titulo completo\n\nEX:\nCiência AND informação\nou\nCiência da informação',
        'Assunto':'Informe o assunto desejado\n\nEX:\nCiênci% da informação\nou\nCiências da informação\n\nPara refinar sua busca utilize os operadores boleanos\nEX:\nAids AND neoplasmas malígnos',
        'País de publicação':'Informe o nome do país da publicação\n\nEX:\nPortugal',
        'Idioma do texto':'Informe o idioma do texto dos artigos\n\nEX:\nDinamarques',
        'Código CCN':'Informe o código da publicação no CCN\n\nEX:\n022173-2',
        'Número ISSN':'Informe o código ISSN da publicação\n\nEX:\n0100-1965',
        'Situação de publicação':'Utilize esse campo para refinar suas buscas com situação da publicação pelo código ou descrição\n\nEX:\nC ou Corrente\nD ou Suspensa\n? ou Desconhecida',
        'Local de edição/publicação':'Informe o local de edição da publicação\n\nEX:\nSalvador',
        'Editor/Publicador':'Informe o nome do editor\n\nEX:\nAcademic Press',
        'Título abreviado':'Informe as palavras SIGNIFICATIVAS do título abreiado separadas por operadores boleanos ou digite o titulo abreviado completo\n\nEX:\nCiênc. AND inf.\nou\nCiênc inf'
     }

     alert(camposConsulta[teste])
    
}

$('[name="teste"]').click(function(){
    // console.log(window.event.target)
    // console.log('aaa')
})