import { Card } from '@/components/ui/Card';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export default function Home() {
  return (
    <div className="min-h-screen bg-background selection:bg-primary-200 selection:text-primary-900 transition-colors duration-500 overflow-x-hidden">
      {/* Dynamic Mesh Gradient Background */}
      <div className="fixed inset-0 -z-10 pointer-events-none overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary-500/20 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[10%] right-[-5%] w-[35%] h-[35%] bg-violet-500/10 rounded-full blur-[100px]" />
        <div className="absolute top-[20%] right-[10%] w-[25%] h-[25%] bg-indigo-500/10 rounded-full blur-[80px]" />
      </div>

      <div className="container mx-auto px-6 lg:px-12 relative">
        {/* Navigation */}
        <header className="flex items-center justify-between py-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl premium-gradient flex items-center justify-center text-white font-black text-2xl shadow-glow transform hover:rotate-6 transition-transform">
              T
            </div>
            <span className="font-black text-2xl text-gray-900 dark:text-white tracking-tighter uppercase">
              Todo<span className="text-primary-600">AI</span>
            </span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm font-bold text-gray-500 dark:text-gray-400">
            <Link href={"#features" as any} className="hover:text-primary-600 transition-colors uppercase tracking-widest">Features</Link>
            <Link href={"#ai" as any} className="hover:text-primary-600 transition-colors uppercase tracking-widest">Intelligence</Link>
            <Link href={"/login" as any} className="hover:text-primary-600 transition-colors uppercase tracking-widest">Sign In</Link>
          </nav>
          <div className="flex items-center gap-4">
            <Link href="/register">
              <Button variant="premium" size="sm" className="hidden sm:inline-flex px-6 h-10">
                Get Started
              </Button>
            </Link>
          </div>
        </header>

        {/* Hero Section */}
        <main className="pt-24 pb-32 flex flex-col items-center text-center max-w-5xl mx-auto">
          <div className="inline-flex items-center px-4 py-1.5 rounded-full glass-card text-xs font-black uppercase tracking-[0.2em] text-primary-600 mb-10 border-primary-500/20">
            <span className="flex h-2 w-2 rounded-full bg-primary-600 mr-3 animate-ping" />
            V2.0 is Intelligence Redefined
          </div>

          <h1 className="text-5xl sm:text-7xl md:text-8xl font-black text-gray-900 dark:text-white tracking-tighter leading-[0.9] mb-8">
            Manage tasks with <br />
            <span className="text-gradient">pure precision.</span>
          </h1>

          <p className="text-xl sm:text-2xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-14 leading-relaxed font-medium">
            The minimal, high-performance todo app that leverages AI to help you clear the clutter and focus on what truly matters.
          </p>

          <div className="flex flex-col sm:flex-row gap-6 w-full sm:w-auto">
            <Link href="/register" className="w-full sm:w-auto">
              <Button variant="premium" size="xl" fullWidth className="sm:w-auto shadow-glow group">
                Join the Future
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Button>
            </Link>
            <Link href="/login" className="w-full sm:w-auto">
              <Button variant="outline" size="xl" fullWidth className="sm:w-auto bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm px-10">
                View Demo
              </Button>
            </Link>
          </div>

          {/* Dynamic Scroll Indicator */}
          <div className="mt-24 animate-bounce opacity-40">
            <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </div>
        </main>

        {/* Features Grid */}
        <section id="features" className="py-24 grid grid-cols-1 md:grid-cols-3 gap-10 max-w-7xl mx-auto">
          {[
            {
              title: "Hyper-Organized",
              desc: "Effortless task capturing with deep-level categorization and priority mapping.",
              icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2",
              color: "primary"
            },
            {
              title: "Peak Performance",
              desc: "Built-in productivity metrics and streak tracking to keep your momentum high.",
              icon: "M13 10V3L4 14h7v7l9-11h-7z",
              color: "emerald"
            },
            {
              title: "Absolute Security",
              desc: "Your tasks are encrypted and private. We use industry-standard security protocols.",
              icon: "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z",
              color: "violet"
            }
          ].map((item, i) => (
            <Card key={i} className="group glass-card border-none hover:-translate-y-2 transition-all p-10 cursor-default">
              <div className={`w-14 h-14 rounded-2xl mb-8 flex items-center justify-center transition-all bg-${item.color}-500 group-hover:bg-${item.color}-600 text-white shadow-lg`}>
                <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                </svg>
              </div>
              <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-4 tracking-tight">{item.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 leading-relaxed font-medium text-lg">
                {item.desc}
              </p>
            </Card>
          ))}
        </section>

        {/* AI Intelligence Section */}
        <section id="ai" className="py-24 mb-32 relative rounded-[3rem] overflow-hidden bg-gray-900 shadow-2xl">
          <div className="absolute inset-0 bg-gradient-to-br from-primary-900/40 to-violet-900/40 pointer-events-none" />
          <div className="absolute top-[-20%] right-[-10%] w-[60%] h-[60%] bg-primary-600/30 blur-[150px] rounded-full animate-pulse" />

          <div className="relative z-10 max-w-4xl mx-auto text-center px-10 py-16">
            <div className="inline-flex items-center justify-center p-4 bg-white/10 rounded-2xl mb-10 backdrop-blur-xl border border-white/10 animate-float">
              <svg className="w-10 h-10 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h2 className="text-4xl md:text-6xl font-black text-white mb-8 tracking-tighter">
              The AI Co-Pilot <br />
              for your focus.
            </h2>
            <p className="text-xl text-gray-300 mb-14 leading-relaxed font-medium">
              Summarize your week, prioritize tasks by impact, and break down complex projects into actionable steps—all through a natural conversation.
            </p>
            <Link href={"/chat" as any}>
              <Button size="xl" className="bg-white text-gray-900 hover:bg-gray-100 hover:scale-105 px-10 font-black tracking-wide border-none">
                Talk to the AI
              </Button>
            </Link>
          </div>
        </section>

        <footer className="py-12 flex flex-col items-center gap-6 text-gray-400 dark:text-gray-500 border-t border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-6 font-bold text-xs uppercase tracking-[0.3em]">
            <Link href="/privacy" className="hover:text-primary-500 transition-colors">Privacy</Link>
            <Link href="/terms" className="hover:text-primary-500 transition-colors">Terms</Link>
            <Link href="/dashboard" className="hover:text-primary-500 transition-colors">App</Link>
          </div>
          <p className="text-xs font-medium">© {new Date().getFullYear()} TodoAI System. Developed with Passion.</p>
        </footer>
      </div>
    </div>
  );
}