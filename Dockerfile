# Final Dockerfile using complete DATABASE_URL
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Expose port
EXPOSE 8069

# Start Odoo - it will automatically use DATABASE_URL environment variable
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"]
