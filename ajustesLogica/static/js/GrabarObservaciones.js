function Grabar() {
    if (DatosCompletos())
        GrabarAjax();
}


function GrabarAjax() {
    var observacion={
                "EsFraude":$("#EsFraude").is(":checked"),
                "Recuperacion":$("#Recuperacion").is(":checked"),
                "Observacion":$("#observacion").val(),
                "Empleado":$("#Empleado").val(),
                "NumEmpleado":$("#NumEmpleado").val(),
                "Unidad":$("#hdnUnidad").val(),
                "Fecha":$("#hdnFecha").val()
    };
    var ajax = {
        type: "POST",
        async: true,
        dataType: "JSON",
        url: "/inventario/RegistroObservacion/",
        data: observacion,
        error: function (xhr, status, error) {
            alert("Ocurrio un error: " + error + ":" + eval(xhr).responseText);
        },
        success: function () {
            alert("Observacion registrada con exito");
        }
    };
    $.ajax(ajax);
}