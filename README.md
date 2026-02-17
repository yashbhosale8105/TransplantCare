# Transplant Care Management System

A comprehensive Python-based application for managing organ transplant operations, connecting donors, patients, and administrative staff through an integrated dashboard system.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [System Components](#system-components)
- [Requirements](#requirements)
- [Database Setup](#database-setup)

## 🎯 Overview

The Transplant Care Management System is a multi-user application designed to streamline organ transplant coordination. It provides separate dashboards for administrators, donors, and patients to manage registrations, track compatibility, and facilitate the transplant process efficiently.

## ✨ Features

- **Multi-User Authentication System**: Separate login portals for admins, donors, and patients
- **Admin Dashboard**: Comprehensive management and monitoring of all system activities
- **Donor Dashboard**: Registration and profile management for organ donors
- **Patient Dashboard**: Patient registration and transplant request management
- **Blood Type & Compatibility Matching**: Advanced matching algorithm for donor-patient compatibility
- **Email Notifications**: Automated email communication system
- **User Registration Forms**: Intuitive forms for donors and patients
- **Data Visualization**: Charts and analytics for system metrics
- **Secure Database**: Robust data storage and management

## 📁 Project Structure

```
Transplant Care/
├── admin_dashboard.py          # Admin main interface
├── admin_login.py              # Admin authentication
├── Donors_Dashboard.py          # Donor main interface
├── donorlogin.py               # Donor authentication
├── donorform.py                # Donor registration form
├── Paitents_Dashboard.py        # Patient main interface
├── patientlogin.py             # Patient authentication
├── patientform.py              # Patient registration form
├── HomePage.py                 # Application home page
├── database_setup.py           # Database initialization
├── setup_database.py           # Alternative database setup
├── matching_feature.py         # Donor-patient matching logic
├── blood.py                    # Blood type compatibility
├── bar_chart.py                # Data visualization
├── email_app.py                # Email service module
├── assets/                     # GUI and styling assets
│   ├── gui.py
│   ├── gui1.py
│   ├── frame0/
│   └── frame1/
├── Image folder/               # Application images and assets
├── sbl/
│   └── game.py                # Additional game component
├── __pycache__/               # Python cache
└── requirements.txt           # Project dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- MySQL or compatible database server

### Steps

1. **Clone or download the project folder**
   ```bash
   cd "Transplant Care"
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python database_setup.py
   # or
   python setup_database.py
   ```

4. **Configure database connection** (if needed)
   - Update database credentials in the respective configuration files

## ⚙️ Configuration

### Database Setup
- Ensure your database server is running
- Update connection parameters in `database_setup.py` or `setup_database.py` with your database credentials
- Default configurations assume a local MySQL server

### Email Configuration
- Configure email settings in `email_app.py` with your SMTP credentials
- Set up email templates for notifications

## 💻 Usage

### Starting the Application
```bash
python HomePage.py
```

### Role-Based Access

#### Administrator
- Login via `admin_login.py`
- Access comprehensive admin dashboard
- Manage users and system operations
- View system analytics and statistics

#### Donors
- Register via donor registration form
- Login via `donorlogin.py`
- Manage donor profile
- Track donation requests

#### Patients
- Register via patient registration form
- Login via `patientlogin.py`
- Manage patient profile
- Request organ transplants
- Track request status

## 🔧 System Components

### Authentication Module
- Secure login system for all user roles
- Password management and validation
- Session management

### Dashboard Modules
- Real-time data updates
- User profile management
- Request tracking and status monitoring

### Matching Engine
- `matching_feature.py`: Core matching algorithm
- `blood.py`: Blood type compatibility checks
- Compatible donor-patient identification

### Communication
- `email_app.py`: Automated email notifications
- Status updates and alerts

### Analytics
- `bar_chart.py`: Statistical visualization
- System usage metrics
- Performance tracking

## 📦 Requirements

All required Python packages are listed in `requirements.txt`. Common dependencies include:
- tkinter (GUI framework)
- mysql-connector-python (Database)
- smtplib (Email)
- pandas (Data processing)
- matplotlib (Charting)

Install all requirements:
```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

The application uses a relational database to store:
- User accounts (Admins, Donors, Patients)
- Donor profiles and medical information
- Patient profiles and transplant requests
- Compatibility matching records
- Communication logs

Run the setup scripts to initialize:
```bash
python database_setup.py
```

## 📧 Support

For issues, questions, or contributions, please contact the development team.

## 📄 License

This project is intended for healthcare management purposes. Ensure compliance with local regulations and data protection laws.

---

**Last Updated**: February 2026
