import os
import re
import sys

def validar_identificador(nombre, tipo):
    if not re.match(r'^[a-z_][a-z0-9_]*$', nombre):
        print(f"❌ Error: El {tipo} '{nombre}' no es válido. Solo se permiten letras minúsculas, números y guiones bajos, y debe comenzar con una letra o guión bajo.")
        sys.exit(1)

def limpiar_nombre(nombre):
    return re.sub(r'[^a-zA-Z0-9_]', '_', nombre.strip().lower())

# Entrada con validación + advertencia
entrada_modulo = input("Nombre del módulo (sin espacios): ").strip()
modulo_limpio = limpiar_nombre(entrada_modulo)

if entrada_modulo != modulo_limpio:
    print(f"⚠️  El nombre del módulo ha sido corregido de '{entrada_modulo}' a '{modulo_limpio}' para cumplir con las reglas de Odoo.")

MODULO = modulo_limpio
validar_identificador(MODULO, "nombre del módulo")

NOMBRE_MODELO = limpiar_nombre(input("Nombre del modelo (en snake_case): "))
validar_identificador(NOMBRE_MODELO, "nombre del modelo")

NOMBRE_CLASE = ''.join(x.capitalize() for x in NOMBRE_MODELO.split('_'))

DESCRIPCION = input("Descripción del módulo: ").strip() or "Módulo de ejemplo"

# Estructura de carpetas
base_path = f"addons/{MODULO}"
os.makedirs(f"{base_path}/models", exist_ok=True)
os.makedirs(f"{base_path}/views", exist_ok=True)
os.makedirs(f"{base_path}/security", exist_ok=True)

# __init__.py
with open(f"{base_path}/__init__.py", "w") as f:
    f.write("from . import models\n")

# __manifest__.py
with open(f"{base_path}/__manifest__.py", "w") as f:
    f.write(f"""{{
    'name': '{MODULO.replace("_", " ").title()}',
    'version': '1.0',
    'summary': '{DESCRIPCION}',
    'author': 'Tu Nombre',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/{NOMBRE_MODELO}_views.xml',
    ],
    'installable': True,
    'application': True,
}}
""")

# models/__init__.py
with open(f"{base_path}/models/__init__.py", "w") as f:
    f.write(f"from . import {NOMBRE_MODELO}\n")

# models/{NOMBRE_MODELO}.py
with open(f"{base_path}/models/{NOMBRE_MODELO}.py", "w") as f:
    f.write(f"""from odoo import models, fields

class {NOMBRE_CLASE}(models.Model):
    _name = 'mi.modelo.{NOMBRE_MODELO}'
    _description = '{NOMBRE_CLASE}'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
""")

# views/{NOMBRE_MODELO}_views.xml
with open(f"{base_path}/views/{NOMBRE_MODELO}_views.xml", "w") as f:
    f.write(f"""<odoo>
  <record id="view_form_{NOMBRE_MODELO}" model="ir.ui.view">
    <field name="name">mi.modelo.{NOMBRE_MODELO}.form</field>
    <field name="model">mi.modelo.{NOMBRE_MODELO}</field>
    <field name="arch" type="xml">
      <form string="{NOMBRE_CLASE}">
        <sheet>
          <group>
            <field name="name"/>
            <field name="descripcion"/>
          </group>
        </sheet>
      </form>
    </field>
  </record>

  <record id="view_tree_{NOMBRE_MODELO}" model="ir.ui.view">
    <field name="name">mi.modelo.{NOMBRE_MODELO}.tree</field>
    <field name="model">mi.modelo.{NOMBRE_MODELO}</field>
    <field name="arch" type="xml">
      <tree string="{NOMBRE_CLASE}s">
        <field name="name"/>
      </tree>
    </field>
  </record>

  <record id="action_{NOMBRE_MODELO}" model="ir.actions.act_window">
    <field name="name">{NOMBRE_CLASE}s</field>
    <field name="res_model">mi.modelo.{NOMBRE_MODELO}</field>
    <field name="view_mode">tree,form</field>
  </record>

  <menuitem id="menu_{NOMBRE_MODELO}_root" name="{NOMBRE_CLASE}s"/>
  <menuitem id="menu_{NOMBRE_MODELO}_sub" name="Listado" parent="menu_{NOMBRE_MODELO}_root" action="action_{NOMBRE_MODELO}"/>
</odoo>
""")

# security/ir.model.access.csv
model_id = f"mi.modelo.{NOMBRE_MODELO}"
model_name = f"model_mi_modelo_{NOMBRE_MODELO}"

with open(f"{base_path}/security/ir.model.access.csv", "w") as f:
    f.write("id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n")
    f.write(f"access_{NOMBRE_MODELO},access_{NOMBRE_MODELO},{model_name},base.group_user,1,1,1,1\n")

print(f"\n✅ Módulo generado correctamente en '{base_path}'")