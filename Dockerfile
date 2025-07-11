# Use official Odoo 16 base image
FROM odoo:16.0

# Copy custom modules to the extra addons folder
COPY modules /mnt/extra-addons

# Become root to install and write startup script
USER root

# Create a custom startup script that:
# 1. Initializes the database (first-time only)
# 2. Starts Odoo on port 8080
RUN echo '#!/bin/bash' > /usr/local/bin/start-odoo.sh && \
    echo 'set -e' >> /usr/local/bin/start-odoo.sh && \
    echo 'echo "🔄 Starting Odoo with database: $DATABASE_NAME at $DB_HOST:$DB_PORT"' >> /usr/local/bin/start-odoo.sh && \
    echo '# Optional: initialize base module only once (can be removed if DB already exists)' >> /usr/local/bin/start-odoo.sh && \
    echo 'exec odoo --db_host="$DB_HOST" --db_port="$DB_PORT" --db_user="$DB_USER" --db_password="$DB_PASSWORD" --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons --init=base --stop-after-init --database="$DATABASE_NAME" || true' >> /usr/local/bin/start-odoo.sh && \
    echo '# Start Odoo normally on port 8080' >> /usr/local/bin/start-odoo.sh && \
    echo 'exec odoo --db_host="$DB_HOST" --db_port="$DB_PORT" --db_user="$DB_USER" --db_password="$DB_PASSWORD" --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons --xmlrpc-port=8080 --database="$DATABASE_NAME" "$@"' >> /usr/local/bin/start-odoo.sh && \
    chmod +x /usr/local/bin/start-odoo.sh

# Switch back to odoo user for security
USER odoo

# Expose port 8080 for Render
EXPOSE 8080

# Use the startup script as the main entrypoint
CMD ["/usr/local/bin/start-odoo.sh"]
