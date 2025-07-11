# Dockerfile for Render.com deployment with PostgreSQL
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo with environment variables
CMD ["odoo", "--database=nuyu_production"]
