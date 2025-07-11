# Render PostgreSQL connection Dockerfile
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo with PostgreSQL environment variables
# Odoo automatically uses PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
