#!/bin/bash

echo "🚀 Setting up Work-To-Home Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create environment files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cat > backend/.env << EOF
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=postgresql://postgres:password@db:5432/worktohome
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
GOOGLE_CLIENT_ID=your-google-client-id
GITHUB_CLIENT_ID=your-github-client-id
MAPBOX_ACCESS_TOKEN=your-mapbox-token
EOF
    echo "✅ Backend .env file created"
fi

if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend .env file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:5000
REACT_APP_MAPBOX_TOKEN=your-mapbox-token
EOF
    echo "✅ Frontend .env file created"
fi

echo "🔧 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "📊 Checking service status..."
docker-compose ps

echo "🎉 Setup complete!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📝 Next steps:"
echo "1. Update the .env files with your API keys"
echo "2. Visit http://localhost:3000 to start using the application"
echo "3. Run 'docker-compose logs -f' to view logs"
echo "4. Run 'docker-compose down' to stop services"
echo ""
echo "🔍 For development:"
echo "- Backend logs: docker-compose logs -f backend"
echo "- Frontend logs: docker-compose logs -f frontend"
echo "- Database access: docker-compose exec db psql -U postgres -d worktohome"
