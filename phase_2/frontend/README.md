# Next.js Todo Application

This is the frontend for the Todo application built with Next.js 14+, TypeScript, and Tailwind CSS. It integrates with a backend API for authentication and task management.

## Features

- **Authentication**: JWT-based authentication with login/register functionality
- **Task Management**: Full CRUD operations for tasks
- **Real-time Updates**: SWR-based polling for live updates
- **Responsive Design**: Mobile-first responsive UI with Tailwind CSS
- **Type Safety**: TypeScript for type-safe development
- **Modern UI**: Clean, accessible interface with proper error handling

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: SWR for server state, React Context for auth state
- **Forms**: React Hook Form with Zod validation
- **Icons**: Inline SVG icons

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx (root layout with auth provider)
│   ├── page.tsx (home page)
│   ├── login/ (login page)
│   ├── register/ (registration page)
│   ├── dashboard/ (dashboard page)
│   └── tasks/ (task management pages)
├── components/
│   ├── ui/ (reusable UI components)
│   ├── auth/ (authentication components)
│   ├── tasks/ (task management components)
│   └── layout/ (layout components)
├── lib/
│   ├── api/ (API client and services)
│   ├── auth/ (authentication utilities)
│   └── types/ (TypeScript types)
├── hooks/ (custom React hooks)
├── utils/ (utility functions)
└── styles/ (additional styles)
```

## Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## API Integration

The app communicates with the backend API through:

- Authentication: `/api/v1/login`, `/api/v1/register`
- Tasks: `/api/v1/tasks/` endpoints
- The API client handles JWT token management automatically.