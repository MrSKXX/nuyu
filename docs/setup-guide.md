Development Setup Guide
Prerequisites

Docker Desktop installed
Git access to repository
VSCode (recommended)

Setup Steps

git clone https://github.com/MrSKXX/nuyu.git
cd nuyu/docker
docker-compose up -d
Open browser: http://localhost:8069/web/login
Create database: "nuyu_production"
Install custom modules from Apps menu

Daily Workflow

docker-compose up -d (start environment)
Develop in modules/ folder
docker-compose restart odoo (after changes)
Test in browser
Commit: git add . && git commit -m "your message"
Push: git push origin [branch-name]