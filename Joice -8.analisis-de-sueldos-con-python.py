#!/usr/bin/env python
# coding: utf-8

# # Análisis de sueldos con Python

# ## Data
# 
# * [2021.2 - sysarmy - Encuesta de remuneración salarial Argentina
# ](https://docs.google.com/spreadsheets/d/1-ZRznwS4TK74o90aOiCKS5SiXxUQ2buN1wxZIMHQmzQ/edit#gid=557755710) 
# * [2021.2 - sysarmy - Encuesta de remuneración salarial Latam
# ](https://docs.google.com/spreadsheets/d/1BkBNt1MHVS7DeIlpgmK9l6krtSQ5t_olRhlcyxMeKy0/edit#gid=557755710)

# 1. Descargar, leer y unir en una sola estructura de datos. ¿Qué estructura elegiste y por qué?
# 
# Como estructura general elegi una lista de diccionarios en los que voy a guardar la información de cada encuestado. 
# La lista me resulta una estructura fácil de recorrer y con varias funciones que permiten manejar facilmente los datos y los diccionarios me parecen una estructura que me permite tener claramente identificados los datos de cada persona.
# 

# In[1]:


dolar_conversion = (
  ('Argentina', 130.9),
  ('Bolivia', 6.86),
  ('Chile', 920.5773255),
  ('Colombia', 4445.01),
  ('Cuba', 24),
  ('Costa Rica', 671.4261825),
  ('Ecuador', 1),
  ('El Salvador', 8.75),
  ('Guatemala', 7.745829),
  ('Honduras', 24.6341828),
  ('México', 20.433),
  ('Nicaragua', 35.85),
  ('Panamá', 1),
  ('Paraguay', 6919.66395),
  ('Perú', 3.940374),
  ('Puerto Rico', 1),
  ('República Dominicana', 54.3192),
  ('Uruguay', 41.6290475),
  ('Venezuela', 5.7456)
)


# In[2]:


# Convertí la tupla en un diccionario porque me queda mejor manejarlo
dict_conversion = dict (dolar_conversion)


# In[3]:


import operator # para poder usar una función que ordena un diccionario 
from unidecode import unidecode # para poder convertir strings, sacarles tildes y cambiar ñ por n
from statistics import median


# In[4]:


#FUNCION CONVERTIR string a NUMERO

#PODRIA USAR EXPRECIONES REGULARES ME DIJO VALE - ESTUDIAR

def string_to_float (string):
    """ Esta funcion recibe un string y devuelve un float, tomar en cuenta que si el string tiene un . 
    lo va a considerar como separador de miles y lo va a sacar y si tiene una , la va a considerar como separador de decimales 
    y la va a cambiar por un . """
    
    numero = 0
  
    str_num = ''
    for elemento in string:
        if elemento.isdigit() or elemento == '.' or elemento == ',':
            if elemento == '.':
                elemento =''
                
            elif elemento == ',':
                elemento = '.'       
            
            str_num = str_num + elemento
            
    if ',,' in str_num or '..' in str_num:
        for letra in str_num:
            if letra == ',':
                str_num = str_num - letra
        
    if str_num != '':
        if str_num != '.' and str_num != '..':
            numero = float (str_num)
    else:
        numero = 0
        
   
    return (numero)


# In[5]:


# Arreglando la estructura de datos de Argentina (agregando el pais)

dic_info_arg = {} 
lista_cabezales_final_arg = [] 
list_info_arg =[] 
list_data_arg = [] 


with open('Argentina.tsv', encoding='utf-8') as data_argentina:
    for index, info in enumerate(data_argentina):
   
        if index == 9:
            lista_cabezales_final_arg = info.split ('\t')
             
        elif index >=9:
            list_info_arg = info.split ('\t')          
            dic_info_arg = dict(zip(lista_cabezales_final_arg, list_info_arg)) # con la funcion zip hago un diccionario entre los datos de mi mi lista info y mi lista de keys lista de cabezales bien
            dic_info_arg ['Region'] = dic_info_arg ['Dónde estás trabajando']
            del dic_info_arg ['Dónde estás trabajando'] 
            dic_info_arg ['Estoy trabajando en'] = 'Argentina'
            list_data_arg.append(dic_info_arg) #agrego a mi lista principal el diccionario



# In[6]:


# Arreglando la estructura de datos de LATAM
list_data_latam = []
dic_info = {}           

with open('Latam.tsv', encoding='utf-8') as data_latam:
    for index, info in enumerate(data_latam):
       
        if index == 10: # pongo 10 y no 9 por mas que este en la fila 9 porque empieza a contar desde 0 
            lista_cabezales_final = info.split ('\t')
            lista_cabezales_final [1:19] = ["Region"]
            
        elif index >10:
            list_info = info.split ('\t')
            i = 1
            while not list_info[i]: # mientras no haya info en la lista con indice i sigue hasta encontrar la region
                i += 1
            region = list_info [i]
            list_info [1:19] = [region] # le asigno a todas los indices (del 1 al 19) en los que estaban los paises solo la region que corresponde
            dic_info = dict(zip(lista_cabezales_final, list_info))
            
            dic_info ['Region'] = region
            list_data_latam.append(dic_info) #agrego a mi lista principal el diccionario      


# In[7]:


#Uniendo datos Argentina y Latam
list_data_latam.extend (list_data_arg)
 


# In[8]:


# DEFINICIÓN DE VARIABLES Y ESTRUCTURAS

# Punto 2
dic_regiones = {} # diccionario que tiene como clave la region y como valor un int que corresponde a la cantidad de veces que esta la region, la uso para calcular el porcentaje por region

# Punto 3
dic_roles = {}
list_roles_ordenada = []

# DEPURAR LOS ROLES 
# cree una lista de listas en la que cada elemento de mi lista es un string con los roles que quieren decir lo mismo
# y están escritos diferentes, tome como criterio que en la posición 0 voy a poner como quiero que quede unficada esos 
# roles en la que unifique los roles, tomando 

list_roles_depurados = [['ingenieria en sistemas de información', 'ingenieria en informatica', 'ingenieria en computacion'],['integrator', 'integration developer', 'integration '],['jefe de sistemas','encargado área de sistemas','jefe división informática','jefe de área de sistemas','jefe de it'],['qa - automation engineer','qa automation', 'qa automation '],['responsable it', 'responsable de área de sistemas '],['security research', 'security researcher'],['seguridad informática','seguridad informática ','seguridad informatica','seguridad informática - accesos','seguridad'],['software engineer', 'software ingeniero','software engineer '],['team leader', 'team lead'],['ui', 'ui '],['trainee etl', 'trainee'],['soporte técnico', 'technical support (not help desk)', 'technical support','técnico', 'soporte tecnico','soporte','soporte it'],['administracion','administración','administrativo','administrativo ','administrativa','administrativa '], ['analista de sistemas', 'analista de sistema'], ['analista funcional','analisis funcional', 'analista funcional',  'analista funcional ', 'analista funcional de sistemas', 'analista funcional sr', 'analista funcional y coordinadora de grupo de mantenimiento '],['cybersecurity', 'cybersecurity ','cyber security'], ['auditor', 'auditoria','auditoría'], ['de todo','de todo un poco'], ['fullstack','full stack developer'],['developer','programador', 'developer, devops', 'developer/devops', 'devops'], ['docencia', 'instructor','profesor de tecnología de la información', 'profesor de informática', 'teacher','docente', 'docente universitario', 'education', 'profesor'] ]


# Punto 4
Contribuis_a_proyectos_open_source = 0
no_contribuye = 0
contribuye_mal_escrito = 0
no_contesta_contribuye = 0
Programas_por_hobbie = 0
no_programas_por_hobbie = 0
no_contesta_programas_por_hobbie = 0
programas_hobbie_mal_escrito = 0 

# Punto 5
junior = 0 
semi_senior = 0
senior = 0      

# Punto 6
hasta_2_comp = 0 
de_2_a_5_comp = 0
mas_5_comp = 0
entre_5_7_comp = 0
entre_7_10_comp = 0
entre_10_15_comp = 0 
mas_15_comp = 0

hasta_2_puesto = 0 
de_2_a_5_puesto = 0
mas_5_puesto = 0
entre_5_7_puesto = 0
entre_7_10_puesto = 0
entre_10_15_puesto = 0 
mas_15_puesto = 0

# Punto 7
dic_educacion = {} 

# Punto 8
dic_carreras = {}

# Punto 9
dic_identidad = {} # la primera clave va a ser la identidad de genero y el valor un entero que cuenta la cantidad de personas 
#con esa identidad y la segunda la palabra 'media y la indentidad' como clave y como valor una lista con los sueldos de esa identidad
dic_identidad1 = {}
# dic_disc = {}
contador_disc = 0

# Punto 10
dic_sueldos_region = {} # diccionario que tiene como clave la region y como valor lista con los sueldos que corresponden a esa region, la utilizo para calcular la media
dic_sueldos_rol = {} # clave rol valor lista con los sueldos
dic_sueldos_exp = {
    'mas_5_comp':[],
    '2_5': [],
    'menos_2': []
} 

dic_sueldos_form = {} # clave el nivel de estudios alcanzado y como valores una lista que esta formaa por 4 listas # primera lista valor, lista con los sueldos de cada nivel educativo y despues y en orden: lista de sueldos con formacion completo, incompleto y en curso

dic_media_sueldos_genero = {} # como clave va a tener el genero y como valor va a tener una lista con los salarios de ese genero

hasta_2_comp_media = []
de_2_a_5_comp_media = []
mas_5_comp_media = []
entre_5_7_comp_media = []
entre_7_10_comp_media = []
entre_10_15_comp_media = []
mas_15_comp_media = []

hasta_2_puesto_media = []
de_2_a_5_puesto_media = []
mas_5_puesto_media = []
entre_5_7_puesto_media = []
entre_7_10_puesto_media = []
entre_10_15_puesto_media = []
mas_15_puesto_media = []
 


# In[9]:


# Formateando datos y creando estructuras para poder realizar el análisis


for elemento in list_data_latam:
    elemento['Salario mensual o retiro BRUTO (en tu moneda local)'] = string_to_float(elemento['Salario mensual o retiro BRUTO (en tu moneda local)'])
    elemento['Salario mensual o retiro NETO (en tu moneda local)'] = string_to_float(elemento['Salario mensual o retiro NETO (en tu moneda local)'])
    elemento ['¿Qué tan conforme estás con tu sueldo?'] = int (elemento ['¿Qué tan conforme estás con tu sueldo?'])
    elemento ['Cómo creés que está tu sueldo con respecto al último semestre'] = int (elemento ['Cómo creés que está tu sueldo con respecto al último semestre'])
    elemento ['¿De qué % fue el ajuste total?'] = float (elemento ['¿De qué % fue el ajuste total?'])
    elemento ['Años de experiencia'] = float (elemento ['Años de experiencia']) # tuve que poner float y no int porque habia respuestas del tipo 3.5
    elemento ['Años en la empresa actual'] = float (elemento ['Años en la empresa actual']) # idem anterior
    elemento ['Años en el puesto actual'] = float (elemento ['Años en el puesto actual']) # idem anterior
    elemento ['¿Gente a cargo?'] = int(float (elemento ['¿Gente a cargo?'])) # no me parece que quede como float por mas que haya algun campo que dice 1.5                                             
    elemento ['¿Tenés hijos/as menores de edad?'] = int(string_to_float(elemento['¿Tenés hijos/as menores de edad?'] ))
    elemento [ 'Trabajo de'] = elemento[ 'Trabajo de'].lower() 
    elemento ['Sueldo en dolares'] = elemento ['Salario mensual o retiro NETO (en tu moneda local)'] / dict_conversion [elemento ['Estoy trabajando en']]
    #creo una clave sueldo en dolares 
    
    #ver si solucionar pago en dolares asi o directamente a todos pasarlos de la moneda local dividiendo por la cotizacion
    if elemento ['Pagos en dólares'] != '' :
            if elemento ['¿Cuál fue el último valor de dólar que tomaron?'] != '':
                elemento ['Pagos en dólares'] = string_to_float (elemento ['Pagos en dólares'])
            else:
                elemento['Pagos en dólares'] = string_to_float (elemento ['¿Cuál fue el último valor de dólar que tomaron?']) * elemento['Salario mensual o retiro NETO (en tu moneda local)']
    else:
        elemento['Pagos en dólares'] = elemento ['Salario mensual o retiro BRUTO (en tu moneda local)'] / dict_conversion[elemento['Estoy trabajando en']]

# Punto 2
    # hago este for para depurar los roles de mi lista _latam 
    for i, rol in enumerate (list_roles_depurados):
        if elemento['Trabajo de'].lower() in rol:            
            elemento['Trabajo de'] = list_roles_depurados [i][0].capitalize () # tomo como convencion que en el lugar 0 de mi lista de depurados voy a poner el nombre correcto
    dic_regiones[elemento['Region']] = 0

#Punto 10
  
    #agrego un item al diccionario para calcular la ultima parte mediana de sueldo por region, 
    #voy a poner todos los sueldos de esta region en una lista
    dic_sueldos_region[elemento['Region']]= []
    dic_sueldos_rol[elemento['Trabajo de']]= [] # aqui es para agregar las claves para hacer sueldo por rol
    dic_media_sueldos_genero [elemento['Me identifico\n']] = [] # aqui es para agregar las claves para hacer sueldo por identificacion sexual
    

# Punto 3
   
    dic_roles[elemento['Trabajo de']] = 0  #creo las claves, una para cada rol
    
# Punto 4    

    if elemento['¿Contribuís a proyectos open source?'].lower() == 'si' or elemento['¿Contribuís a proyectos open source?'].lower() == 'sí':
        Contribuis_a_proyectos_open_source +=  1 
        
    elif elemento['¿Contribuís a proyectos open source?'].lower() == 'no':
        no_contribuye +=  1 
    elif elemento['¿Contribuís a proyectos open source?'].lower() != '':
        contribuye_mal_escrito += 1
    elif elemento['¿Contribuís a proyectos open source?'] == '':
        no_contesta_contribuye += 1
    
    # pregunto por la parte de '¿Programás como hobbie?'   
    if elemento['¿Programás como hobbie?'].lower() == 'si' or elemento['¿Programás como hobbie?'].lower() == 'sí':
        Programas_por_hobbie +=  1      
    elif elemento['¿Programás como hobbie?'].lower() == 'no':
        no_programas_por_hobbie +=  1 
    elif elemento['¿Programás como hobbie?'].lower() != '':
        programas_hobbie_mal_escrito += 1
    elif elemento['¿Programás como hobbie?'] == '':
        no_contesta_programas_por_hobbie += 1

# Punto 5
    if elemento['Años de experiencia'] < 2 :
        junior += 1
        dic_sueldos_exp['menos_2'].append(elemento['Sueldo en dolares']) # punto 10 
    elif elemento['Años de experiencia'] >= 2 and elemento['Años de experiencia'] < 5 :
        semi_senior += 1 
        dic_sueldos_exp['2_5'].append(elemento['Sueldo en dolares']) # punto 10
    elif elemento['Años de experiencia'] >= 5:
        senior += 1
        dic_sueldos_exp['mas_5_comp'].append(elemento['Sueldo en dolares']) # punto 10
        
# Punto 6 


    if elemento['Años en la empresa actual'] > 15:
        mas_15_comp += 1
        mas_15_comp_media.append(elemento['Sueldo en dolares']) 
        
    elif elemento['Años en la empresa actual'] > 10 :
        entre_10_15_comp += 1
        entre_10_15_comp_media.append(elemento['Sueldo en dolares'])
        
    elif elemento['Años en la empresa actual'] > 7 :
        entre_7_10_comp += 1
        entre_7_10_comp_media.append(elemento['Sueldo en dolares'])
        
    elif elemento['Años en la empresa actual'] > 5 :
        mas_5_comp += 1
        entre_5_7_comp_media.append(elemento['Sueldo en dolares'])
    
    elif elemento['Años en la empresa actual'] > 2 :
        de_2_a_5_comp += 1  
        de_2_a_5_comp_media.append(elemento['Sueldo en dolares'])
        
    elif elemento['Años en la empresa actual'] <= 2 :
        hasta_2_comp += 1   
        hasta_2_comp_media.append(elemento['Sueldo en dolares'])
    
    if elemento['Años en el puesto actual'] > 15:
        mas_15_puesto += 1
        
    elif elemento['Años en el puesto actual'] > 10 :
        entre_10_15_puesto += 1
        
    elif elemento['Años en el puesto actual'] > 7 :
        entre_7_10_puesto += 1
            
    elif elemento['Años en el puesto actual'] > 5 :
        mas_5_puesto += 1
    
    
    elif elemento['Años en el puesto actual'] > 2 :
        de_2_a_5_puesto += 1  
          
    elif elemento['Años en el puesto actual'] <= 2 :
        hasta_2_puesto += 1 


# Punto 7
#creando las claves de mi diccionario de educacion

    dic_educacion[elemento['Nivel de estudios alcanzado']] = [0,0,0,0] 
    # primer valor, cuantos hay de cada nivel educativo y después y en orden:
    #cuantos hay completo, incompleto y en curso 
    dic_sueldos_form[elemento['Nivel de estudios alcanzado']] = [[],[],[],[]] 
    # primer valor, lista con los sueldos de cada nivel educativo y después y en orden:
    # lista de sueldos con formacion completo, incompleto y en curso

# Punto 8


    carrera = elemento ['Carrera'].lower()
    if 'lic ' in carrera:
        elemento['Carrera'] = carrera.replace('lic ', "Licenciatura ")
    elif 'lic. ' in carrera:
        elemento['Carrera'] = carrera.replace('lic. ', "Licenciatura ")
    elif 'tec ' in carrera:
        elemento['Carrera'] = carrera.replace('tec ', 'Tecnicatura ')
    elif 'tec. ' in carrera:
        elemento['Carrera'] = carrera.replace('tec. ', 'Tecnicatura ')
    elif 'cs ' in carrera:
        elemento['Carrera'] = carrera.replace('cs ', 'Ciencias ')
    elif 'cs. ' in carrera:
        elemento['Carrera'] = carrera.replace('cs. ', 'Ciencias ')
    elif 'ed ' in carrera:
        elemento['Carrera'] = carrera.replace('ed ', 'Educación ')
    elif 'ed. ' in carrera:
        elemento['Carrera'] = carrera.replace('ed. ', 'Educación ')
    
    elemento['Carrera'] =  unidecode(elemento['Carrera'])
    elemento['Carrera'] = elemento['Carrera'].capitalize()
    
    dic_carreras[elemento['Carrera']] = 0
    
# Punto 9
    identidad =  unidecode(elemento['Me identifico\n'].lower())
    dic_identidad[identidad] = 0
#     dic_disc[elemento['¿Tenés algún tipo de discapacidad?']] = 0
    if elemento['¿Tenés algún tipo de discapacidad?'] != '':
        contador_disc += 1


# En otro for en list_data_latam cargo los datos de las claves creadas en los diccionarios
for dato in list_data_latam:

# Punto 2 
    dic_regiones[dato['Region']] +=  1 # cuento cuantas veces aparece la region
    
    dic_sueldos_region[dato['Region']].append(dato['Sueldo en dolares']) # Punto 10
    dic_sueldos_rol[dato['Trabajo de']].append(dato['Sueldo en dolares']) # Punto 10
        
# Punto 3
    # recorro lista_latam para sumar 1 por cada vez que aparece el rol
    dic_roles[dato['Trabajo de']] = dic_roles[dato['Trabajo de']] + 1

  
    
# Punto 7
    #contando cada nivel
    dic_educacion[dato['Nivel de estudios alcanzado']] [0] += 1
    dic_sueldos_form[dato['Nivel de estudios alcanzado']][0].append(dato['Sueldo en dolares'])
    
    # primer valor, cuantos hay de cada nivel educativo y despues y en orden:
    #cuandos hay completo, incompleto y en curso y por ultimo no contesta 
    
    if dato['Estado'].lower () == 'completado':
        dic_educacion[dato['Nivel de estudios alcanzado']] [1] += 1
        dic_sueldos_form[dato['Nivel de estudios alcanzado']] [1].append(dato['Sueldo en dolares'])                                                     
    elif dato['Estado'].lower () == 'incompleto':
        dic_educacion[dato['Nivel de estudios alcanzado']] [2] += 1
        dic_sueldos_form[dato['Nivel de estudios alcanzado']] [2].append(dato['Sueldo en dolares'])  
    elif dato['Estado'].lower () == 'en curso':
        dic_educacion[dato['Nivel de estudios alcanzado']] [3] += 1
        dic_sueldos_form[dato['Nivel de estudios alcanzado']] [3].append(dato['Sueldo en dolares']) 
        
# Punto 8
    dic_carreras[dato['Carrera']] += 1

# Punto 9

# en el diccionario dic_media_sueldos_genero unifique aqui los datos de varon en uno solo y borre las claves.
# en dic_identidad lo hice en el punto 9
    identidad1 =  unidecode(dato['Me identifico\n'].lower())
    dic_identidad[identidad1] += 1
    if identidad1 == 'varon' or identidad1 ==  'varon cis' or identidad == 'masculino\n' or identidad == 'hombre\n' or identidad == 'varon\n' or identidad == 'varon \n' :
        if dato['Sueldo en dolares'] > 100 and dato['Sueldo en dolares'] < 10000: #defini agregar solamente los sueldos mayores a 100 dolares y menores a 10000
            dic_media_sueldos_genero['Varón Cis\n'].append(dato['Sueldo en dolares'])
        
    elif dato['Sueldo en dolares'] > 100 and dato['Sueldo en dolares'] < 10000:
        dic_media_sueldos_genero [dato['Me identifico\n']].append(dato['Sueldo en dolares']) 
    
del dic_media_sueldos_genero ['Varón Cis']
del dic_media_sueldos_genero ['Masculino\n']
del dic_media_sueldos_genero ['Hombre\n']
del dic_media_sueldos_genero ['Varón\n']
del dic_media_sueldos_genero ['Varón \n']
del dic_media_sueldos_genero ['Varon\n']
    
    
 
    
 


# 2. Printear porcentaje de participación por región, ordenado de mayor a menor. Ej: 
# 
# ```
# - Ciudad Autónoma de Buenos Aires - 59.4%
# - Formosa - 0.04%
# ```

# In[10]:


# Convierto el diccionario en una lista ordenada en este caso por el item 1 que son la cantidad de personas que son de esa region

list_regiones_ordenado = sorted(dic_regiones.items(), key=operator.itemgetter(1), reverse=True)


for region in list_regiones_ordenado:
    porcentaje_participacion = region[1] * 100 / len(list_data_latam)
    print (f' {region[0]} - {porcentaje_participacion:.2f}%')


# 3. Printear porcentaje de participación por tipo de rol, ordenado de mayor a menor. Ej:  
# `- Developer - 39.11 %`

# In[11]:


# Tome la decisión de mostrar los roles con mas de 1%

list_roles_ordenada = sorted(dic_roles.items(), key=operator.itemgetter(1), reverse=True)
print ('Rol y porcentaje de participación\n')

for rol1 in list_roles_ordenada:
    porcentaje_participacion_roles = rol1[1] * 100 / len(list_data_latam)
    if porcentaje_participacion_roles >= 1 :
        print (f' {rol1[0].capitalize()} - {porcentaje_participacion_roles:.2f}%')


# 4. Printear porcentaje de respuesta para las preguntas: 
# * ¿Contribuís a proyectos Open Source?
# * ¿Programás por hobbie?

# In[12]:



porcentaje_contribuye = Contribuis_a_proyectos_open_source * 100 / len(list_data_latam) 
porcentaje_contribuye_neto = Contribuis_a_proyectos_open_source * 100 / (len(list_data_latam) - no_contesta_contribuye)

# Si bien esta información no la solicitaba me pareció interesante tenerla sobre quienes habían contestado que NO contribuían
porcentaje_no_contribuye_neto = no_contribuye * 100 / (len(list_data_latam) - no_contesta_contribuye)

porcentaje_programa_por_hobbie = Programas_por_hobbie * 100 / len(list_data_latam) 
porcentaje_programa_por_hobbie_neto = Programas_por_hobbie * 100 / (len(list_data_latam) - no_contesta_programas_por_hobbie )

# Esta información si bien no la pedíaa pero me pareció interesante tenerla sobre quienes habian contestado quienes NO programan por hobbie
porcentaje_no_contesta_hobbie = no_contesta_programas_por_hobbie * 100 / (len(list_data_latam) - no_contesta_programas_por_hobbie )

print(f'Contribuyen a proyectos Open Source {Contribuis_a_proyectos_open_source} personas que es un {porcentaje_contribuye:.2f}% del total y un {porcentaje_contribuye_neto:.2f}% de quienes contestaron')
print(f'Programan por hobbie {Programas_por_hobbie} personas que es un {porcentaje_programa_por_hobbie:.2f}% del total y un {porcentaje_programa_por_hobbie_neto:.2f}% de quienes contestaron')


# 5. Printear porcentaje por seniority según años de experiencia, el mapeo es:
# ```
# Junior: de 0 hasta 2 años.
# Semi-Senior: de 2 años inclusive hasta 5 años.
# Senior: desde 5 años inclusive.
# ``` 

# In[13]:



porcentaje_junior = junior * 100 / len(list_data_latam)
porcentaje_semi_senior = semi_senior * 100 / len(list_data_latam)
porcentaje_senior = senior * 100 / len(list_data_latam)

print(f'Junior: de 0 hasta 2 años: {porcentaje_junior:.2f}%')
print(f'Semi-Senior: de 2 años inclusive hasta 5 años: {porcentaje_semi_senior:.2f}%')
print(f'Senior: mas de 5 años inclusive: {porcentaje_senior:.2f}%')


# 6. Printear porcentaje de personas encuestadas por años en la compañía actual y por años en el puesto actual.

# In[14]:




    
porc_hasta_2_comp = hasta_2_comp * 100 / len(list_data_latam)
porc_de_2_5_comp = de_2_a_5_comp * 100 / len(list_data_latam)
porc_entre_5_7_comp = mas_5_comp * 100 / len(list_data_latam)
porc_entre_7_10_comp = entre_7_10_comp * 100 / len(list_data_latam)
porc_entre_10_15_comp = entre_10_15_comp * 100 / len(list_data_latam)
porc_mas_15_comp = mas_15_comp * 100 / len(list_data_latam)

porc_hasta_2_puesto = hasta_2_puesto * 100 / len(list_data_latam)
porc_de_2_5_puesto = de_2_a_5_puesto * 100 / len(list_data_latam)
porc_entre_5_7_puesto = mas_5_puesto * 100 / len(list_data_latam)
porc_entre_7_10_puesto = entre_7_10_puesto * 100 / len(list_data_latam)
porc_entre_10_15_puesto = entre_10_15_puesto * 100 / len(list_data_latam)
porc_mas_15_puesto = mas_15_puesto * 100 / len(list_data_latam)

print('Información de porcentaje por año en la compañía actual \n')
print(f'Menos de 2 años -- {porc_hasta_2_comp:.2f}%')
print(f'2 a 5 años -- {porc_de_2_5_comp:.2f}%')
print(f'5 - 7 años -- {porc_entre_5_7_comp:.2f}%')
print(f'7 a 10 años -- {porc_entre_7_10_comp:.2f}%')
print(f'10 a 15 años -- {porc_entre_10_15_comp:.2f}%')
print(f'Mas de 15 años -- {porc_mas_15_comp:.2f}%')
print('-----------')

print('Información de porcentaje por año en el puesto actual \n')

print(f'Menos de 2 años -- {porc_hasta_2_puesto:.2f}%')
print(f'2 a 5 años -- {porc_de_2_5_puesto:.2f}%')
print(f'5 - 7 años -- {porc_entre_5_7_puesto:.2f}%')
print(f'7 a 10 años -- {porc_entre_7_10_puesto:.2f}%')
print(f'10 a 15 años -- {porc_entre_10_15_puesto:.2f}%')
print(f'Más de 15 años -- {porc_mas_15_puesto:.2f}%')


# 7. Printear porcentajes de nivel de educación formal y estado, es decir: % educación secundaria, terciaria, universitaria, postgrado, doctorado, postdoctorado, completo, incompleto y en curso para cada uno.

# In[15]:


no_contestan_edu = dic_educacion[''] [0]
del dic_educacion['']

for d in dic_educacion.items():
    porcentaje_por_nivel_gral = d[1][0] * 100 / len(list_data_latam)
    porcentaje_por_nivel_neto = d[1][0] * 100 / (len(list_data_latam) - no_contestan_edu)
    porcentaje_completo = d[1][1] * 100 / d[1][0]
    porcentaje_incompleto = d[1][2] * 100 / d[1][0]
    porcentaje_en_curso = d[1][3] * 100 / d[1][0]
    print (f' El nivel {d[0]}, es un {porcentaje_por_nivel_gral:.2f}% del total general y un {porcentaje_por_nivel_neto:.2f}% de los que contestaron')
    print (f''' Dentro del nivel {d[0]}:
    Completo: {porcentaje_completo:.2f}% 
    Incompleto: {porcentaje_incompleto:.2f}%
    En curso: {porcentaje_en_curso:.2f}%''' )


# 8. Formatear las carreras universitarias:
# - Nombres capitalizados
# - Reemplazar vocales con tilde por vocales sin tilde.
# - Reemplazar `ñ` por `n`
# - *lic*, *lic.* por Licenciatura
# - *tec*, *tec.* por Tecnucatura
# * *cs, *cs.* por Ciencias
# * *ed, ed.* por Educación
# * Transformaciones que se consideren necesarias
# 
# Printear porcentaje según carrera

# In[16]:


# tome la decision de printear las carreras con  porcentaje mayor a 1%

no_contesta_carrera = dic_carreras ['']
del dic_carreras ['']
list_carreras_ordenada = sorted(dic_carreras.items(), key=operator.itemgetter(1), reverse=True)


for carrera in list_carreras_ordenada:
    porcentaje_carrera = carrera[1] * 100 / len(list_data_latam)
    porcentaje_carrera_neto = carrera[1] * 100 / no_contesta_carrera
   # hago un if para solo printear los datos cuyo porcentaje es mayor a 1%
    if porcentaje_carrera_neto > 1:
        print (f' {carrera[0].capitalize()} - {porcentaje_carrera:.2f}% del total y un {porcentaje_carrera_neto:.2f}% de quienes contestaron\n')
    


# 9. Printear porcentaje por identidad de género y personas con discapacidad

# In[17]:


# Uniendo valores que significan lo mismo
 
dic_identidad['varon cis\n'] = dic_identidad['varon \n'] + dic_identidad['varon cis\n'] + dic_identidad ['varon cis']+ dic_identidad['masculino\n'] + dic_identidad['varon\n']+ dic_identidad['hombre\n'] 

del dic_identidad ['varon cis']
del dic_identidad ['masculino\n']
del dic_identidad ['hombre\n']
del dic_identidad ['varon\n']
del dic_identidad ['varon \n']


# Tome la decision de mostrar aquellos que tienen mas de 10 registros porque habia muchas respuestas que desvirtuaban la informacion, quedaron fuera del analisis 130 registros
for i in dic_identidad.items():
    if i[1] > 10:
        dic_identidad1[i[0]] = i[1] # creo 

list_identidad_ordenada = sorted(dic_identidad1.items(), key=operator.itemgetter(1), reverse=True)    

print('Identidad de género -- porcentaje sobre el total')

for identidad in list_identidad_ordenada:
    porcentaje_identidad = identidad[1] * 100 / len(list_data_latam)
    print(f'{identidad[0].capitalize()} --> {porcentaje_identidad:.2f}%')
print('-----------')
porcentaje_discapacidad = contador_disc * 100 / len(list_data_latam)
print (f'El porcentaje de personas con discapacidad es de un {porcentaje_discapacidad:.2f}%')


# 10. Salarios: calcular la mediana salarial para cada una de las siguientes categorías:
# - Salario según región
# - Salario por rol
# - Salario por experiencia
# - Salario por nivel de formación
# - Salario por género
# 
# **TIP:** Podemos utilizar la biblioteca statics
# 
# ```
# import statistics
# 
# # unsorted list of random integers
# data1 = [2, -2, 3, 6, 9, 4, 5, -1]
#  
#  
# # Printing median of the
# # random data-set
# print("Median of data-set is : % s "
#         % (statistics.median(data1)))
# 
# ```

# In[18]:


# MEDIA DE SALARIOS POR REGION
# Tome como criterio no mostrar la media de sueldos mayores a 20000 ni los menores a 100

print('Region ---- Media de sueldos en dólares --- Cantidad de personas\n')

# for sueldo in dic_sueldos_region.items():
#     media_sueldo_region = median (sueldo[1])  
#     print(f'{sueldo[0]} -- {media_sueldo_region:.2f} ')
dic_region_media_sueldo = {}
for sueldo in dic_sueldos_region.items():
    media_sueldo_region = median (sueldo[1])  
    dic_region_media_sueldo [ sueldo[0]] = media_sueldo_region
list_reg_med_sueldo_ord =  sorted(dic_region_media_sueldo.items(), key=operator.itemgetter(1), reverse=True)       

for d in list_reg_med_sueldo_ord:
    if d[1] < 20000 and d[1] > 100:
        print(f'{d[0]} -- U$S {d[1]:.2f} -- {len(dic_sueldos_region[d[0]])} ')


# In[19]:


# MEDIA DE SALARIOS POR REGION 
#(IGUAL QUE LA ANTERIOR PERO AGREGUE EL CRITERIO DE SOLO MOSTRAR LOS QUE TIENEN MAS DE 10 RESPUESTAS)
# Tome como criterio no mostrar la media de sueldos mayores a 20000 ni los menores a 100 y solo los que tienen mas de 10 registros de respuesta

print('Region ---- Media de sueldos en dólares --- Cantidad de personas\n')

dic_region_media_sueldo = {}
for sueldo in dic_sueldos_region.items():
    if len (sueldo[1]) > 10:
        media_sueldo_region = median (sueldo[1])  
        dic_region_media_sueldo [ sueldo[0]] = media_sueldo_region
list_reg_med_sueldo_ord =  sorted(dic_region_media_sueldo.items(), key=operator.itemgetter(1), reverse=True)       

for d in list_reg_med_sueldo_ord:
    if d[1] < 20000 and d[1] > 100:
        print(f'{d[0]} -- U$S {d[1]:.2f} -- {len(dic_sueldos_region[d[0]])} ')


# In[20]:


# MEDIA DE SALARIOS POR ROL ordenada por sueldo
print('Media de sueldos en dólares por rol y cantidad de personas en ese rol\n')

dic_sueldos_rol_ordenado = {}    
for sueldo1 in dic_sueldos_rol.items():
    media_sueldo_rol = median (sueldo1[1])  
    dic_sueldos_rol_ordenado [sueldo1[0]] = media_sueldo_rol
    

list_sueldos_rol_ordenado = sorted(dic_sueldos_rol_ordenado.items(), key=operator.itemgetter(1), reverse=True)
for i in list_sueldos_rol_ordenado:
    print(f'{i[0].capitalize()} -- U$S {i[1]:.2f} -- {len(dic_sueldos_rol[i[0]])} persona(s)')
    


# In[21]:


# Listado de rol y sueldo en aquellos roles que superan las 10 personas para que la muestra sea representativa
dic_sueldos_rol_ordenado_1 = {} 
for i in dic_sueldos_rol.items():
     if len(i[1]) > 10:
        media_rol_persona = median (i[1])
        dic_sueldos_rol_ordenado_1[i[0]] = media_rol_persona
    
print ('Rol -- Media de sueldo -- Cantidad de personas')
list_sueldos_rol_ordenado1 = sorted(dic_sueldos_rol_ordenado_1.items(), key=operator.itemgetter(1), reverse=True)
for i in list_sueldos_rol_ordenado1:
    print(f'{i[0].capitalize()} -- U$S {i[1]:.2f} -- {len(dic_sueldos_rol[i[0]])} persona(s)')

      


# In[22]:


# Salario por experiencia

print('Experiencia -- media de sueldos en dólares \n')


for sueldo2 in dic_sueldos_exp.items():
    media_sueldo_exp = median(sueldo2[1])
    if sueldo2[0] == 'mas_5_comp':
        print(f'Mas de 5 años -- U$S {media_sueldo_exp:.2f}' )
    elif sueldo2[0] == '2_5':
        print(f'Entre 2 y 5 años -- U$S {media_sueldo_exp:.2f}' )
    elif sueldo2[0] == 'menos_2':
        print(f'Menos de 2 años -- U$S {media_sueldo_exp:.2f}' )
        
        
        


# In[23]:


# salario por experiencia con otro rango de años.
print('Experiencia -- Media de sueldos en dólares \n')

valor_hasta_2_comp_media = median (hasta_2_comp_media)
valor_de_2_a_5_comp_media = median (de_2_a_5_comp_media)
valor_entre_5_7_comp_media = median (entre_5_7_comp_media)
valor_entre_7_10_comp_media = median(entre_7_10_comp_media)
valor_entre_10_15_comp_media = median (entre_10_15_comp_media)
valor_mas_15_comp_media = median(mas_15_comp_media)

print(f'Menos de 2 años -- {valor_hasta_2_comp_media:.2f}')
print(f'Entre 2 y 5 años -- {valor_de_2_a_5_comp_media:.2f}')
print(f'Entre 5 y 7 años -- {valor_entre_5_7_comp_media:.2f}')
print(f'Entre 7 y 10 años -- {valor_entre_7_10_comp_media:.2f}')
print(f'Entre 10 y 15 años -- {valor_entre_10_15_comp_media:.2f}')
print(f'Más de 15 años -- {valor_mas_15_comp_media:.2f}')


# In[24]:


#Salario por nivel de formación


# RECORDAR QUE dic_sueldos_form tiene como clave el nivel y como valores una lista que esta formaa por 4 listas # primera lista valor, lista con los sueldos de cada nivel educativo y despues y en orden:
    # lista de sueldos con formacion completo, incompleto y en curso

print('Nivel de formación -- Media de sueldos en dólares \n')

del dic_sueldos_form [''] # borro la clave vacia para que no me aparezca.

for sueldo3 in dic_sueldos_form.items():
    
    # tengo que hacer los if porque si la lista es vacia el calculo de median da error, tome como criterio que hubiera por lo menos 10 registros
    if len(sueldo3[1][0]) > 10: # en sueldo3 [1] [0] tengo la lista de todos los sueldos con determinado nivel de estudios alcanzado. 
        media_sueldo_form = median(sueldo3[1][0])
    else:
        media_sueldo_form = 0
        
        
    if len(sueldo3[1][1]) > 10: # en sueldo3 [1] [1] tengo la lista de los sueldos con nivel de formacion completo. 
        media_sueldo_form_comp = median(sueldo3[1][1])
    else:
        media_sueldo_form_comp = 0
        
    if len(sueldo3[1][2]) > 10: # en sueldo3 [1] [2] tengo la lista de los sueldos en los que la formacion esta incompleto. 
        media_sueldo_form_incomp = median(sueldo3[1][2]) # en sueldo3 [1] [2] tengo la lista de los sueldos en los que la formacion esta incompleto. 
    else:
        media_sueldo_form_incomp = 0
        
    if len(sueldo3[1][3]) > 10: # en sueldo3 [1] [3] tengo la lista de los sueldos en los que la formacion esta en curso.     
        media_sueldo_form_en_curso = median(sueldo3[1][3])
    else:
        media_sueldo_form_en_curso = 0
    
# Defini hacer otro if para mostrar los que tienen suficientes datos
    
    if media_sueldo_form > 0:
        print (f' {sueldo3[0].upper()}, U$S { media_sueldo_form:.2f}--- {len(sueldo3[1][0])} personas')
              
        print (f'   Dentro del nivel {sueldo3[0]} la media del sueldo según el estado de la formación es:')
           
        if media_sueldo_form_comp > 0:
            print(f'     Completo: U$S {media_sueldo_form_comp:.2f} - {len(sueldo3[1][1])} personas')
        else:
            print('     Completo: No hay datos suficientes para que la muestra sea representativa')
        if media_sueldo_form_incomp > 0:
            print(f'     Incompleto: U$S {media_sueldo_form_incomp:.2f} - {len(sueldo3[1][2])} personas')
        else:
            print('     Incompleto: No hay datos suficientes para que la muestra sea representativa')
        if media_sueldo_form_en_curso:
            print(f'     En curso: U$S {media_sueldo_form_en_curso:.2f} - {len(sueldo3[1][3])} personas' )
        else:
            print('     En curso: No hay datos suficientes para que la muestra sea representativa')
    else:
        print(sueldo3[0].upper(), 'no existen datos suficientes para que la muestra sea representativa')
    print('-------------')
        
    
    


# In[25]:


# Media de salario tomando en cuenta el género

dic_media_genero_ord = {}

for i in dic_media_sueldos_genero.items():
    if len(i[1])> 10:
        media_sueldo_identificacion = median (i[1])
        dic_media_genero_ord [i[0]] = [media_sueldo_identificacion]
        dic_media_genero_ord [i[0]].append(len(i[1]))


list_dic_media_sueldos_genero = sorted(dic_media_genero_ord.items(), key=operator.itemgetter(1), reverse=True)
for i in list_dic_media_sueldos_genero:
    print(f'{i[0]} ----{i[1][0]:.2f}, cantidad personas: {i[1][1]}')


# 11. En base a los resultados obtenidos confeccionar conclusiones respecto a:
# 
# - Rol vs sueldos
# - Nivel de educación alcanzada vs sueldos
# - Género vs sueldos

# # Conclusiones
# 
# 
# # Análisis de sueldo por región.
# 
# La media de sueldo más alta por región (Montevideo) es 3,5 veces mayor que la media de sueldo más baja por región (Misiones)
# 
# En las primeras 3 regiones la media de sueldo no tiene mucha variación, en las siguientes regiones baja sensiblemente. 
# 
# 
# # Análisis tomando en cuenta la cantidad de años en el puesto actual y en la compañía actual.
# 
# El 67% de las personas ha estado menos de 2 años en la compañía actual, lo que da la pauta de que es un rubro con gran movilidad. 
# 
# Porcentajes similares se dan en la permanencia en el puesto actual, el cambio es la constante en este rubro, tanto de compañía como de puesto.
# 
# # Análisis tomando en cuenta la experiencia
# 
# Los media de sueldos más alto esta en la franja de 5 a 7 años de experiencia. 
# 
# El menor sueldo lo tiene los junior (menos de 2 años de experiencia), pero no se da la misma relación con quienes tienen más experiencia, ya que no obtienen la media de salarios más alta.
# 
# Entre quienes tienen la media de salario más baja (menos de 2 años de experiencia) y quienes tienen la media de salario más alta (entre 5 y 7 años de experiencia) hay un 16% de diferencia.
# La experiencia es un factor importante en la diferencia de sueldos pero no es el determinante.
# 
# 
# # Análisis tomando en cuenta el género. 
# 
# Las mujeres son las que perciben menor remuneración a pesar ocupar el segundo lugar en porcentaje de participación, su sueldo se ubica en el quinto escalón.
# 
# Más del 75% de los puestos de trabajo son ocupados por hombres.
# 
# # Análisis de sueldos por rol
# 
# Los media de sueldos del rol mejor pago (Vp / c-level ) es 4,7 veces mayor que la media de sueldo más baja (Soporte Técnico). Tomando en cuenta la información significativa es decir con un mínimo de 10 respuestas.
# 
# 
# 
# # Análisis tomando en cuenta la formación
# 
# 
# Tener la formación incompleta no parece influir directamente en la remuneración. (No se detecta una aumento significativo en la remuneración con quienes tienen la formación completa). 
# 
# Mas del 68% de quienes contestaron a la pregunta sobre su formación tienen un nivel universitario. 
# (El nivel Universitario, es un 34.63% del total general y un 68.50% de los que contestaron.)
# 
# 
# 
# 

# 12. Generar gráficos de barra para mostrar los resultados mencionados anteriormente usando strings, ej:
# 
# ```
# developer | -----------------------------------------------
# sysadmin  | ---------------------------
# QA        | ------------------
#           | ..................5%.......10%...............40%
# ```

# ![Media%20Sueldo%20por%20region.jpg](attachment:Media%20Sueldo%20por%20region.jpg)

# ![Media%20sueldos%20por%20rol.jpg](attachment:Media%20sueldos%20por%20rol.jpg)

# ![Media%20Sueldo%20por%20genero.jpg](attachment:Media%20Sueldo%20por%20genero.jpg)

# ![Porcentaje%20por%20a%C3%B1o%20en%20la%20comp%20actual.jpg](attachment:Porcentaje%20por%20a%C3%B1o%20en%20la%20comp%20actual.jpg)

# ![media%20sueldo%20por%20formacion1.jpg](attachment:media%20sueldo%20por%20formacion1.jpg)

# ![%25%20personas%20en%20el%20puesto%20y%20compa%C3%B1ia%20actual.jpg](attachment:%25%20personas%20en%20el%20puesto%20y%20compa%C3%B1ia%20actual.jpg)

# ![genero%20sobre%20el%20total.jpg](attachment:genero%20sobre%20el%20total.jpg)

# ![media%20de%20sueldos%20por%20experiencia.jpg](attachment:media%20de%20sueldos%20por%20experiencia.jpg)

# Resultados de la encuesta: https://sueldos.openqube.io/encuesta-sueldos-2021.02/
