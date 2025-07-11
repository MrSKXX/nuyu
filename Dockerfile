# 🐍 Use official Python base
FROM python:3.10-slim

# 🏗️ Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    curl \
    wget \
    nodejs \
    npm \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libldap2-dev \
    libsasl2-dev \
    libjpeg-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 🐘 Install wkhtmltopdf (PDF export)
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb

# 📁 Create Odoo user & folders
RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo
WORKDIR /opt/odoo

# 🧠 Clone Odoo Community from GitHub
RUN git clone --depth=1 --branch=16.0 https://www.github.com/odoo/odoo /opt/odoo/odoo

# 🧪 Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# 📂 Mount custom addons if needed
RUN mkdir /mnt/extra-addons && chown odoo:odoo /mnt/extra-addons

# ✍️ Create the custom startup script using environment variables
USER root
RUN echo '#!/bin/bash' > /usr/local/bin/start-odoo.sh && \
    echo 'set -e' >> /usr/local/bin/start-odoo.sh && \
    echo 'echo "📦 Connecting to DB at: ${DB_HOST}:${DB_PORT}"' >> /usr/local/bin/start-odoo.sh && \
    echo 'exec odoo \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --db_host="${DB_HOST}" \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --db_port="${DB_PORT}" \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --db_user="${DB_USER}" \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --db_password="${DB_PASSWORD}" \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --addons-path=/mnt/extra-addons,/opt/odoo/odoo/addons \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --xmlrpc-port="${PORT}" \\' >> /usr/local/bin/start-odoo.sh && \
    echo '  --database="${DATABASE_NAME}" "$@"' >> /usr/local/bin/start-odoo.sh && \
    chmod +x /usr/local/bin/start-odoo.sh

# 🔐 Set user back to Odoo (non-root)
USER odoo

# 🚀 Start Odoo with your custom script
CMD ["/usr/local/bin/start-odoo.sh"]
