
function sortNumber(a,b) {
    return b-a;
}
 
function FormatoMoneda(cellClass) {
        $("."+cellClass).each(function(){
            var decimales="0";
            var monto="";
            var formateado="";
            if ($(this).text().split(".").length>1) {
                decimales=$(this).text().split(".")[1];
                if (decimales.length>2) {
                    decimales=decimales.substring(0,2);
                }
            }
            monto=$(this).text().split(".")[0];
            var posiciones=0;
            for (var x=monto.length-1;x>=0;x--) {
                if (posiciones>=3) {
                    formateado=","+formateado;
                    posiciones=0
                }
                formateado=monto.charAt(x)+formateado;
                posiciones++;
            }
            $(this).text(formateado+"."+decimales);    
        });
}
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