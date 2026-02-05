# 🛒 Inventory Management System (Flask + SQLite)

A role-based Inventory Management System built using **Python Flask** and **SQLite**, designed to manage products, track stock movement, and maintain transaction history through a centralized web interface.

This project replaces manual or spreadsheet-based inventory tracking with a **structured, secure, and scalable** web application.

---

## 📌 Features

### 🔐 User Authentication
- Secure login system  
- Role-Based Access Control (RBAC)

---

### 👥 User Roles
- **Admin**: Manage products, view analytics & transactions  
- **Manager**: Update inventory, view analytics & transactions  
- **Staff**: Update inventory only  

---

### 📦 Product Management
- Add, edit, delete products  
- Define minimum stock levels  

---

### 📊 Inventory Management
- Stock **IN** / Stock **OUT** operations  
- Automatic quantity updates (no duplicate inventory rows)  
- Low-stock alerts on dashboard  

---

### 🧾 Transaction Logging
- Complete history of stock movements  
- Tracks product, quantity, action type, user, and timestamp  

---

### 📈 Analytics Dashboard
- Product-wise stock visualization  
- Stock IN vs Stock OUT summary  

---

### 📤 Export Functionality
- Download stock report as CSV  

## 🧠 System Design Overview

- Centralized database for all inventory data  
- One-to-one relationship between **Product** and **Inventory**  
- Role-based access handled at application level  
- Modular and extensible architecture  

---

### ⚠️ Note
This project is implemented as a **local web application**.  
However, the architecture is **cloud-ready** and can be deployed to cloud platforms (AWS, Azure, etc.) with minimal changes.

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Python (Flask) |
| ORM | SQLAlchemy |
| Database | SQLite |
| Authentication | Flask-Login |
| Frontend | HTML, CSS |
| Charts | Chart.js |

## 📂 Project Structure
```
inventory-system/
│
├── app.py # Main Flask application
├── models.py # Database models
├── config.py # App configuration
├── inventory.db # SQLite database
│
├── templates/ # HTML templates
│ ├── login.html
│ ├── layout.html
│ ├── dashboard.html
│ ├── products.html
│ ├── inventory.html
│ ├── stock.html
│ ├── analytics.html
│ └── transactions.html
│
├── static/
│ └── style.css # Styling
│
├── venv/ # Virtual environment
└── README.md
```

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Rashid7520/inventory-management-system.git
cd inventory-management-system
```

### 2️⃣ Create & Activate Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```
pip install flask flask-sqlalchemy flask-login
```

### 4️⃣ Run the Application
```
python app.py
```

## 🔐 Access Control Summary

| Role    | Permissions |
|---------|-------------|
| Admin   | Full access (products, analytics, transactions) |
| Manager | Inventory updates, analytics, transactions |
| Staff  | Inventory updates only |

---

## 🚀 Future Enhancements

- Cloud deployment (AWS / Azure)
- PostgreSQL or MySQL integration
- User management dashboard
- Email alerts for low stock
- REST API integration
- Dockerization

---

## 🎓 Academic Relevance

This project demonstrates:

- CRUD operations
- Database normalization
- Role-based access control
- MVC-style architecture
- Real-world inventory workflows

**Suitable for:**
- College projects
- Mini-projects
- Resume / portfolio showcase

---

## 👤 Author

- **Mohammad Rashid Nazir**
- **Arun Mandava**
- **Sneh Jain**
- **Tejus Sharma**
- **Gargee Kataria**
- Inventory Management System – Mini Project
