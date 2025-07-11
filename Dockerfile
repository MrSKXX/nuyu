# Dockerfile with database initialization
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Create the entrypoint script with database initialization
USER root
RUN echo '#!/bin/bash' > /usr/local/bin/start-odoo.sh && \
    echo 'set -e' >> /usr/local/bin/start-odoo.sh && \
    echo 'echo "Starting Odoo with database: $DB_HOST"' >> /usr/local/bin/start-odoo.sh && \
    echo '# Initialize database if it does not exist' >> /usr/local/bin/start-odoo.sh && \
    echo 'exec odoo --db_host="$DB_HOST" --db_port="$DB_PORT" --db_user="$DB_USER" --db_password="$DB_PASSWORD" --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons --init=base --stop-after-init --database=nuyu_production || true' >> /usr/local/bin/start-odoo.sh && \
    echo '# Start Odoo normally' >> /usr/local/bin/start-odoo.sh && \
    echo 'exec odoo --db_host="$DB_HOST" --db_port="$DB_PORT" --db_user="$DB_USER" --db_password="$DB_PASSWORD" --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons "$@"' >> /usr/local/bin/start-odoo.sh && \
    chmod +x /usr/local/bin/start-odoo.sh

# Switch back to odoo user
USER odoo

# Expose port
EXPOSE 8069

# Use the startup script
CMD ["/usr/local/bin/start-odoo.sh"]
