from peewee import *

sqlite_crear = SqliteDatabase('obras_urbanas.db',
    pragmas={'journal_mode': 'wal'})

try:
    sqlite_crear.connect()
except OperationalError as e:
    print("Error al conectar la bbdd.", e)
    exit()

class BaseModel(Model):
    class Meta:
        database = sqlite_crear

class Etapa(BaseModel):
    idEtapa = AutoField()
    nombre = CharField(unique=True, null=False, max_length=30, constraints=[Check('length(nombre) > 0')])

    class Meta:
        db_table = 'Etapas'

class Empresa(BaseModel):
    idEmpresa = AutoField()
    licitacionOfertaEmpresa = CharField(null=False, max_length=150, constraints=[Check('length(licitacionOfertaEmpresa) > 0')])
    licitacionAnio = IntegerField(null=False, constraints=[Check('licitacionAnio >= 2010')])
    cuitContratista = CharField(null=False, max_length=11, constraints=[Check('length(cuitContratista) == 11')])
    areaContratacion = CharField(null=False, max_length=100, constraints=[Check('length(areaContratacion) > 0')])

    class Meta:
        db_table = 'Empresas'

class Barrio(BaseModel):
    idBarrio = AutoField()
    nombre = CharField(null=False, unique=True, max_length=100, constraints=[Check('length(nombre) > 0')])
    comuna = IntegerField(null=False)

    class Meta:
        db_table = 'Barrios'

class TipoObra(BaseModel):
    idTipoObra = AutoField()
    nombre = CharField(unique=True, null=False, max_length=100, constraints=[Check('length(nombre) > 0')])
    
    class Meta:
       db_table = 'TipoObras'

class AreaResponsable(BaseModel):
    idAreaResponsable = AutoField()
    nombre = CharField(unique=True, null=False, max_length=100, constraints=[Check('length(nombre) > 0')])

    class Meta:
       db_table = 'AreaResponsables'

class TipoContratacion(BaseModel):
    idTipoContratacion = AutoField()
    nombre = CharField(unique=True, null=False, max_length=100, constraints=[Check('length(nombre) > 0')])

    class Meta:
        db_table = 'TipoContrataciones'

class Ubicacion(BaseModel):
    idUbicacion = AutoField()
    barrio = ForeignKeyField(Barrio, backref='barrio')
    direccion = CharField(null=False, max_length=150, constraints=[Check('length(direccion) > 0')])
    latitud = FloatField()
    longitud = FloatField()

    class Meta:
       db_table = 'Ubicaciones'

class Obra(BaseModel):
    idObra = AutoField()
    nombre = CharField(null=False, max_length=200, constraints=[Check('length(nombre) > 0')])
    empresa = ForeignKeyField(Empresa, backref='empresa')
    tipoObra = ForeignKeyField(TipoObra, backref='tipoObra')
    areaResponsable = ForeignKeyField(AreaResponsable, backref='areaResponsable') 
    ubicacion = ForeignKeyField(Ubicacion, backref='ubicacion') 
    tipoContratacion = ForeignKeyField(TipoContratacion, backref='tipoContratacion') 
    etapa = ForeignKeyField(Etapa, backref='etapa') 
    fechaInicio = DateField(null=False) 
    fechaFinIinicial = DateField(null=False)
    plazoMeses = IntegerField(null=False, constraints=[Check('plazoMeses > 0')])
    manoObra = IntegerField(null=False, constraints=[Check('manoObra >= 0')])
    numeroExpediente = CharField(null=False, unique=True)
    porcentajeAvance = IntegerField(null=False, constraints=[Check('porcentajeAvance >= 0 AND porcentajeAvance <= 100')])
    montoContrato = IntegerField(null=False, constraints=[Check('montoContrato >= 0')])
    descripcion = CharField(null=False, max_length=500, constraints=[Check('length(descripcion) > 0')])
    destacada = CharField(null=False, max_length=5)
    numeroContratacion = IntegerField(null=False)

    class Meta:
       db_table = 'Obras'
