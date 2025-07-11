# Fixed Dockerfile for Render.com deployment
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo
CMD ["odoo"]
