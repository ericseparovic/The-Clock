import sqlite3

sql_tabla_empresas = '''
CREATE TABLE IF NOT EXISTS EMPRESAS(
ID_EMPRESA INTEGER PRIMARY KEY, 
NOMBRE TEXT NOT NULL,
TELEFONO TEXT NOT NULL,
ID_USUARIO INTEGER,
FOREIGN KEY (ID_USUARIO) REFERENCES USUARIOS (ID_USUARIO)
)
'''

sql_tabla_empleados = '''
CREATE TABLE IF NOT EXISTS EMPLEADOS(
ID_EMPLEADO INTEGER PRIMARY KEY, 
DOCUMENTO TEXT NOT NULL,
NOMBRE TEXT NOT NULL,
APELLIDO TEXT NOT NULL,
GENERO TEXT NOT NULL,
FECHA_NACIMIENTO DATE NOT NULL,
TELEFONO TEXT NOT NULL,
DIRECCION TEXT NOT NULL,
ID_USUARIO INTEGER,
ID_EMPRESA INTEGER,
ID_HORARIO INTEGER,
FOREIGN KEY (ID_USUARIO) REFERENCES USUARIOS (ID_USUARIO),
FOREIGN KEY (ID_EMPRESA) REFERENCES EMPLEADOS (ID_EMPRESA)
FOREIGN KEY (ID_HORARIO) REFERENCES HORARIOS (ID_HORARIO)
)
'''

sql_tabla_usuarios = '''
CREATE TABLE IF NOT EXISTS USUARIOS(
ID_USUARIO INTEGER PRIMARY KEY, 
CORREO TEXT NOT NULL, 
CLAVE TEXT NOT NULL,
ID_ROL INTEGER,
FOREIGN KEY (ID_ROL) REFERENCES ROLES (ID_ROL)

)
'''

sql_tabla_roles = '''
CREATE TABLE IF NOT EXISTS ROLES(
ID_ROLES INTEGER PRIMARY KEY, 
TIPO TEXT NOT NULL
)
'''

sql_tabla_horarios = '''
CREATE TABLE IF NOT EXISTS HORARIOS(
ID_HORARIO INTEGER PRIMARY KEY, 
HORA_ENTRADA TIME, 
HORA_SALIDA TIME
)
'''

sql_tabla_marcas = '''
CREATE TABLE IF NOT EXISTS MARCAS(
ID_MARCA INTEGER  PRIMARY KEY, 
HORA_ENTRADA TIME,
HORA_SALIDA TIME,
FECHA DATE,
DURACION INTEGER,
INCIDENCIA_ASISTENCIA TEXT,
INCIDENCIA_HORARIO_ENTRADA,
INCIDENCIA_HORARIO_SALIDA,
ID_EMPLEADO INTEGER,
FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADOS (ID_EMPLEADO)
)
'''

sql_tabla_ausencias = '''
CREATE TABLE IF NOT EXISTS AUSENCIAS(
 ID_AUSENCIA INTEGER PRIMARY KEY,
 FECHA_AUSENCIA DATE,
 MOTIVO TEXT,
 ID_EMPLEADO INTEGER,
FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADOS (ID_EMPLEADO)
)
'''

sql_tabla_notificaciones = '''
CREATE TABLE IF NOT EXISTS NOTIFICACIONES(
 ID_NOTIFICACION INTEGER PRIMARY KEY,
 FECHA_NOTIFICACION DATE,
 HORA TIME,
 ASUNTO TEXT,
 DESCRIPCION,
 ID_EMPLEADO INTEGER,
FOREIGN KEY (ID_EMPLEADO) REFERENCES EMPLEADOS (ID_EMPLEADO)
)
'''


if __name__ == '__main__':
    try:
        print('Creando Base de datos..')
        conexion = sqlite3.connect('the_clock.db')

        print('Creando Tablas..')
        conexion.execute(sql_tabla_empresas)
        print('Creando empresa..')

        conexion.execute(sql_tabla_empleados)
        print('Creando empleados..')

        conexion.execute(sql_tabla_usuarios)
        print('Creando usuarios..')

        conexion.execute(sql_tabla_roles)
        print('Creando roles..')

        conexion.execute(sql_tabla_horarios)
        print('Creando horarios..')

        conexion.execute(sql_tabla_marcas)
        print('Creando marcas..')

        conexion.execute(sql_tabla_ausencias)
        print('Creando ausencias..')
        
        conexion.execute(sql_tabla_notificaciones)
        print('Creando notificaciones..')

        conexion.close()
        print('Creacion Finalizada.')
    except Exception as e:
        print(f'Error creando base de datos: {e}', e)
