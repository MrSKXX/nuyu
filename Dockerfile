# Definitive working Dockerfile for Render.com
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Create Odoo configuration file
RUN echo "[options]" > /etc/odoo/odoo.conf && \
    echo "addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons" >> /etc/odoo/odoo.conf && \
    echo "data_dir = /var/lib/odoo" >> /etc/odoo/odoo.conf && \
    echo "logfile = /var/log/odoo/odoo.log" >> /etc/odoo/odoo.conf && \
    echo "log_level = info" >> /etc/odoo/odoo.conf

# Expose port
EXPOSE 8069

# Start Odoo with explicit database connection parameters
CMD ["sh", "-c", "odoo --config=/etc/odoo/odoo.conf --db_host=${DB_HOST:-$POSTGRES_HOST} --db_port=${DB_PORT:-$POSTGRES_PORT} --db_user=${DB_USER:-$POSTGRES_USER} --db_password=${DB_PASSWORD:-$POSTGRES_PASSWORD}"]
