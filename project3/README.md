# Work-To-Home – Commute-Based Housing Finder

A full-stack application that helps users find home listings based on their work commute. The app integrates multiple APIs to fetch commute and housing data while maintaining secure user authentication.

## 🚀 Features

- **Smart Housing Search**: Find homes based on commute time and preferences
- **Commute Analysis**: Real-time commute calculations using mapping APIs
- **User Authentication**: Secure OAuth integration with Google and GitHub
- **Personalized Recommendations**: AI-powered housing suggestions
- **Interactive Maps**: Visual commute routes and housing locations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React.js** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **React Query** for state management
- **Mapbox** for interactive maps

### Backend
- **Flask** with Python
- **SQLAlchemy** for database ORM
- **PostgreSQL** for database
- **JWT** for authentication
- **OAuth2** for social login
- **Redis** for caching

### DevOps & Quality
- **ESLint** & **Prettier** for code formatting
- **Jest** & **React Testing Library** for testing
- **GitHub Actions** for CI/CD
- **Docker** for containerization

## 📁 Project Structure

```
work-to-home/
├── frontend/                 # React.js frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── backend/                 # Flask backend application
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utility functions
│   │   └── config.py       # Configuration
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Docker configuration
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Docker (optional)
- PostgreSQL (optional, can use SQLite for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd work-to-home
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Environment Variables**
   Create `.env` files in both frontend and backend directories with your API keys:
   ```
   # Backend .env
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost/worktohome
   GOOGLE_CLIENT_ID=your-google-client-id
   GITHUB_CLIENT_ID=your-github-client-id
   MAPBOX_ACCESS_TOKEN=your-mapbox-token
   
   # Frontend .env
   REACT_APP_API_URL=http://localhost:5000
   REACT_APP_MAPBOX_TOKEN=your-mapbox-token
   ```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
python -m pytest
```

## 🚀 Deployment

### Using Docker
```bash
docker-compose up --build
```

### Manual Deployment
1. Build the frontend: `npm run build`
2. Deploy backend to your preferred hosting service
3. Configure environment variables
4. Set up database and run migrations

## 📝 API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Housing Endpoints
- `GET /api/housing/search` - Search for housing listings
- `GET /api/housing/{id}` - Get housing details
- `POST /api/housing/favorites` - Add to favorites
- `GET /api/housing/favorites` - Get user favorites

### Commute Endpoints
- `POST /api/commute/calculate` - Calculate commute time
- `GET /api/commute/history` - Get commute history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Mapbox for mapping services
- Google Maps API for commute calculations
- React and Flask communities for excellent documentation
