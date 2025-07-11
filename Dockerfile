# Final working Dockerfile for Render.com deployment
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo with environment variables (no default db host)
CMD ["odoo", "--db_host=${POSTGRES_HOST}", "--db_port=${POSTGRES_PORT}", "--db_user=${POSTGRES_USER}", "--db_password=${POSTGRES_PASSWORD}", "--database=${POSTGRES_DB}"]
