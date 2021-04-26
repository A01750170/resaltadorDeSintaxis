import re
import dominate
from dominate.tags import *
#Creacion de los léxicos
variables = ""
operadores = ""
enteros = ""
flotante = ""
strings = ""
comentarios = ""
comentariosMult = ""
palabrasReservadas = ""
lexico = [variables,operadores,enteros,flotante,strings,comentarios,comentariosMult,palabrasReservadas]
#Se lee el archivo y se guardan las expresiones
with open("expresiones.txt","r") as archivo:
    expresiones = archivo.readlines()
    i = 0
    for expresion in expresiones:
        lexico[i] = expresion.rstrip()
        i += 1
archivo.close()

doc = dominate.document(title='Resaltador de sintaxis de Python')

with doc.head:
    link(rel='stylesheet', href='estilo.css')
    meta(charset = "UTF-8")
    meta(name = "viewport", content = "width= device-width, initial-scale= 1")

with doc:
    body(cls = "estilo")
    with open("input.txt","r",encoding = "utf8") as input:
        lineas = input.readlines()
        i=0
        for linea in lineas:
            with div():
                attr(cls='estilo')
                lineas[i] = linea.rstrip()
                palabras = lineas[i].rsplit()
                j = 0
                #Verifica el inicio de la linea
                if lineas[i].startswith('"""') or lineas[i].startswith("'''") or lineas[i].startswith("#"):
                    if (re.match(lexico[5],lineas[i])):
                        span(lineas[i],cls = "comentarios")
                    elif (re.match(lexico[6],lineas[i])):
                        span(lineas[i],cls = "comentariosMult")                    
                elif lineas[i].startswith("'") or lineas[i].startswith('"'):
                    if (re.match(lexico[4],lineas[i])):
                        span(lineas[i],cls = "strings")
                else:
                    #palabras.append("")
                    for palabra in palabras:
                        if (re.match(lexico[1],palabra)):
                            span(palabra,cls = "operadores")
                        elif (re.match(lexico[2],palabra)):
                            span(palabra,cls = "enteros")
                        elif (re.match(lexico[3],palabra)):
                            span(palabra,cls = "flotante")
                        elif(re.match(lexico[7],palabra)):
                            span(palabra, cls = "palabrasReservadas")
                        elif(re.match(lexico[4],palabra)):
                            span(palabra,cls = "strings")
                        else:
                            try:
                                #Revisa si la palabra es una variable y si la palabra siguiente es un operador
                                if (re.match(lexico[0],palabra) and re.match(lexico[1],palabras[j+1])):
                                    span(palabra,cls = "variables")
                                #Revisa si la palabra es una variable y si la palabra anterior es una PR
                                elif(re.match(lexico[0],palabra) and re.match(lexico[7],palabras[j-1])):
                                    span(palabra,cls = "variables")
                                #Si no es ninguno
                                else:
                                    span(palabra)
                            except Exception as e:
                                try:
                                    #Revisa si la palabra es una variable y si la palabra anterior es un operador
                                    if (re.match(lexico[0],palabra) and re.match(lexico[1],palabras[j-1])):
                                        span(palabra,cls = "variables")
                                    #Si no es ninguno
                                    else:
                                        span(palabra)    
                                except Exception as e:
                                    span(palabra)
                        j += 1
            i += 1
        #for linea in lineas
    input.close()
html = open("resaltadorSintaxis.html","w",encoding = "utf8")
html.write(str(doc))
html.close()