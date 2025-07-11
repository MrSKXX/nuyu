# Permanent solution Dockerfile for Render.com
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Create entrypoint script that uses environment variables
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'echo "Starting Odoo with database: $DB_HOST"' >> /entrypoint.sh && \
    echo 'exec odoo \' >> /entrypoint.sh && \
    echo '  --db_host="$DB_HOST" \' >> /entrypoint.sh && \
    echo '  --db_port="$DB_PORT" \' >> /entrypoint.sh && \
    echo '  --db_user="$DB_USER" \' >> /entrypoint.sh && \
    echo '  --db_password="$DB_PASSWORD" \' >> /entrypoint.sh && \
    echo '  --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \' >> /entrypoint.sh && \
    echo '  "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose port
EXPOSE 8069

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
