import peewee as pw

crearDataBase = pw.SqliteDatabase('obras_urbanas.db')

class BaseModel(pw.Model):
    class Meta:
        database = crearDataBase

crearDataBase.connect()




#crear bbdd
from peewee import*
sqlite_crear = SqliteDatabase('/importar_csv_a_base_datos/obras_urbanas.db',
    pragmas={'journal_mode': 'wal'})

#conexion con except OperationalError 
try:
    sqlite_crear.connect()
except OperationalError as e:
    print("Error al conectar la bbdd.",e)
    exit()

#definicion del modelo_orm
class BaseModel(Model):
    class Meta:
        database = sqlite_crear

# ARCHIVO EXCEL CSV ESTRUCTURA CONTIENE LA INFORMACION  PARA LA CLASE OBRA  
class Obra(BaseModel):
    nombre = str
    etapa = str
    #indica tipo de obra
    tipo = str
    descripcion = str
    monto_contrato = int
    comuna = int
    barrio = str
    direccion = str
    #creo que es la forma de cargar fecha  año mes y dia
    from datetime import date
    fecha_inicio = date 
    fecha_fin_inicial = date
    plazo_meses = int
    mano_obra = int
    
    #DE LA PARTE REQUERIMIENTOS HASTA EL PUNTO 3
    
#mapear class obra a tabla 
sqlite_crear.create_tables([Obra])#(QUIZAS VA DENTRO DEL MODULO GESTIONAR_OBRAS.PY, PUNTO 4/C)





