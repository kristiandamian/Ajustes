class Configuracion(object):
    LOGIN_URL='/ajustes/login/'

    PANTALLA_INICIO='/ajustes/'

    CORREO_CARTERAS='kristiandamian@gmail.com'#'ajustescarteras@coppel.com'
    SMTP_SERVER='10.33.128.98'
        
    MAX_DAYS_DIFF=16
    DAYS_DIFF=7
    
    @staticmethod
    def NombreCentro(centro):
        nomCentro={1:"Muebles",2:"Ropa",3:"Cajas"}
        return nomCentro[centro]