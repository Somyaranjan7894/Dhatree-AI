import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Sprout, LogIn, ArrowRight, FlaskConical, ScanLine, 
  CloudSun, Bot, BarChart3, Database, ShieldCheck, Cpu, ChevronRight, 
  LayoutDashboard, Menu, X, Smartphone, Check, Shield, FileText, Mail, ArrowDown, ChevronDown
} from "lucide-react";
import { APP_NAME, APP_TAGLINE } from "@/config/constants";
import { Button } from "@/components/common";
import { useAuth } from "@/modules/auth/useAuth";

const Counter: React.FC<{ end: number; suffix?: string; duration?: number; isFloat?: boolean }> = ({ end, suffix = "", duration = 2000, isFloat = false }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp: number | null = null;
    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const easeOut = progress * (2 - progress);
      setCount(isFloat ? Number((easeOut * end).toFixed(1)) : Math.floor(easeOut * end));
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }, [end, duration, isFloat]);

  return <span>{count}{suffix}</span>;
};

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Features", href: "#features" },
    { name: "How It Works", href: "#how-it-works" },
    { name: "Technology", href: "#technology" },
    { name: "Documentation", href: "#" },
    { name: "Contact", href: "#footer" },
  ];

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-white/80 dark:bg-slate-950/80 backdrop-blur-md shadow-sm py-3' : 'bg-transparent py-5'}`}>
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="bg-primary-600 p-1.5 rounded-lg text-white shadow-md">
              <Sprout className="h-6 w-6" />
            </div>
            <span className="font-bold text-xl text-slate-900 dark:text-white">{APP_NAME}</span>
          </Link>
          
          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <a key={link.name} href={link.href} className="text-sm font-semibold text-slate-600 hover:text-primary-600 dark:text-slate-300 dark:hover:text-primary-400 transition-colors">
                {link.name}
              </a>
            ))}
            <Link to="/login">
              <Button variant="outline" size="sm" className="font-bold rounded-lg border-2" leftIcon={<LogIn className="w-4 h-4" />}>
                Sign In
              </Button>
            </Link>
          </nav>

          {/* Mobile Menu Toggle */}
          <button className="md:hidden text-slate-600 dark:text-slate-300 p-2" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} aria-label="Toggle menu">
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-100 dark:border-slate-800 overflow-hidden"
          >
            <div className="container mx-auto px-6 py-4 flex flex-col gap-2">
              {navLinks.map((link) => (
                <a key={link.name} href={link.href} onClick={() => setMobileMenuOpen(false)} className="text-base font-semibold text-slate-600 hover:text-primary-600 dark:text-slate-300 transition-colors py-3 border-b border-slate-50 dark:border-slate-800/50">
                  {link.name}
                </a>
              ))}
              <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="mt-4">
                <Button className="w-full font-bold justify-center rounded-xl py-6" leftIcon={<LogIn className="w-5 h-5" />}>
                  Sign In
                </Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

export const Landing: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  if (!loading && isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const features = [
    { icon: Sprout, title: "Crop Recommendation", desc: "Recommend the most suitable crop using soil and environmental conditions." },
    { icon: FlaskConical, title: "Fertilizer Recommendation", desc: "Receive intelligent fertilizer recommendations based on soil analysis." },
    { icon: ScanLine, title: "Disease Detection", desc: "Detect crop diseases instantly using AI-powered image recognition." },
    { icon: CloudSun, title: "Weather Intelligence", desc: "Access farm-specific weather forecasts and smart agricultural advisories." },
    { icon: Bot, title: "AI Farming Assistant", desc: "Get expert agricultural guidance using Gemini AI." },
    { icon: BarChart3, title: "Smart Analytics", desc: "Monitor farms, predictions, recommendations, and AI insights." }
  ];

  const reasons = [
    "AI-powered recommendations",
    "Production-ready Machine Learning",
    "Farm-specific Weather Intelligence",
    "Smart Disease Detection",
    "Responsive on Desktop & Mobile",
    "Secure Cloud Architecture",
    "Modern User Experience",
    "Fast AI Predictions"
  ];

  const techStack = [
    "Python", "Django", "React", "TypeScript", "TensorFlow", "Scikit-learn", 
    "Gemini AI", "PostgreSQL", "Redis", "Tailwind CSS", "Docker"
  ];

  const trustBadges = [
    { icon: Cpu, label: "AI Powered" },
    { icon: CloudSun, label: "Real-Time Weather" },
    { icon: ScanLine, label: "39 Disease Classes" },
    { icon: Smartphone, label: "Mobile Friendly" },
    { icon: ShieldCheck, label: "Secure Platform" }
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 font-sans text-slate-800 dark:text-slate-200 selection:bg-primary-500 selection:text-white">
      <Navbar />

      {/* 1. HERO SECTION */}
      <section className="relative pt-32 pb-20 lg:pt-40 lg:pb-28 overflow-hidden min-h-screen flex flex-col justify-center">
        <div className="absolute inset-0 z-0 pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-primary-400/20 dark:bg-primary-900/30 rounded-full mix-blend-multiply blur-3xl animate-pulse" style={{ animationDuration: '8s' }} />
          <div className="absolute top-[20%] right-[-10%] w-[30rem] h-[30rem] bg-green-400/20 dark:bg-green-900/20 rounded-full mix-blend-multiply blur-3xl animate-pulse" style={{ animationDuration: '10s' }} />
          <div className="absolute bottom-[-20%] left-[20%] w-[40rem] h-[40rem] bg-emerald-400/20 dark:bg-emerald-900/20 rounded-full mix-blend-multiply blur-3xl animate-pulse" style={{ animationDuration: '12s' }} />
        </div>
        
        <div className="container mx-auto px-6 relative z-10 text-center flex flex-col items-center flex-grow justify-center mt-10">
          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 260, damping: 20 }}>
            <div className="h-20 w-20 mb-8 rounded-3xl bg-gradient-to-br from-primary-500 to-primary-700 text-white flex items-center justify-center shadow-2xl shadow-primary-500/30">
              <Sprout className="h-10 w-10" />
            </div>
          </motion.div>
          
          <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-6">
            {APP_NAME}
          </motion.h1>
          <motion.h2 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="text-xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-green-500 mb-6 max-w-3xl">
            {APP_TAGLINE}
          </motion.h2>
          <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="text-lg md:text-xl text-slate-600 dark:text-slate-400 mb-10 max-w-3xl leading-relaxed">
            Empower your farm with AI-powered crop recommendations, disease detection, fertilizer planning, weather intelligence, and an intelligent farming assistant—all in one platform.
          </motion.p>
          
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto mb-16">
            <Link to="/login" className="w-full sm:w-auto">
              <Button size="lg" className="w-full text-base font-bold px-8 py-6 rounded-xl shadow-xl shadow-primary-500/20 hover:-translate-y-1 transition-all" leftIcon={<LogIn className="w-5 h-5" />}>
                Sign In
              </Button>
            </Link>
            <Link to="/register" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="w-full text-base font-bold px-8 py-6 rounded-xl border-2 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm hover:bg-white dark:hover:bg-slate-800 hover:-translate-y-1 transition-all" rightIcon={<ArrowRight className="w-5 h-5" />}>
                Get Started
              </Button>
            </Link>
          </motion.div>

          {/* Trust Badges */}
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8, duration: 1 }} className="flex flex-wrap justify-center gap-4 md:gap-8 text-slate-600 dark:text-slate-400">
            {trustBadges.map((badge, idx) => (
              <div key={idx} className="flex items-center gap-2 text-sm font-semibold bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm px-4 py-2 rounded-full border border-slate-200/50 dark:border-slate-700/50 shadow-sm">
                <badge.icon className="h-4 w-4 text-primary-500" />
                <span>{badge.label}</span>
              </div>
            ))}
          </motion.div>
        </div>
        
        {/* Scroll Down Indicator */}
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          transition={{ delay: 1.5, duration: 1 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-slate-400"
        >
          <span className="text-xs uppercase tracking-widest font-bold">Scroll</span>
          <motion.div animate={{ y: [0, 8, 0] }} transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}>
            <ArrowDown className="h-5 w-5" />
          </motion.div>
        </motion.div>
      </section>

      {/* 2. FEATURES SECTION */}
      <section id="features" className="py-24 bg-white dark:bg-slate-900 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Everything Farmers Need in One Platform
            </motion.h2>
            <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg text-slate-600 dark:text-slate-400">
              Core AI modules designed to optimize your agricultural yield.
            </motion.p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <motion.div 
                key={idx} 
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="group p-8 rounded-[2rem] border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 hover:bg-white dark:hover:bg-slate-800 hover:-translate-y-2 hover:shadow-2xl hover:shadow-primary-500/5 transition-all duration-300"
              >
                <div className="h-14 w-14 rounded-2xl bg-primary-100 dark:bg-primary-900/50 text-primary-600 dark:text-primary-400 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-primary-500 group-hover:text-white transition-all duration-300 shadow-sm">
                  <feature.icon className="h-7 w-7" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">{feature.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed font-medium">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* 3. WHY CHOOSE DHATREE AI */}
      <section className="py-24 bg-slate-50 dark:bg-slate-950">
        <div className="container mx-auto px-6">
          <div className="flex flex-col lg:flex-row items-center gap-16">
            <div className="lg:w-1/2">
              <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-6">
                Why Choose {APP_NAME}?
              </motion.h2>
              <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg text-slate-600 dark:text-slate-400 mb-10 leading-relaxed">
                Built from the ground up to solve complex agricultural problems using state-of-the-art machine learning models and intuitive interfaces.
              </motion.p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {reasons.map((reason, idx) => (
                  <motion.div 
                    key={idx} 
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex items-center gap-3 bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm hover:border-primary-200 dark:hover:border-primary-800 hover:shadow-md transition-all"
                  >
                    <div className="bg-primary-100 dark:bg-primary-900/50 rounded-full p-1 text-primary-600 dark:text-primary-400 shrink-0">
                      <Check className="h-4 w-4 stroke-[3]" />
                    </div>
                    <span className="text-sm font-bold text-slate-700 dark:text-slate-300">{reason}</span>
                  </motion.div>
                ))}
              </div>
            </div>
            <div className="lg:w-1/2 w-full">
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                className="relative rounded-[2rem] overflow-hidden shadow-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-10"
              >
                <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-primary-500 via-green-500 to-emerald-500" />
                <div className="absolute -right-10 -top-10 w-40 h-40 bg-primary-500/10 rounded-full blur-3xl" />
                <div className="absolute -left-10 -bottom-10 w-40 h-40 bg-green-500/10 rounded-full blur-3xl" />
                
                <div className="flex flex-col gap-8 relative z-10">
                  <div className="flex items-center gap-5">
                    <div className="bg-primary-50 dark:bg-slate-800 p-4 rounded-2xl text-primary-500 shadow-sm">
                      <ShieldCheck className="h-10 w-10" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-slate-900 dark:text-white">Enterprise Grade Security</h3>
                      <p className="text-slate-500 font-medium mt-1">Secure, scalable, and reliable cloud infrastructure.</p>
                    </div>
                  </div>
                  
                  <div className="space-y-6 mt-4">
                    {[
                      { label: "Data Encryption", val: 100 },
                      { label: "Uptime Reliability", val: 99.9 },
                      { label: "API Performance", val: 95 }
                    ].map((item, i) => (
                      <div key={i}>
                        <div className="flex justify-between text-sm mb-2 font-bold">
                          <span className="text-slate-700 dark:text-slate-300">{item.label}</span>
                          <span className="text-primary-600">{item.val}%</span>
                        </div>
                        <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                          <motion.div 
                            initial={{ width: 0 }}
                            whileInView={{ width: `${item.val}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 1.5, delay: 0.5 + i * 0.2 }}
                            className="h-full bg-gradient-to-r from-primary-500 to-green-500 rounded-full" 
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. PLATFORM STATISTICS */}
      <section className="py-24 bg-slate-900 dark:bg-slate-950 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-primary-900/10 mix-blend-multiply" />
        <div className="absolute inset-0 bg-[url('/vite.svg')] opacity-5 bg-repeat bg-[length:100px_100px]" />
        
        <div className="container mx-auto px-6 relative z-10">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-10 text-center divide-x divide-slate-800/50">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="flex flex-col items-center justify-center">
              <span className="text-4xl md:text-5xl font-extrabold mb-3 text-white"><Counter end={39} suffix="+" /></span>
              <span className="text-primary-400 text-sm md:text-base font-bold uppercase tracking-wider">Disease Classes</span>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="flex flex-col items-center justify-center border-l border-slate-800/50">
              <span className="text-4xl md:text-5xl font-extrabold mb-3 text-white"><Counter end={98.5} isFloat suffix="%" /></span>
              <span className="text-primary-400 text-sm md:text-base font-bold uppercase tracking-wider">Model Accuracy</span>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }} className="flex flex-col items-center justify-center border-l-0 md:border-l border-slate-800/50 pt-8 md:pt-0">
              <span className="text-4xl md:text-5xl font-extrabold mb-3 text-white"><Counter end={55} suffix=",000+" /></span>
              <span className="text-primary-400 text-sm md:text-base font-bold uppercase tracking-wider">Training Images</span>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.3 }} className="flex flex-col items-center justify-center border-l border-slate-800/50 pt-8 lg:pt-0">
              <span className="text-4xl md:text-5xl font-extrabold mb-3 text-white"><Counter end={6} suffix="+" /></span>
              <span className="text-primary-400 text-sm md:text-base font-bold uppercase tracking-wider">AI Modules</span>
            </motion.div>
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.4 }} className="flex flex-col items-center justify-center col-span-2 md:col-span-1 lg:col-span-1 border-l-0 lg:border-l border-slate-800/50 pt-8 lg:pt-0">
              <span className="text-4xl md:text-5xl font-extrabold mb-3 text-white">24/7</span>
              <span className="text-primary-400 text-sm md:text-base font-bold uppercase tracking-wider">AI Assistant</span>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 5. HOW IT WORKS */}
      <section id="how-it-works" className="py-32 bg-white dark:bg-slate-900">
        <div className="container mx-auto px-6">
          <div className="text-center mb-24">
            <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              How It Works
            </motion.h2>
            <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg text-slate-600 dark:text-slate-400">
              A seamless process from data entry to intelligent insights.
            </motion.p>
          </div>
          
          <div className="flex flex-col md:flex-row items-start justify-between gap-12 md:gap-4 relative max-w-6xl mx-auto">
            {/* Connecting Line for Desktop */}
            <div className="hidden md:block absolute top-12 left-[10%] right-[10%] h-1 bg-slate-100 dark:bg-slate-800 -z-10 rounded-full" />
            
            {[
              { step: 1, title: "Create Your Farm", icon: Database },
              { step: 2, title: "Upload Soil & Crop Details", icon: Sprout },
              { step: 3, title: "AI Analyses Your Farm", icon: Cpu },
              { step: 4, title: "Receive Smart Recommendations", icon: BarChart3 }
            ].map((item, idx, arr) => (
              <React.Fragment key={item.step}>
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.2 }}
                  className="flex flex-col items-center text-center w-full md:w-1/4 group"
                >
                  <div className="h-24 w-24 rounded-full bg-white dark:bg-slate-900 border-[8px] border-slate-50 dark:border-slate-950 flex items-center justify-center mb-6 group-hover:border-primary-100 dark:group-hover:border-primary-900/50 transition-all duration-300 relative z-10 shadow-[0_0_0_2px_theme(colors.slate.200)] dark:shadow-[0_0_0_2px_theme(colors.slate.800)] group-hover:shadow-[0_0_0_2px_theme(colors.primary.500)] group-hover:-translate-y-2 group-hover:bg-primary-50 dark:group-hover:bg-primary-900/20">
                    <item.icon className="h-10 w-10 text-slate-400 group-hover:text-primary-600 dark:group-hover:text-primary-500 transition-colors" />
                    <div className="absolute -top-2 -right-2 h-8 w-8 bg-primary-500 text-white rounded-full flex items-center justify-center font-bold shadow-lg text-sm">
                      {item.step}
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">{item.title}</h3>
                </motion.div>
                {/* Arrow for mobile */}
                {idx < arr.length - 1 && (
                  <div className="md:hidden text-slate-300 dark:text-slate-700 self-center -mt-6 -mb-6">
                    <ChevronDown className="h-8 w-8" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>

      {/* 6. APPLICATION PREVIEW */}
      <section className="py-24 bg-slate-50 dark:bg-slate-950 overflow-hidden">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Application Preview
            </motion.h2>
            <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg text-slate-600 dark:text-slate-400">
              Experience a beautifully crafted, responsive interface.
            </motion.p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {/* Dashboard Mock */}
            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden hover:-translate-y-2 transition-transform duration-300">
              <div className="h-12 bg-slate-100 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 flex items-center px-5 gap-2">
                <div className="flex gap-2"><div className="h-3 w-3 rounded-full bg-red-400" /><div className="h-3 w-3 rounded-full bg-yellow-400" /><div className="h-3 w-3 rounded-full bg-green-400" /></div>
                <span className="mx-auto text-xs font-bold text-slate-500 flex items-center gap-2 uppercase tracking-wider"><LayoutDashboard className="h-4 w-4" /> Dashboard</span>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="h-28 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 flex flex-col justify-center px-4"><div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/50 mb-3 flex items-center justify-center text-primary-500"><Sprout className="w-5 h-5"/></div><div className="h-2 w-1/2 bg-slate-200 dark:bg-slate-700 rounded mb-2"></div><div className="h-4 w-3/4 bg-slate-300 dark:bg-slate-600 rounded"></div></div>
                  <div className="h-28 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 flex flex-col justify-center px-4"><div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/50 mb-3 flex items-center justify-center text-green-500"><CloudSun className="w-5 h-5"/></div><div className="h-2 w-1/2 bg-slate-200 dark:bg-slate-700 rounded mb-2"></div><div className="h-4 w-3/4 bg-slate-300 dark:bg-slate-600 rounded"></div></div>
                </div>
                <div className="h-32 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 w-full flex items-end p-5 gap-3">
                   <div className="flex-1 bg-primary-200 dark:bg-primary-900/40 h-1/3 rounded-t-sm"></div><div className="flex-1 bg-primary-300 dark:bg-primary-800/50 h-1/2 rounded-t-sm"></div><div className="flex-1 bg-primary-400 dark:bg-primary-700/60 h-3/4 rounded-t-sm"></div><div className="flex-1 bg-primary-500 h-full rounded-t-sm shadow-md"></div><div className="flex-1 bg-primary-400 dark:bg-primary-700/60 h-2/3 rounded-t-sm"></div><div className="flex-1 bg-primary-300 dark:bg-primary-800/50 h-1/3 rounded-t-sm"></div>
                </div>
              </div>
            </motion.div>

            {/* Disease Detection Mock */}
            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden hover:-translate-y-2 transition-transform duration-300">
              <div className="h-12 bg-slate-100 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 flex items-center px-5 gap-2">
                <div className="flex gap-2"><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /></div>
                <span className="mx-auto text-xs font-bold text-slate-500 flex items-center gap-2 uppercase tracking-wider"><ScanLine className="h-4 w-4" /> Disease Detection</span>
              </div>
              <div className="p-6 flex flex-col h-full gap-5">
                <div className="w-full h-44 border-2 border-dashed border-primary-300 dark:border-primary-800 rounded-2xl flex flex-col items-center justify-center bg-primary-50 dark:bg-primary-900/10 text-primary-500">
                  <ScanLine className="h-12 w-12 mb-3 opacity-50" />
                  <span className="text-sm font-bold opacity-80">Upload Leaf Image</span>
                </div>
                <div className="flex flex-col gap-3 mt-auto">
                  <div className="h-10 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-900/50 w-full flex items-center px-4 gap-3"><div className="w-2.5 h-2.5 rounded-full bg-red-500"></div><div className="h-2.5 w-1/3 bg-red-200 dark:bg-red-800/80 rounded-full"></div></div>
                  <div className="h-20 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 w-full p-4 flex flex-col justify-center"><div className="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full mb-3"></div><div className="h-2 w-5/6 bg-slate-200 dark:bg-slate-700 rounded-full"></div></div>
                </div>
              </div>
            </motion.div>

            {/* AI Assistant Mock */}
            <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }} className="rounded-[2rem] border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-2xl overflow-hidden hover:-translate-y-2 transition-transform duration-300 hidden lg:block">
              <div className="h-12 bg-slate-100 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 flex items-center px-5 gap-2">
                <div className="flex gap-2"><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /><div className="h-3 w-3 rounded-full bg-slate-300 dark:bg-slate-700" /></div>
                <span className="mx-auto text-xs font-bold text-slate-500 flex items-center gap-2 uppercase tracking-wider"><Bot className="h-4 w-4" /> AI Assistant</span>
              </div>
              <div className="p-6 flex flex-col h-full bg-slate-50/30 dark:bg-slate-900/30">
                <div className="flex-grow flex flex-col gap-6 mb-4 mt-2">
                  <div className="flex justify-end">
                    <div className="bg-primary-500 text-white p-4 rounded-2xl rounded-tr-sm text-sm w-4/5 shadow-md font-medium leading-relaxed">
                      How much nitrogen does my wheat crop need?
                    </div>
                  </div>
                  <div className="flex justify-start items-start gap-3">
                    <div className="bg-gradient-to-br from-primary-500 to-green-600 rounded-full p-2 text-white shrink-0 shadow-md"><Bot className="h-5 w-5" /></div>
                    <div className="bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 p-4 rounded-2xl rounded-tl-sm text-sm w-[85%] shadow-md">
                      <div className="h-2 w-full bg-slate-100 dark:bg-slate-700 rounded-full mb-3"></div><div className="h-2 w-full bg-slate-100 dark:bg-slate-700 rounded-full mb-3"></div><div className="h-2 w-3/4 bg-slate-100 dark:bg-slate-700 rounded-full"></div>
                    </div>
                  </div>
                </div>
                <div className="h-12 mt-auto bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full flex items-center px-5 shadow-sm">
                  <div className="h-3 w-1/3 bg-slate-200 dark:bg-slate-700 rounded-full"></div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 7. TECHNOLOGY STACK */}
      <section id="technology" className="py-24 bg-white dark:bg-slate-900">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Powered By Modern Technologies
            </motion.h2>
            <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg text-slate-600 dark:text-slate-400">
              Built with a robust, scalable, and secure architecture.
            </motion.p>
          </div>
          <motion.div 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ staggerChildren: 0.1 }}
            className="flex flex-wrap justify-center gap-4 max-w-5xl mx-auto"
          >
            {techStack.map(tech => (
              <motion.span 
                key={tech}
                whileHover={{ scale: 1.05 }}
                className="px-6 py-3 rounded-2xl bg-slate-50 dark:bg-slate-800/50 text-slate-700 dark:text-slate-300 font-bold border border-slate-200 dark:border-slate-700 hover:border-primary-500 dark:hover:border-primary-500 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 hover:shadow-lg transition-all cursor-default flex items-center gap-2"
              >
                <Cpu className="h-4 w-4 opacity-50" />
                {tech}
              </motion.span>
            ))}
          </motion.div>
        </div>
      </section>

      {/* 8. CALL TO ACTION */}
      <section className="py-32 bg-gradient-to-br from-primary-600 via-primary-700 to-green-800 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-black/20 rounded-full blur-3xl translate-y-1/3 -translate-x-1/3" />
        <div className="container mx-auto px-6 text-center relative z-10">
          <motion.h2 initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white mb-6">
            Ready to Transform Agriculture?
          </motion.h2>
          <motion.p initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }} className="text-lg md:text-xl text-primary-100 mb-12 max-w-2xl mx-auto font-medium">
            Join Dhatree AI and experience intelligent farming powered by artificial intelligence.
          </motion.p>
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.2 }} className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/login" className="w-full sm:w-auto">
              <Button size="lg" className="w-full bg-white text-primary-800 hover:bg-slate-50 border-0 px-10 py-6 rounded-xl font-bold shadow-2xl shadow-black/20 transition-transform hover:-translate-y-1">
                Sign In
              </Button>
            </Link>
            <Link to="/register" className="w-full sm:w-auto">
              <Button size="lg" className="w-full bg-transparent border-2 border-white text-white hover:bg-white/10 px-10 py-6 rounded-xl font-bold transition-transform hover:-translate-y-1">
                Create Account
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* 9. FOOTER */}
      <footer id="footer" className="bg-slate-950 text-slate-400 py-20 border-t border-slate-900 relative">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-slate-800 to-transparent"></div>
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
            <div className="col-span-1 md:col-span-2 lg:col-span-1">
              <div className="flex items-center gap-3 text-white mb-6">
                <div className="bg-gradient-to-br from-primary-500 to-primary-700 p-2.5 rounded-xl shadow-lg"><Sprout className="h-6 w-6" /></div>
                <span className="font-extrabold text-2xl tracking-tight">{APP_NAME}</span>
              </div>
              <p className="text-sm leading-relaxed mb-6 font-medium opacity-80">
                AI-Powered Digital Agriculture Platform providing crop recommendations, disease detection, and weather intelligence.
              </p>
            </div>
            
            <div>
              <h4 className="text-white font-bold text-lg mb-6">Links</h4>
              <ul className="space-y-4 text-sm font-semibold">
                <li><a href="#features" className="hover:text-primary-400 transition-colors flex items-center gap-2"><ChevronRight className="h-4 w-4 opacity-50" /> Features</a></li>
                <li><a href="#" className="hover:text-primary-400 transition-colors flex items-center gap-2"><ChevronRight className="h-4 w-4 opacity-50" /> Documentation</a></li>
                <li><a href="#" className="hover:text-primary-400 transition-colors flex items-center gap-2"><ChevronRight className="h-4 w-4 opacity-50" /> GitHub</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-bold text-lg mb-6">Legal</h4>
              <ul className="space-y-4 text-sm font-semibold">
                <li><a href="#" className="hover:text-primary-400 transition-colors flex items-center gap-2"><Shield className="h-4 w-4 opacity-50" /> Privacy Policy</a></li>
                <li><a href="#" className="hover:text-primary-400 transition-colors flex items-center gap-2"><FileText className="h-4 w-4 opacity-50" /> Terms & Conditions</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-bold text-lg mb-6">Contact</h4>
              <ul className="space-y-4 text-sm font-semibold">
                <li><a href="mailto:contact@dhatree.ai" className="hover:text-primary-400 transition-colors flex items-center gap-2"><Mail className="h-4 w-4 opacity-50" /> Contact Support</a></li>
              </ul>
            </div>
          </div>
          
          <div className="pt-8 border-t border-slate-800/50 flex flex-col md:flex-row justify-between items-center gap-4 text-sm font-bold opacity-80">
            <p>© 2026 Dhatree AI. All rights reserved.</p>
            <div className="flex items-center gap-3 bg-slate-900/50 px-4 py-2 rounded-full border border-slate-800">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
              </span>
              <span>All systems operational</span>
              <span className="mx-1 text-slate-700">|</span>
              <span>Version 0.1.0</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
