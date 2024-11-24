from peewee import *

sqlite_crear = SqliteDatabase('obras_urbanas.db',
    pragmas={'journal_mode': 'wal'})

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
    nombre = CharField(unique=True, null=False, max_length=30, constraints=[Check('length(nombre) > 0')])

    class Meta:
        db_table = 'Etapa'

class Empresa(BaseModel):
    idEmpresa = AutoField()
    licitacionOfertaEmpresa = CharField(null=False, max_length=150, constraints=[Check('length(licitacionOfertaEmpresa) > 0')])
    licitacionAnio = IntegerField(null=False, constraints=[Check('licitacionAnio >= 2010')])
    tipoContratacion = CharField(null=False, max_length=100, constraints=[Check('length(tipoContratacion) > 0')])
    cuitContratista = CharField(null=False, unique=True, max_length=11, constraints=[Check('length(cuitContratista) == 11')])
    areaContratacion = CharField(null=False, max_length=100, constraints=[Check('length(areaContratacion) > 0')])
    numeroContratacion = IntegerField(null=False, unique=True)

    class Meta:
        db_table = 'Empresa'

class Barrio(BaseModel):
    idBarrio = AutoField()
    nombre = CharField(null=False, unique=True, max_length=100, constraints=[Check('length(nombre) > 0')])
    comuna = CharField(null=False, max_length=4, constraints=[Check('length(comuna) > 0')])

    class Meta:
       db_table = 'Barrio'

class TipoObra(BaseModel):
    idTipoObra = AutoField()
    nombre = CharField(unique=True, null=False, max_length=100, constraints=[Check('length(nombre) > 0')])
    
    class Meta:
       db_table = 'TipoObra'

class AreaResponsable(BaseModel):
    idAreaResponsable = AutoField()
    nombre = CharField(unique=True, null=False, max_length=100, constraints=[Check('length(nombre) > 0')])

    class Meta:
       db_table = 'AreaResponsable'

class Ubicacion(BaseModel):
    idUbicacion = AutoField()
    idBarrio = ForeignKeyField(Barrio, backref='barrio')
    direccion = CharField(null=False, max_length=150, constraints=[Check('length(direccion) > 0')])
    latitud = FloatField()
    longitud = FloatField()

    class Meta:
       db_table = 'Ubicacion'

class Obra(BaseModel):
    idObra = AutoField()
    nombre = CharField(null=False, max_length=200, constraints=[Check('length(nombre) > 0')])
    idTipoObra = ForeignKeyField(TipoObra, backref='tipoObra')
    idAreaResponsable = ForeignKeyField(AreaResponsable, backref='areaResponsable') 
    idUbicacion = ForeignKeyField(Ubicacion, backref='ubicacion') 
    fechaInicio = DateField(null=False) 
    fechaFinIinicial = DateField(null=False)
    plazoMeses = IntegerField(null=False, constraints=[Check('plazoMeses > 0')])
    manoObra = IntegerField(null=False, constraints=[Check('manoObra >= 0')])
    idEtapa = ForeignKeyField(Etapa, backref='etapa') 
    numeroExpediente = IntegerField(null=False, unique=True)
    porcentajeAvance = IntegerField(null=False, constraints=[Check('porcentajeAvance >= 0 AND porcentajeAvance <= 100')])
    montoContrato = IntegerField(null=False, constraints=[Check('montoContrato >= 0')])
    descripcion = CharField(null=False, max_length=500, constraints=[Check('length(descripcion) > 0')])

    class Meta:
       db_table = 'Obra'

class EmpresaObra(BaseModel):
    idEmpresa = ForeignKeyField(Empresa, backref='empresa')
    idObra = ForeignKeyField(Obra, backref='obra')

    class Meta:
       db_table = 'EmpresaObra'
