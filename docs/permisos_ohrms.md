# 🔐 Gestión de Permisos en Módulos OHRMS

## 📋 **Problema Común**

Los módulos de terceros (como OHRMS) no aparecen en la configuración de permisos de usuario porque:

1. **No están instalados** correctamente
2. **No tienen grupos de seguridad** específicos
3. **Faltan en las categorías** de permisos

## ✅ **Solución Implementada**

Hemos creado el módulo `ohrms_security_groups` que define:

### **Grupos de Seguridad Disponibles:**

#### **🏢 Recursos Humanos Generales**
- **HR / Usuario Básico**: Solo lectura de empleados
- **HR / Usuario Avanzado**: Lectura y escritura 
- **HR / Gerente**: Permisos completos + eliminación

#### **💰 Nómina**
- **Nómina / Usuario**: Consulta de nóminas
- **Nómina / Gerente**: Gestión completa de nóminas

#### **🏦 Préstamos**
- **Préstamos / Usuario**: Ver préstamos de empleados
- **Préstamos / Gerente**: Aprobar/rechazar préstamos

#### **📋 Otros**
- **Documentos de Empleados / Usuario**: Gestión de documentos
- **Dashboard HR / Usuario**: Acceso al tablero de HR

## 🚀 **Cómo Asignar Permisos**

### **Método 1: Via interfaz web**

1. **Ve a Configuración → Usuarios y Empresas → Usuarios**
2. **Selecciona un usuario**
3. **En la pestaña "Permisos de acceso"**
4. **Busca la sección "Recursos Humanos - OHRMS"**
5. **Asigna los grupos necesarios**

### **Método 2: Configuración masiva**

```python
# Ejemplo para asignar permisos via código
user = self.env['res.users'].browse(user_id)
hr_manager_group = self.env.ref('ohrms_security_groups.group_hr_manager')
user.groups_id = [(4, hr_manager_group.id)]
```

## 📊 **Matriz de Permisos Recomendada**

| **Rol** | **HR Básico** | **HR Avanzado** | **HR Gerente** | **Nómina** | **Préstamos** |
|---------|---------------|-----------------|----------------|------------|---------------|
| **Empleado** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **HR Usuario** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **HR Gerente** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Contador** | ❌ | ❌ | ❌ | ✅ | ✅ |

## 🔧 **Instalación de Módulos OHRMS**

### **Orden recomendado de instalación:**

1. **hr_employee_updation** - Actualización de empleados
2. **oh_employee_creation_from_user** - Crear empleados desde usuarios
3. **hr_payroll_community** - Nómina comunitaria
4. **hr_contract_types** - Tipos de contrato
5. **ohrms_loan** - Gestión de préstamos
6. **hrms_dashboard** - Dashboard de HR
7. **ohrms_core** - Módulo principal (instala dependencias)

### **Comandos para verificar instalación:**

```bash
# Ver módulos instalados
docker-compose exec web odoo shell -d postgres
>>> self.env['ir.module.module'].search([('name', 'like', 'hr_'), ('state', '=', 'installed')])

# Actualizar módulo específico
docker-compose exec web odoo -d postgres -u nombre_modulo --stop-after-init
```

## 🛠️ **Solución de Problemas**

### **Problema: "Módulo no aparece en Apps"**
```bash
# Verificar que esté en addons/
ls -la addons/nombre_modulo/

# Verificar manifest
cat addons/nombre_modulo/__manifest__.py

# Reiniciar Odoo
docker-compose restart web
```

### **Problema: "Error de dependencias"**
1. Instalar dependencias primero
2. Verificar `depends` en `__manifest__.py`
3. Instalar módulos base de Odoo requeridos

### **Problema: "Permisos no aparecen"**
1. Instalar `ohrms_security_groups`
2. Actualizar lista de aplicaciones
3. Verificar en modo desarrollador

## 📝 **Personalización Avanzada**

### **Crear grupos personalizados:**

```xml
<record id="group_custom_hr" model="res.groups">
    <field name="name">Mi Grupo HR Personalizado</field>
    <field name="category_id" ref="module_category_hr_custom"/>
    <field name="comment">Descripción del grupo</field>
</record>
```

### **Asignar permisos específicos:**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_mi_modelo,Mi Acceso,model_mi_modelo,group_custom_hr,1,1,1,0
```

## 🎯 **Resultado Final**

Después de seguir esta guía:

- ✅ **Módulos OHRMS** instalados y funcionando
- ✅ **Permisos organizados** por categorías
- ✅ **Grupos de seguridad** específicos para HR
- ✅ **Gestión granular** de accesos
- ✅ **Configuración escalable** para equipos grandes

¡Ahora podrás gestionar permisos de manera profesional en tu instancia de Odoo 16 con OHRMS! 🚀
