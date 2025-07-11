#!/bin/bash

# Start Odoo with environment variables
exec odoo \
    --db_host="$POSTGRES_HOST" \
    --db_port="$POSTGRES_PORT" \
    --db_user="$POSTGRES_USER" \
    --db_password="$POSTGRES_PASSWORD" \
    --database="$POSTGRES_DB"
