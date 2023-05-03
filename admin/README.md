# Logueo en producción
| Rol        | Email           | Password  |
| ------------- |:-------------:| -:|
| Admin      | admin@gmail.com | admin123 |
| Operador | operador@gmail.com | operador123 |

# Carnet

- Deberia haber una carpeta admin/public/uploads donde se guardaran las imagenes de los socios.
- Se debería tener una imagen en admin/public/uploads cuyo nombre debe ser **EXACTAMENTE**: "default_photo.jpg"

# Base de datos

## Conexión:
* **Host = localhost**
* **Puerto = 5432**
* **Username = postgres**
* **Contraseña = proyecto**

## Filas/tuplas que agregar a las tablas desde pgadmin u otro administrador de base de datos:

**Tabla "Configuracion_general":**
* Crear una tupla con la configuración del sistema

**Tabla "Configuracion_paginado":** 
* Crear una tupla con la configuración de paginado

**Tabla "Usuarios:**

* Al menos un usuario cuya contraseña se debe almacenar con el siguiente hash que es para la contraseña **admin123**:
sha256$3avTC9Ehs6jgGDl6$de25a296fd1ba76933c0c994eb0fb617b78b9352339927cc09504ec6341ce758

**Tabla "Permisos":**
Agregar los siguientes permisos siguiendo la sintaxis modulo_accion (por ejemplo: usuario_index, disciplina_new):

* usuario: index, new, update, destroy
* disciplina: index, new, update, destroy
* socio: index, new, update, destroy
* pago: index, pay, download
* configuración: index, update

**Tabla "Roles":**
* Rol que represente a un administrador, DEBE llamarse: "ROL_ADMINISTRADOR"
* Rol que represente a un operador: "rol operador"

**Tabla "Permiso_Rol":**
Crear tuplas que relacionen a los roles de la siguientes formas:

* Permisos del rol de operador
  * Para socio, disciplina, permisos de: index, new, update
  * Para usuario, permisos de: index
  * Para pago: index, pay, download

* Permisos del rol de administrador: 
  * Todos los permisos de operador
  * Ademas para socio y disciplina permisos de: destroy
  * Para usuario: new, update, destroy
  * Para configuración: index, update

**Tabla "Usuario_Rol":**
* Relacionar al menos un usuario con el rol admin
* Relacionar un usuario con el rol operador