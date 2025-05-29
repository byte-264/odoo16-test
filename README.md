# Proyecto Odoo 16 con Docker

## 📁 Estructura de directorios

```
odoo-project/
├── docker-compose.yml
├── config/
│   └── odoo.conf
├── addons/
│   └── (aquí irán tus módulos personalizados)
└── data/
```

**Config**: Contiene el archivo `odoo.conf` con la configuración del servidor Odoo (base de datos, puerto, logs, etc.).

## 🐳 ¿Qué es Docker Compose?

Docker Compose es una herramienta que permite definir y ejecutar aplicaciones multi-contenedor usando un archivo YAML. En lugar de manejar cada contenedor por separado, se define toda la aplicación en un solo archivo.

## 🏗️ Cómo funciona la configuración

### Servicios definidos:

#### 🌐 **web** (Odoo)
- **Imagen**: `odoo:16.0`
- **Puerto**: `8069` (acceso desde http://localhost:8069)
- **Dependencias**: Espera a que el servicio `db` esté listo
- **Volúmenes**:
  - `odoo-web-data`: Datos persistentes de Odoo
  - `./config`: Configuración personalizada
  - `./addons`: Módulos personalizados

#### 🗄️ **db** (PostgreSQL)
- **Imagen**: `postgres:13`
- **Base de datos**: `postgres`
- **Usuario**: `odoo`
- **Contraseña**: `myodoo`
- **Volumen**: `odoo-db-data` para persistencia de datos

## 🚀 Comandos básicos

### Iniciar la aplicación
```bash
docker-compose up -d
```
> El flag `-d` ejecuta en segundo plano (detached)

### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Solo Odoo
docker-compose logs -f web

# Solo PostgreSQL
docker-compose logs -f db
```

### Detener la aplicación
```bash
docker-compose down
```

### Reiniciar un servicio específico
```bash
docker-compose restart [nombre-del-servicio]
```

### Ver estado de los servicios
```bash
docker-compose ps
```

## 🔄 Flujo de funcionamiento

1. **Lectura del archivo**: Docker Compose lee `docker-compose.yml`
2. **Red interna**: Crea una red para que los contenedores se comuniquen
3. **Base de datos primero**: Levanta PostgreSQL
4. **Odoo después**: Inicia Odoo y lo conecta automáticamente a la DB
5. **Acceso**: Odoo queda disponible en `http://localhost:8069`

## 📋 Características importantes

- **Persistencia**: Los volúmenes guardan datos aunque elimines los contenedores
- **Reinicio automático**: `restart: unless-stopped` reinicia contenedores si fallan
- **Variables de entorno**: Configuración automática de conexión DB
- **Dependencias**: Odoo espera a que PostgreSQL esté listo

## 🔧 Primer uso

1. Clona o descarga este proyecto
2. Ejecuta: `docker-compose up -d`
3. Espera unos minutos para que se descarguen las imágenes
4. Ve a `http://localhost:8069`
5. Configura tu primera base de datos de Odoo