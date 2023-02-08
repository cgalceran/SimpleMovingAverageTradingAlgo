def initialize(context):
    """
    Esta funcion es llamada una sola vez cuando el programa es iniciado.
    """   
    # Seleccionar el titulo que queremos operar
    context.titulo = symbol('MCD')
    
    #Estas son las comisiones que nos pretederian cobrar el Agente
    set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1))
         
def handle_data(context,data):
    """
    Esta función es llamada a cada minuto mientras el programa esté encendido.
    """
    # Obtencion de la serie historica de datos 
    historial = data.history(context.titulo, 'price', 200, '1d')   
    historial_50 = historial[-50:]
    historial_200= historial
    # Construccion de la media movil de corto plazo
    MM1 = historial_50.mean()
    # Construccion de la media movil de largo plazo
    MM2 = historial_200.mean()
    
    # Identificar el actual precio del titulo 
    precio_actual = data.current(context.titulo,'price')
    
    # Identificar actualmente cuantas posiciones en el título tenemos
    posiciones_actuales = context.portfolio.positions[context.titulo].amount
    
    # Identificar el efectivo que tenemos en la cuenta
    efectivo = context.portfolio.cash    
    
    # Esta es la lógica del algoritmo
    if (MM1 > MM2) and posiciones_actuales == 0:
        cantidad_de_acciones = int(efectivo/precio_actual)
        order(context.titulo,cantidad_de_acciones)
        log.info('Comprando Acciones a %s!' % (precio_actual))
   
    elif (MM1 < MM2) and posiciones_actuales != 0:
        order_target(context.titulo,0)
        log.info('Vendiendo Acciones! a %s'% (precio_actual))
    
    # Funcion que ayuda a construir el grafico segun las variables que sigamos    
    record(MM1=MM1,MM2=MM2,Price=precio_actual)