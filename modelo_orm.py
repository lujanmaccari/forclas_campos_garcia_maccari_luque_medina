from peewee import *

#crear bbdd
sqlite_crear = SqliteDatabase('obras_urbanas.db',
    pragmas={'journal_mode': 'wal'})

#conexion con except OperationalError 
try:
    sqlite_crear.connect()
except OperationalError as e:
    print("Error al conectar la bbdd.",e)
    exit()

class BaseModel(Model):
    class Meta:
        database = sqlite_crear

class Etapa(BaseModel):
    idEtapa = AutoField()
    nombre = CharField()

class Empresa(BaseModel):
    idEmpresa = AutoField()
    licitacionOfertaEmpresa = CharField()
    licitacionAnio = IntegerField()
    tipoContratacion = CharField()
    cuitContratista = IntegerField()
    areaContratacion = CharField()
    numeroContratacion = IntegerField()
    
class Ubicacion(BaseModel):
    idUbicacion = AutoField()
    barrio = CharField()
    comuna = CharField()
    direccion = CharField()
    latitud = FloatField()
    longitud = FloatField()

class TipoObra(BaseModel):
    idTipoObra = AutoField()
    nombre = CharField()

class AreaResponsable(BaseModel):
    idAreaResponsable = AutoField()
    nombre = CharField()

class Obra(BaseModel):
    idObra = AutoField()
    nombre = CharField()
    idTipoObra = ForeignKeyField(TipoObra, backref='tipoObra')
    idAreaResponsable = ForeignKeyField(AreaResponsable, backref='areaResponsable') 
    idUbicacion = ForeignKeyField(Ubicacion, backref='ubicacion') 
    destacada = BooleanField()
    fechaInicio = DateField() 
    fechaFinIinicial = DateField()
    idFuenteFinanciamiento = ForeignKeyField(Empresa, backref='fuente_financiamiento')
    plazoMeses = IntegerField() 
    manoObra = IntegerField() 
    idEtapa = ForeignKeyField(Etapa, backref='etapa') 
    numeroExpediente = IntegerField() 
    porcentajeAvance = IntegerField() 
    montoContrato = IntegerField() 
    descripcion = CharField()

class EmpresaObra(BaseModel):
    idEmpresa = ForeignKeyField(Empresa, backref='empresa')
    idObra = ForeignKeyField(Obra, backref='obra')

# sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, EmpresaObra])