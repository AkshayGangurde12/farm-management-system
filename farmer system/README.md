# Farm Management System

A modern web application for connecting farmers with buyers, built with Flask and designed for agricultural product management.

## Features

- 🌱 **Product Management**: Farmers can list their agricultural products with detailed information
- 🛒 **E-commerce Style**: Modern UI similar to Zepto with category filtering
- 👨‍🌾 **Farmer Dashboard**: Personal dashboard for managing products and inventory
- 📱 **Responsive Design**: Works perfectly on all devices
- 🔐 **User Authentication**: Secure login and registration system
- 📊 **Analytics**: Track sales and inventory management

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Vercel

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open http://localhost:5000 in your browser

## Deployment on Vercel

### Prerequisites
- GitHub account
- Vercel account (free)

### Steps to Deploy

1. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push your code to the repository

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "New Project"
   - Import your GitHub repository

3. **Configure Environment Variables** (Optional):
   - In Vercel dashboard, go to your project settings
   - Add environment variables if needed:
     - `SECRET_KEY`: Your secret key for Flask
     - `DATABASE_URL`: If using external database

4. **Deploy**:
   - Vercel will automatically deploy your application
   - Your app will be available at `https://your-project-name.vercel.app`

### Important Notes for Vercel Deployment

- ✅ **Serverless Ready**: The app is configured for serverless deployment
- ✅ **Database**: Uses SQLite for simplicity (consider PostgreSQL for production)
- ✅ **Static Files**: All CSS, JS, and images are properly configured
- ✅ **Environment Variables**: Supports production environment configuration

## Project Structure

```
farmer-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── instance/             # Database files (local only)
└── README.md            # This file
```

## Features Overview

### For Farmers
- List products with categories, prices, and quantities
- Upload product images
- Manage inventory and availability
- Track product performance

### For Buyers
- Browse products by category
- Search and filter products
- Contact farmers directly
- View detailed product information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.