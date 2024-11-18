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

    class Meta:
        db_table = 'Etapa'

class Empresa(BaseModel):
    idEmpresa = AutoField()
    licitacionOfertaEmpresa = CharField()
    licitacionAnio = IntegerField()
    tipoContratacion = CharField()
    cuitContratista = CharField()
    areaContratacion = CharField()
    numeroContratacion = IntegerField()

    class Meta:
        db_table = 'Empresa'

class Barrio(BaseModel):
    idBarrio = AutoField()
    nombre = CharField()
    comuna = CharField()

    class Meta:
       db_table = 'Barrio'

class TipoObra(BaseModel):
    idTipoObra = AutoField()
    nombre = CharField(unique = True)
    
    class Meta:
       db_table = 'TipoObra'

class AreaResponsable(BaseModel):
    idAreaResponsable = AutoField()
    nombre = CharField()

    class Meta:
       db_table = 'AreaResponsable'

class Ubicacion(BaseModel):
    idUbicacion = AutoField()
    idBarrio = ForeignKeyField(Barrio, backref='barrio')
    direccion = CharField()
    latitud = FloatField()
    longitud = FloatField()

    class Meta:
       db_table = 'Ubicacion'

class Obra(BaseModel):
    idObra = AutoField()
    nombre = CharField()
    idTipoObra = ForeignKeyField(TipoObra, backref='tipoObra')
    idAreaResponsable = ForeignKeyField(AreaResponsable, backref='areaResponsable') 
    idUbicacion = ForeignKeyField(Ubicacion, backref='ubicacion') 
    fechaInicio = DateField() 
    fechaFinIinicial = DateField()
    plazoMeses = IntegerField() 
    manoObra = IntegerField() 
    idEtapa = ForeignKeyField(Etapa, backref='etapa') 
    numeroExpediente = IntegerField() 
    porcentajeAvance = IntegerField() 
    montoContrato = IntegerField() 
    descripcion = CharField()

    class Meta:
       db_table = 'Obra'

class EmpresaObra(BaseModel):
    idEmpresa = ForeignKeyField(Empresa, backref='empresa')
    idObra = ForeignKeyField(Obra, backref='obra')

    class Meta:
       db_table = 'EmpresaObra'
