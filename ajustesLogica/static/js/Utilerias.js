
function DatosCompletos(clase) {
    
    if (clase=="" || clase==null || clase==undefined) {
        clase="obligatorio";
    }
    var completos=true;
    $("."+clase).closest('div').removeClass("has-error");
    $("."+clase).each(function(){
        if($(this).val()==null || $(this).val().length<=0){
            completos=false;
            $(this).closest('div').addClass("has-error")
        }
    });
    if (!completos) 
        alert("Debe capturar todos los datos obligatorios");
    return completos;
}