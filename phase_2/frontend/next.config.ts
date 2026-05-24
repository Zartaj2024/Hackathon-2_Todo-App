import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typedRoutes: true,
  // Ensure the app works correctly behind the Hugging Face proxy
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: (process.env.BACKEND_URL || 'http://localhost:8000') + '/api/v1/:path*',
      },
    ];
  },
};

export default nextConfig;
