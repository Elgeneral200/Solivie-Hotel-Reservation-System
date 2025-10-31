# 🏨 Hotel Reservation System

A complete hotel reservation and management system built with Python and Streamlit.

## 📋 Features

### Customer Features
- ✅ User registration and authentication
- 🔍 Room search with filters
- 📅 Real-time availability checking
- 💰 Dynamic pricing
- 💳 Multiple payment methods
- 🎁 Promotional codes
- 👤 Profile management
- ⭐ Reviews and ratings
- 🏆 Loyalty program

### Admin Features
- 📊 Dashboard with analytics
- 🛏️ Room management
- 📋 Booking management
- 👥 User management
- 📈 Reports

## 🛠 Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.8+
- **Database:** SQLite + SQLAlchemy
- **Security:** Bcrypt

## 📁 Project Structure
hotel-reservation-system/
├── app.py # Main entry point
├── config.py # Configuration
├── requirements.txt # Dependencies
├── database/ # Database models
├── backend/ # Business logic
├── frontend/ # UI pages
├── utils/ # Utilities
└── tests/ # Tests

## 🚀 Installation

### 1. Create Virtual Environment
- python -m venv venv
- venv\Scripts\activate

### 2. Install Dependencies
- pip install -r requirements.txt


### 3. Initialize Database
- python -m database.seed_data


### 5. Run Application
- streamlit run app.py


Open browser at `http://localhost:8501`

## ⚙️ Configuration

Create `.env` file:
- SECRET_KEY=your-secret-key
- EMAIL_HOST=smtp.gmail.com
- EMAIL_PORT=587
- EMAIL_USER=your-email@gmail.com
- EMAIL_PASSWORD=your-password


## 🔑 Default Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Customer
- Email: `john.doe@example.com`
- Password: `password123`

**⚠️ Change in production!**

## 📖 Usage

### For Customers
1. Register/Login
2. Search rooms by date and preferences
3. Book and pay
4. Manage bookings
5. Leave reviews

### For Admins
1. Login with admin credentials
2. Access dashboard
3. Manage rooms, bookings, users
4. View reports

## 🧪 Testing
- python -m pytest tests/


## 👥 Team

- Team Members: 
1. Salma Abdelhamid 
2. Dai Ehab 
3. Shaza Mohamed 
4. Muhammad Fathi 
5. Mohamed Elsayed

## 📄 License

Solavie Hotel Team

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📞 Support

For issues, create a GitHub issue or contact support@hotel.com

---

Made with ❤️ by Solivie Team

