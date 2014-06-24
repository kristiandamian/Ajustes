function dtpConfig(){
            $( ".datepicker" ).datepicker({
                firstDay: 1,
                dateFormat: 'dd/mm/yy',
                monthNames: ['Enero', 'Febrero', 'Marzo',
                'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre',
                'Octubre', 'Noviembre', 'Diciembre'],
                dayNamesMin: ['Dom', 'Lun', 'Mar', 'Mier', 'Jue', 'Vie', 'Sab']
            });
            
            $('#ui-datepicker-div').css("font-size",".9em");            
            $('.errorlist').css("color","red");
            $('ul').css("list-style-type","none");
}