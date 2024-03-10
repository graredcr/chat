
import requests  
from datetime import date
import calendar

class lya2Rest:
    def __init__(self):
        print("ini")
    
    def getAuthInfo( self, token): 
        print('getAuthInfo')
        url = 'https://dev2.lya2.com/lya2git/index01.php?pag=93&rest=true'
        auth = requests.get(url, headers={'Authorization': str(token)  })  
        
        if(auth.status_code == 200):
            data    = auth.json() 
            today   = date.today()
            d1      = today.strftime("%d/%m/%Y") 
            indexdia = today.weekday();
            print("indexdiaindexdia: "+str(indexdia))
            #if indexdia < 0: 
            #    indexdia = 6
            diastring = calendar.day_name[indexdia] 

            name = data['data']['0']['nombre']+" "+data['data']['0']['apellidos'];
            nivel = data['data']['0']['acceso']

            context=[]
            context.append("Nombre del usuario  es "+name) 
            context.append("Fecha, hoy es dia "+d1+", "+str(diastring))
            context.append("Email "+data['data']['0']['email'])
            context.append("Nivel de acceso "+nivel )
            context.append("Soy staff del "+data['data']['0']['name_subcenterprincipal'])
            context.append("Identificador de usuario "+data['data']['0']['id_personal'] )
            context.append("Identificador de sylbo "+data['data']['0']['id_sylbo'] )

            return [context, name, nivel ] 

    
 