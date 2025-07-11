# Simple working Dockerfile for Render.com
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Create a startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 8069

# Use startup script
CMD ["/start.sh"]
