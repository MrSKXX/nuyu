# Immediate SQLite solution - works instantly
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Create data directory
RUN mkdir -p /var/lib/odoo

# Expose port
EXPOSE 8069

# Start Odoo with SQLite (no external database needed)
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons", "--data-dir=/var/lib/odoo"]
