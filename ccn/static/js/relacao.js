$('.btnRetornar').click(function(){
    window.location.replace("/")
})

$( document ).ready(function() {
    $( ".universidade_hover" ).hover(function() {
        var info = $($(window.event.target).parents()[1]).find('#info_adicionais')
        if ($(info).css("display")=='block'){
            $(info).css("display","none")
        } else {
            $(info).css("display","block")
        }
    });
});