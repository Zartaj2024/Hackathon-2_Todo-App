import React from 'react';
import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-background py-16 px-6 lg:px-12 border-t border-gray-100 dark:border-gray-800">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="flex flex-col items-center md:items-start gap-4">
            <div className="flex items-center gap-3 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
              <div className="w-8 h-8 rounded-lg premium-gradient flex items-center justify-center text-white font-black text-base">
                T
              </div>
              <span className="font-black text-lg text-gray-900 dark:text-white tracking-tighter uppercase">
                Todo<span className="text-primary-600">AI</span>
              </span>
            </div>
            <p className="text-gray-400 dark:text-gray-500 text-[10px] font-black uppercase tracking-[0.3em]">
              The Intelligent Management Protocol
            </p>
          </div>

          <div className="flex items-center gap-10 font-bold text-xs uppercase tracking-[0.2em]">
            <Link href="/privacy" className="text-gray-400 hover:text-primary-500 transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="text-gray-400 hover:text-primary-500 transition-colors">Terms of Use</Link>
            <Link href={"/help" as any} className="text-gray-400 hover:text-primary-500 transition-colors">Support</Link>
          </div>

          <div className="text-center md:text-right">
            <p className="text-gray-400 dark:text-gray-600 text-[10px] font-black uppercase tracking-[0.1em]">
              &copy; {new Date().getFullYear()} TodoAI Systems Inc. <br />
              All cycles reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export { Footer };