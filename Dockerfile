# Dockerfile personalizado basado en Odoo 16
FROM odoo:16.0

# Cambiar a usuario root para instalar paquetes
USER root

# Instalar LibreOffice y dependencias necesarias
RUN apt-get update && \
    apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-liberation \
    fonts-dejavu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar python-docx
RUN rm -f /usr/lib/python3*/EXTERNALLY-MANAGED 2>/dev/null || true && \
    pip3 install python-docx

# Volver al usuario odoo
USER odoo
