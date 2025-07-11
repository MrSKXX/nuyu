# Final working Dockerfile for Odoo on Render
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo (will use DB_HOST, DB_PORT, DB_USER, DB_PASSWORD automatically)
CMD ["odoo"]
