import peewee as pw

crearDataBase = pw.SqliteDatabase('obras_urbanas.db')

class BaseModel(pw.Model):
    class Meta:
        database = crearDataBase

crearDataBase.connect()
