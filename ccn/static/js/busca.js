$('.novaConsulta').click(function(){
    // $('.tabelaResultado').css('visibility','hidden')
    window.location.replace("/")
});

$( document ).ready(function() {
    url = new URL(window.location);
    const params = new URLSearchParams(url.search)
    for(var value of params) {
        if(value[0]=='qtdItens'){
            params.delete('qtdItens')
            window.location.href = window.location.origin+window.location.pathname+'?'+params.toString()
        }
    }
});

$('#qtdItens').change(function(){
    cache =  window.location.href
    window.location.href = window.location.href + '&qtdItens='+$('#qtdItens option:selected').text();
})