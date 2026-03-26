# Daily Expenses Tracker - Frontend

This is the frontend for the Daily Expenses Tracker application.

## Environment Configuration

The application uses environment variables to manage different environments. The following environment files are available:

- `.env` - Development environment (default)
- `.env.production` - Production environment

### Environment Variables

- `VITE_API_BASE_URL` - The base URL for the API backend

### Development Environment

By default, the application uses the development environment with the following API URL:
```
http://localhost:8000
```

### Production Environment

For production, update the `.env.production` file with your production API URL:
```
VITE_API_BASE_URL=https://your-production-api.com
```

### How to Use Environment Variables

1. Create or modify the appropriate environment file (`.env` for development, `.env.production` for production)
2. Set the `VITE_API_BASE_URL` variable to your backend API URL
3. The application will automatically use the correct environment variables based on the build mode

### Building for Production

To build the application for production, use the following command:

```bash
npm run build
```

This will create a production-ready build with the production environment variables.
