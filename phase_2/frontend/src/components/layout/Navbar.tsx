'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/lib/auth/context';

const Navbar = () => {
  const pathname = usePathname();
  const { user, isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path: string) => {
    return pathname === path;
  };

  const navLinks = [
    { href: '/', label: 'Home' },
    ...(isAuthenticated
      ? [
        { href: '/dashboard', label: 'Dashboard' },
        { href: '/tasks', label: 'Tasks' },
        { href: '/chat', label: 'AI Assistant' }
      ]
      : []
    ),
  ];

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 border-b ${scrolled
      ? 'py-3 backdrop-blur-xl bg-background/80 border-gray-200/50 dark:border-gray-800/50'
      : 'py-6 bg-transparent border-transparent'
      }`}>
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex justify-between items-center h-12">
          <div className="flex items-center gap-10">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-9 h-9 rounded-xl premium-gradient flex items-center justify-center text-white font-black text-xl shadow-glow group-hover:scale-110 transition-transform">
                T
              </div>
              <span className="font-black text-xl text-gray-900 dark:text-white tracking-tighter uppercase">
                Todo<span className="text-primary-600">AI</span>
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-2">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href as any}
                  className={`${isActive(link.href)
                    ? 'bg-primary-500/10 text-primary-600 dark:bg-primary-500/15 dark:text-primary-400'
                    : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'
                    } px-4 py-2 rounded-xl text-sm font-bold uppercase tracking-widest transition-all duration-300`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          <div className="flex items-center md:hidden">
            {/* Mobile menu button */}
            <button
              type="button"
              className="p-2 rounded-xl bg-gray-100 dark:bg-gray-800 text-gray-500 hover:text-primary-600 focus:outline-none transition-colors"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span className="sr-only">Open main menu</span>
              <svg
                className={`${mobileMenuOpen ? 'hidden' : 'block'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                className={`${mobileMenuOpen ? 'block' : 'hidden'} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-5">
            {isAuthenticated ? (
              <div className="flex items-center gap-6">
                <div className="flex flex-col items-end">
                  <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Connected as</span>
                  <span className="text-sm font-bold text-gray-900 dark:text-white">{user?.name || user?.email}</span>
                </div>
                <Button variant="outline" size="sm" onClick={logout} className="h-10 px-6">
                  Log Out
                </Button>
              </div>
            ) : (
              <div className="flex gap-4">
                <Link href="/login">
                  <Button variant="ghost" size="sm" className="h-10 px-6 font-black uppercase tracking-widest text-xs">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="premium" size="sm" className="h-10 px-6">
                    Join Free
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className={`md:hidden fixed inset-0 z-40 bg-background/95 backdrop-blur-2xl transition-transform duration-500 ease-in-out ${mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
        }`}>
        <div className="pt-24 pb-12 px-8 space-y-6">
          <div className="space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href as any}
                onClick={() => setMobileMenuOpen(false)}
                className={`${isActive(link.href)
                  ? 'text-primary-600 bg-primary-500/10'
                  : 'text-gray-600 dark:text-gray-300'
                  } block px-6 py-4 rounded-2xl text-xl font-black uppercase tracking-tighter transition-all`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="pt-6 border-t border-gray-200 dark:border-gray-800">
            {isAuthenticated ? (
              <div className="space-y-6">
                <div className="px-6">
                  <div className="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Authenticated as</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">
                    {user?.name || user?.email}
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="lg"
                  fullWidth
                  className="h-14"
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                >
                  Terminate Session
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="outline" fullWidth className="h-14">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="premium" fullWidth className="h-14">
                    Join TodoAI
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export { Navbar };