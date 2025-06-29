# NuYu Medical Spa - Odoo Customizations

## Medical Inventory Management System

Medical spa inventory management system built on Odoo Community Edition 16.0, designed for NuYu Medical Spa operations in Lebanon.

## Features

- Multi-location inventory management (Main Warehouse to Treatment Rooms)
- Room-to-room transfers with workflow management
- Medical product categorization (Injectable, Consumable, Retail, Device)
- Consignment inventory tracking with supplier management
- Expiry date monitoring with automated alerts
- Refrigeration requirement tracking (2-8°C for injectables)
- Lebanese currency support (LBP)
- Medical spa-specific workflows

## Quick Start for Team

### Prerequisites

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Follow installation instructions for your operating system
   - Ensure Docker is running before proceeding

2. **Install Git**
   - Windows: https://git-scm.com/download/win
   - Mac: `brew install git` or download from git-scm.com
   - Linux: `sudo apt install git` (Ubuntu/Debian)

3. **Install VSCode (Recommended)**
   - Download from: https://code.visualstudio.com/
   - Install Python and XML extensions for development

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/MrSKXX/nuyu.git
cd nuyu
```

2. **Start Docker Environment**
```bash
cd docker
docker-compose up -d
```

3. **Access Odoo**
   - Open browser: http://localhost:8069/web/login
   - Wait for Odoo to fully load (may take 2-3 minutes on first startup)

4. **Create Database**
   - Click "Create Database"
   - Database Name: `nuyu_production`
   - Email: `admin@nuyu.com`
   - Password: `nuyu2025`
   - Language: English
   - Country: Lebanon
   - Click "Create Database"

5. **Install Medical Inventory Module**
   - Go to **Apps** menu
   - Remove "Apps" filter to see all modules
   - Search for "Medical Spa Inventory" or "NuYu"
   - Click **Install**

### Common Issue After Database Creation

**If you encounter SMS-related errors in Settings:**

The system may display warnings about missing SMS functionality. This can be resolved by:

1. Go to Apps menu
2. Search for "stock sms"
3. Install the "Stock SMS" module
4. Restart if needed:
```bash
docker-compose restart odoo
```

This resolves SMS-related configuration warnings.

### Access Medical Inventory

After installation, "Medical Inventory" will appear in the main menu with:
- **Operations**: Room Transfers, Consignment, Expiry Dashboard
- **Configuration**: Medical Products, Medical Locations

## Pre-loaded Sample Data

The system includes sample medical products:
- **Botox 100 Units** ($450) - Injectable, refrigerated
- **Hyaluronic Acid Filler 1ml** ($280) - Injectable, refrigerated
- **Vitamin C Serum 30ml** ($85) - Retail product
- **Disposable Needles 30G** ($2.50) - Medical consumable

And NuYu medical locations:
- **Main Warehouse** (with refrigeration)
- **Treatment Room 1, 2, 3**
- **Doctor Private Stock** (refrigerated)
- **Refrigerated Storage**

## Development Workflow

### Daily Development
```bash
# Start environment
docker-compose up -d

# Make changes to files in modules/medical_inventory/
# After changes, restart:
docker-compose restart odoo

# In Odoo: Apps → Medical Spa Inventory → Upgrade
```

### Git Workflow
```bash
git add .
git commit -m "feature: description of changes"
git push origin [branch-name]
```

### Module Structure
```
modules/medical_inventory/
├── models/                 # Backend logic
│   ├── product_template.py # Medical product fields
│   ├── room_transfer.py    # Room transfer workflow
│   ├── consignment.py      # Consignment tracking
│   └── stock.py           # Stock enhancements
├── views/                  # User interface
│   ├── medical_inventory_menus.xml
│   ├── room_transfer_views.xml
│   ├── consignment_views.xml
│   ├── product_views.xml
│   └── stock_location_views.xml
├── data/                   # Setup data
│   ├── stock_location_data.xml
│   └── product_category_data.xml
└── security/              # Permissions
    └── ir.model.access.csv
```

## Business Workflows

### Room Transfer Process
1. Navigate to **Medical Inventory** → **Operations** → **Room Transfers**
2. Click **NEW**
3. Select source location (e.g., Main Warehouse)
4. Select destination (e.g., Treatment Room 1)
5. Add products with quantities
6. **Confirm** → **Mark Done**

### Consignment Management
1. Navigate to **Medical Inventory** → **Operations** → **Consignment**
2. Click **NEW**
3. Select supplier and location
4. Add consignment products with costs
5. **Activate** to mark as consignment stock
6. **Settle** when products are used

### Medical Product Setup
1. Navigate to **Medical Inventory** → **Configuration** → **Medical Products**
2. Click **NEW**
3. Set medical category (Injectable/Consumable/Retail/Device)
4. Configure storage requirements
5. Set expiry and batch tracking

## Development Team Roles

- **Lead Developer**: Inventory and Infrastructure
- **Senior Developer**: Custom Features and POS Integration
- **Technical Lead**: Architecture and Technical Decisions

## Testing Your Setup

### Verify Installation
1. **Check Menu**: "Medical Inventory" appears in main menu
2. **Test Transfer**: Create room transfer from warehouse to treatment room
3. **View Products**: Verify medical products with categories
4. **Check Locations**: Confirm NuYu locations are created

### Test Data Flow
1. **Create Room Transfer**: Move Botox from warehouse to Treatment Room 1
2. **Add Consignment**: Track supplier products
3. **Monitor Expiry**: Check expiry dashboard functionality

## Troubleshooting

### Docker Issues
```bash
# Stop containers
docker-compose down

# Start fresh
docker-compose up -d

# Check logs
docker-compose logs odoo
```

### Module Installation Issues
1. Restart containers: `docker-compose restart odoo`
2. Check Apps menu filters (remove "Apps" filter)
3. Try upgrade instead of install
4. Check logs for specific errors

### View Errors
- Verify XML syntax in view files
- Check field names exist in models
- Restart after making changes

### Permission Errors
- Ensure user has "Inventory/User" access rights
- Check security/ir.model.access.csv for model permissions

### Database Connection Issues
- Ensure Docker is running
- Check if port 8069 is available
- Restart Docker Desktop if needed

## System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended)
- **Storage**: 10GB free space
- **Docker**: Latest version
- **Browser**: Chrome, Firefox, Safari (latest versions)

### Development Requirements
- **VSCode** with Python and XML extensions
- **Git** for version control
- **Terminal/Command Line** access

## Production Deployment

### Pre-Production Checklist
- Test all workflows thoroughly
- Backup development database
- Review security permissions
- Train end users
- Document custom workflows

### Environment Variables
```bash
# In docker/.env (create if needed)
POSTGRES_PASSWORD=secure_password
ODOO_ADMIN_PASSWORD=secure_admin_password
```

## Support

### Repository Information
- **GitHub**: https://github.com/MrSKXX/nuyu.git
- **Main Branch**: production-ready
- **Organization**: Symufolk/Home Logic

### Getting Help
1. Check this README for common issues
2. Review module documentation in `docs/`
3. Check GitHub issues for known problems
4. Contact technical lead for support

## Development Roadmap

### Currently Implemented
- Multi-location inventory management
- Room transfer workflows
- Medical product categorization
- Consignment tracking
- Lebanese currency integration
- Medical spa user interface

### Sprint 1 (In Progress)
- Enhanced expiry monitoring
- POS Lebanese currency integration
- Advanced reporting features
- Mobile responsiveness testing

### Future Enhancements
- Automated reorder alerts
- Patient treatment history integration
- Advanced analytics dashboard
- Mobile application development
- Integration with accounting system

## Business Impact

### Primary Requirements Status
- Multi-location inventory management: Implemented
- Room-to-room transfer capability: Implemented
- Medical spa location structure: Implemented
- Expiry date tracking: Implemented
- Professional environment: Implemented
- Lebanese currency support (LBP): Implemented

### Community Edition vs Enterprise
This implementation demonstrates that Odoo Community Edition can handle the primary requirements for medical spa inventory management, providing cost-effective functionality while maintaining professional standards.

**Result**: Functional medical spa inventory system with significant cost savings compared to Enterprise licensing.

## Architecture Overview

### Core Models
- **Medical Products**: Extended product management with medical-specific fields
- **Medical Locations**: Spa-specific location hierarchy and storage requirements
- **Room Transfers**: Workflow management for inter-location product movement
- **Consignment Tracking**: Supplier consignment inventory management
- **Stock Enhancement**: Medical-specific stock tracking and monitoring

### Security Model
- Role-based access control
- Stock user and manager permission levels
- Model-specific access rights
- Data integrity validation

### Integration Points
- Standard Odoo inventory management
- Lebanese currency configuration
- POS system integration ready
- Accounting system integration ready

## Contributing

### Code Standards
- Follow Odoo development guidelines
- Use descriptive model and field names
- Implement proper validation
- Document complex business logic
- Test thoroughly before commits

### Development Process
1. Create feature branch from production-ready
2. Implement changes with proper testing
3. Update documentation as needed
4. Submit pull request with description
5. Code review and merge process

This medical inventory management system provides a foundation for NuYu Medical Spa operations with room for continued enhancement and customization based on evolving business needs.