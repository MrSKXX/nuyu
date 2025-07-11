# Ultra simple Dockerfile - let Odoo auto-detect environment
FROM odoo:16.0

# Copy custom modules
COPY modules /mnt/extra-addons

# Set environment variables that Odoo will automatically use
ENV HOST=$POSTGRES_HOST
ENV PORT=$POSTGRES_PORT  
ENV USER=$POSTGRES_USER
ENV PASSWORD=$POSTGRES_PASSWORD

# Expose port
EXPOSE 8069

# Start Odoo (it will use the environment variables automatically)
CMD ["odoo"]
