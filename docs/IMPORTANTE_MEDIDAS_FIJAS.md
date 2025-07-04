# ⚠️ DIMENSIONES FIJAS DE TARJETAS DE EMPLEADO ⚠️

## 🚨 ATENCIÓN: MEDIDAS NUNCA DEBEN CAMBIARSE 🚨

### Dimensiones Estándar ISO/IEC 7810 ID-1

Las tarjetas de empleado están configuradas con las dimensiones exactas del estándar internacional:

- **Alto**: 305 = 86mm
- **Ancho**: 191 = 54mm

### ❌ PROHIBIDO CAMBIAR

**NUNCA** modifiques estas medidas en los siguientes archivos:

1. **`models/card_setting.py`**:
   ```python
   card_width = fields.Float('Width', default=246)   # MANTENER SIEMPRE 246px
   card_height = fields.Float('Height', default=161) # MANTENER SIEMPRE 161px
   ```

2. **`wizard/print_employee_card.py`**:
   ```python
   width = fields.Float('Width', required="1", default=246)  # NUNCA CAMBIAR
   height = fields.Float('Height', required="1", default=161) # NUNCA CAMBIAR
   ```

3. **`data/default_card_template_es.xml`**:
   ```xml
   <field name="card_width">246</field>  <!-- MANTENER SIEMPRE 246px -->
   <field name="card_height">161</field> <!-- MANTENER SIEMPRE 161px -->
   ```

### ✅ QUÉ SÍ SE PUEDE MODIFICAR

- Posiciones de elementos (top, left)
- Tamaños de fuente
- Colores
- Habilitar/deshabilitar campos
- Texto de etiquetas
- Tamaños de logos, fotos y códigos de barras

### 📐 Por qué estas medidas

- **56mm x 86mm** es el tamaño estándar mundial para tarjetas de identificación
- Compatible con laminadoras, impresoras de tarjetas y fundas estándar
- **246x161 píxeles** a 96 DPI corresponde exactamente a estas medidas físicas
- Mantiene proporción correcta para impresión sin distorsión

### 🛠️ Configuración del PDF

El sistema está configurado para:
- Papel: 86mm x 56mm (landscape)
- Márgenes: 0mm en todos los lados
- Sin bordes negros
- Fondo blanco limpio

### ⚠️ RECORDATORIO FINAL

Si cambias las medidas, las tarjetas **NO** encajarán en:
- Fundas protectoras estándar
- Laminadoras comerciales
- Impresoras de tarjetas
- Porta-tarjetas corporativos

**¡Mantén siempre 246x161px!**
