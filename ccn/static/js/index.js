console.log($('.append'))
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