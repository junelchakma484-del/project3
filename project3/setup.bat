@echo off
echo 🚀 Setting up Work-To-Home Application...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create environment files if they don't exist
if not exist "backend\.env" (
    echo 📝 Creating backend .env file...
    (
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo DATABASE_URL=postgresql://postgres:password@db:5432/worktohome
        echo JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
        echo GOOGLE_CLIENT_ID=your-google-client-id
        echo GITHUB_CLIENT_ID=your-github-client-id
        echo MAPBOX_ACCESS_TOKEN=your-mapbox-token
    ) > backend\.env
    echo ✅ Backend .env file created
)

if not exist "frontend\.env" (
    echo 📝 Creating frontend .env file...
    (
        echo REACT_APP_API_URL=http://localhost:5000
        echo REACT_APP_MAPBOX_TOKEN=your-mapbox-token
    ) > frontend\.env
    echo ✅ Frontend .env file created
)

echo 🔧 Building and starting services...
docker-compose up --build -d

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo 📊 Checking service status...
docker-compose ps

echo.
echo 🎉 Setup complete!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:5000
echo 🗄️  Database: localhost:5432
echo.
echo 📝 Next steps:
echo 1. Update the .env files with your API keys
echo 2. Visit http://localhost:3000 to start using the application
echo 3. Run 'docker-compose logs -f' to view logs
echo 4. Run 'docker-compose down' to stop services
echo.
echo 🔍 For development:
echo - Backend logs: docker-compose logs -f backend
echo - Frontend logs: docker-compose logs -f frontend
echo - Database access: docker-compose exec db psql -U postgres -d worktohome
echo.
pause
