# Auto Trade Sync App - Frontend

Modern React + TypeScript dashboard for managing trading signal automation.

## Features

- 🔐 **Authentication** - JWT-based login and registration
- 📊 **Dashboard** - Real-time statistics and analytics
- 📱 **Channel Management** - Add and manage Telegram channels
- 🏦 **Broker Integration** - Configure multiple broker accounts
- 📈 **Signal Monitoring** - View and track all trading signals
- 🔗 **Channel-Broker Mapping** - Route signals to brokers
- 🎨 **Modern UI** - Clean, responsive design with Tailwind CSS
- ⚡ **Fast** - Powered by Vite for instant HMR

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Routing
- **TanStack Query** - Data fetching and caching
- **Axios** - HTTP client
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **React Hot Toast** - Notifications

## Prerequisites

- Node.js 16+ and npm
- Backend API running on http://localhost:8000

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` if needed (default configuration works with local backend):

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1
```

### 3. Start Development Server

```bash
npm run dev
```

The app will open at **http://localhost:3000**

## Available Scripts

```bash
# Development
npm run dev          # Start dev server with HMR
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Type Checking
tsc --noEmit        # Check TypeScript types
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API service layer
│   │   ├── axios.ts    # Axios instance
│   │   ├── auth.ts     # Authentication API
│   │   ├── channels.ts # Channels API
│   │   ├── brokers.ts  # Brokers API
│   │   └── signals.ts  # Signals API
│   ├── components/
│   │   ├── auth/       # Authentication components
│   │   ├── layout/     # Layout components (Header, Sidebar)
│   │   └── common/     # Reusable UI components
│   ├── pages/          # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Channels.tsx
│   │   ├── Brokers.tsx
│   │   ├── Signals.tsx
│   │   └── Mappings.tsx
│   ├── store/          # State management
│   ├── types/          # TypeScript types
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Usage Guide

### 1. First Time Setup

1. **Start the backend** (in another terminal):
   ```bash
   cd ..
   source venv/bin/activate
   python main.py
   ```

2. **Register a new account**:
   - Open http://localhost:3000
   - Click "Sign up"
   - Fill in username, email, and password
   - You'll be automatically logged in

### 2. Add Telegram Channels

1. Navigate to **Channels** page
2. Click "Add Channel"
3. Enter channel name (e.g., @trading_signals)
4. Add optional description
5. Click "Add Channel"

### 3. Add Brokers

1. Navigate to **Brokers** page
2. Click "Add Broker"
3. Select broker type (Angel One, Zerodha, etc.)
4. Enter broker name and credentials
5. Click "Add Broker"

### 4. Create Mappings

1. Navigate to **Mappings** page
2. Click "Add Mapping"
3. Select a Telegram channel
4. Select a broker
5. Click "Create Mapping"

Signals from the channel will now route to the broker!

### 5. Monitor Signals

1. Navigate to **Signals** page
2. View all received signals
3. Check parsing status
4. See execution details

### 6. View Dashboard

The Dashboard shows:
- Total signals (last 7 days)
- Active channels and brokers
- Success rate
- Top trading symbols
- Latest signals

## API Integration

The frontend automatically connects to the backend API at `http://localhost:8000`.

### Authentication Flow

1. User logs in → receives JWT token
2. Token stored in localStorage
3. All API requests include `Authorization: Bearer <token>`
4. Token expires → automatic logout

### API Endpoints Used

- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Register
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/channels/` - List channels
- `POST /api/v1/channels/` - Create channel
- `DELETE /api/v1/channels/{id}` - Delete channel
- `GET /api/v1/brokers/` - List brokers
- `POST /api/v1/brokers/` - Create broker
- `GET /api/v1/signals/` - List signals
- `GET /api/v1/signals/stats/summary` - Get statistics

## Development

### Adding a New Page

1. Create page component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/layout/Sidebar.tsx`

### Adding a New API Endpoint

1. Add TypeScript types in `src/types/api.ts`
2. Create API function in `src/api/`
3. Use with React Query in component

Example:

```typescript
// In component
const { data, isLoading } = useQuery({
  queryKey: ['my-data'],
  queryFn: myApi.getData,
});
```

### State Management

- **Global state**: Zustand (auth store)
- **Server state**: TanStack Query (API data)
- **Local state**: React useState

### Styling

Using Tailwind CSS utility classes:

```tsx
<div className="bg-white rounded-lg shadow-md p-6">
  <h1 className="text-2xl font-bold text-gray-900">
    Hello World
  </h1>
</div>
```

## Building for Production

```bash
# Build
npm run build

# Preview build
npm run preview
```

The build output is in the `dist/` directory.

### Deployment

Deploy the `dist/` folder to:
- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **Static host**: Upload `dist/` folder

## Troubleshooting

### API Connection Issues

**Problem**: Cannot connect to backend

**Solution**:
```bash
# Check backend is running
curl http://localhost:8000/health

# Check .env configuration
cat .env

# Restart frontend
npm run dev
```

### Login Not Working

**Problem**: Login fails or redirects to login

**Solution**:
- Check backend is running
- Clear browser localStorage
- Check Network tab for API errors

### Build Errors

**Problem**: TypeScript or build errors

**Solution**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Check types
npm run build
```

### Port Already in Use

**Problem**: Port 3000 is already in use

**Solution**:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or run on different port
npm run dev -- --port 3001
```

## Performance Optimization

- ✅ Code splitting with React.lazy()
- ✅ Image optimization
- ✅ Bundle size optimization
- ✅ React Query caching
- ✅ Debounced API calls

## Security

- ✅ JWT token authentication
- ✅ Automatic token refresh handling
- ✅ Protected routes
- ✅ XSS protection
- ✅ CSRF protection via backend

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Create a feature branch
2. Make changes
3. Run linting: `npm run lint`
4. Build: `npm run build`
5. Test thoroughly
6. Submit PR

## License

MIT

## Support

For issues or questions:
- Check backend logs
- Check browser console
- Check Network tab for API errors
- Review this README

## Changelog

### v1.0.0 (2025-01-01)
- Initial release
- Authentication system
- Dashboard with statistics
- Channel management
- Broker management
- Signal monitoring
- Channel-broker mappings
- Responsive design
