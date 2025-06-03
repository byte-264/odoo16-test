# 🚀 Odoo 16 con Docker

> **Sistema ERP completo** ejecutándose en contenedores Docker con PostgreSQL y módulos personalizados.

[![Odoo](https://img.shields.io/badge/Odoo-16.0-purple?logo=odoo)](https://www.odoo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue?logo=postgresql)](https://www.postgresql.org/)

---

## 📋 Tabla de Contenidos

- [🎯 Características](#-características)
- [⚡ Instalación Rápida](#-instalación-rápida)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🛠️ Comandos Útiles](#-comandos-útiles)
- [🔧 Configuración](#-configuración)
- [📦 Módulos Disponibles](#-módulos-disponibles)

---

## 🎯 Características

✅ **Odoo 16** - Última versión LTS  
✅ **PostgreSQL 13** - Base de datos robusta  
✅ **Docker Compose** - Despliegue simplificado  
✅ **Módulos OHRMS** - Sistema completo de recursos humanos  
✅ **Persistencia de datos** - Los datos se mantienen entre reinicios  
✅ **Configuración personalizable** - Fácil de adaptar a tus necesidades  

---

## ⚡ Instalación Rápida

### **Prerrequisitos**
- 🐳 [Docker](https://docs.docker.com/get-docker/) instalado
- 🔧 [Docker Compose](https://docs.docker.com/compose/install/) instalado
- 💾 Al menos 4GB de RAM libre
- 🌐 Puerto 8069 disponible

### **1️⃣ Clonar el proyecto**
```bash
git clone https://github.com/byte-264/odoo16-test.git
cd odoo16-test
```

### **2️⃣ Iniciar Odoo**
```bash
docker-compose up -d
```

### **3️⃣ Acceder a la aplicación**
Abre tu navegador en: **http://localhost:8069**

### **4️⃣ Configuración inicial**
1. Crea una nueva base de datos
2. Configura el idioma y país
3. ¡Listo para usar! 🎉

---

## 📁 Estructura del Proyecto

```
odoo16/
├── 📄 docker-compose.yml      # Configuración de contenedores
├── 📄 README.md               # Esta documentación
├── 📄 create.py               # Script de creación de módulos
├── 📂 config/
│   └── 📄 odoo.conf          # Configuración de Odoo
├── 📂 addons/                 # Módulos personalizados y de terceros
│   ├── 📁 primer_modulo_prueba/
│   ├── 📁 ohrms_core/
│   ├── 📁 hr_payroll_community/
│   └── 📁 ... (más módulos)
├── 📂 docs/                   # Documentación adicional
│   ├── 📄 modulos.MD
│   └── 📄 permisos_ohrms.md
└── 📂 data/                   # Datos persistentes (autogenerado)
```

### **Descripción de carpetas:**

| **Carpeta** | **Descripción** |
|-------------|-----------------|
| `config/` | Configuración del servidor Odoo |
| `addons/` | Módulos personalizados y de terceros |
| `docs/` | Documentación y guías |
| `data/` | Volúmenes Docker para persistencia |

---

## 🛠️ Comandos Útiles

### **🟢 Gestión de Contenedores**

```bash
# Iniciar en segundo plano
docker-compose up -d

# Ver estado de servicios
docker-compose ps

# Detener servicios
docker-compose down

# Reiniciar solo Odoo
docker-compose restart web

# Reiniciar solo PostgreSQL
docker-compose restart db
```

### **📊 Monitoreo**

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de Odoo
docker-compose logs -f web

# Ver logs solo de PostgreSQL
docker-compose logs -f db

# Ver últimos 50 logs
docker-compose logs --tail=50 web
```

### **🔧 Mantenimiento**

```bash
# Acceder al contenedor de Odoo
docker-compose exec web bash

# Acceder al shell de Odoo
docker-compose exec web odoo shell -d postgres

# Actualizar lista de módulos
docker-compose exec web odoo -d postgres --update=all --stop-after-init

# Instalar módulo específico
docker-compose exec web odoo -d postgres -i nombre_modulo --stop-after-init
```

---

## 🔧 Configuración

### **🌐 Servicios Docker**

#### **Odoo (web)**
- **Puerto**: `8069` → `http://localhost:8069`
- **Imagen**: `odoo:16.0`
- **Volúmenes**: Datos, config, addons
- **Variables**: Host DB, usuario, contraseña

#### **PostgreSQL (db)**
- **Puerto**: `5432` (interno)
- **Imagen**: `postgres:13`
- **Base de datos**: `postgres`
- **Usuario**: `odoo` / **Contraseña**: `myodoo`

### **⚙️ Configuración Personalizada**

Edita `config/odoo.conf` para personalizar:

```ini
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
; db_host = db
; db_port = 5432
; db_user = odoo
; db_password = myodoo
```

---

## 📦 Módulos Disponibles

### **🏢 Módulos Core**
- `primer_modulo_prueba` - Módulo de ejemplo personalizado
- `ohrms_security_groups` - Gestión de permisos personalizados


## Contraseña de BD de prueba
- 5k9y-t4ig-5p6x