import React from 'react';
import { BookOpen, Send } from 'lucide-react';
import { FaGithub, FaTwitter, FaLinkedin } from 'react-icons/fa';
import { Link } from 'react-router-dom';

export default function Footer() {
  const handleNewsletterSubmit = (e) => {
    e.preventDefault();
    alert("Subscription registered successfully.");
  };

  return (
    <footer className="bg-theme-surface border-t border-theme-border mt-20 transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10">
          
          {/* Column 1: Branding and summary */}
          <div className="md:col-span-2 space-y-4">
            <Link to="/" className="flex items-center gap-2 select-none">
              <div className="w-8 h-8 rounded-lg bg-theme-accent text-white flex items-center justify-center font-display font-extrabold text-lg shadow-md">
                A
              </div>
              <span className="font-display font-bold text-xl tracking-tight text-theme-text">
                Ascendrite
              </span>
            </Link>
            <p className="text-sm text-theme-subtle leading-relaxed max-w-sm">
              Engineered for visual learners and industry readiness. Integrating step-by-step algorithms simulation with textbook-grade core curriculum.
            </p>
            
            {/* Social handles */}
            <div className="flex items-center gap-4 pt-2">
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-theme-subtle hover:text-theme-accent transition-colors">
                <FaGithub size={18} />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-theme-subtle hover:text-theme-accent transition-colors">
                <FaTwitter size={18} />
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="text-theme-subtle hover:text-theme-accent transition-colors">
                <FaLinkedin size={18} />
              </a>
            </div>
          </div>

          {/* Column 2: Subject Tracks */}
          <div className="space-y-4">
            <h4 className="font-display font-bold text-sm text-theme-text tracking-wide uppercase">Learning Tracks</h4>
            <ul className="space-y-2 text-xs font-semibold text-theme-subtle">
              <li><a href="#curriculum-grid" className="hover:text-theme-accent transition-colors">Artificial Intelligence</a></li>
              <li><a href="#curriculum-grid" className="hover:text-theme-accent transition-colors">Core Computer Science</a></li>
              <li><a href="#curriculum-grid" className="hover:text-theme-accent transition-colors">Software Engineering</a></li>
              <li><a href="#curriculum-grid" className="hover:text-theme-accent transition-colors">Web Development</a></li>
            </ul>
          </div>

          {/* Column 3: Platform Resources */}
          <div className="space-y-4">
            <h4 className="font-display font-bold text-sm text-theme-text tracking-wide uppercase">Developer Specs</h4>
            <ul className="space-y-2 text-xs font-semibold text-theme-subtle">
              <li><a href="#" className="hover:text-theme-accent transition-colors flex items-center gap-1"><BookOpen size={12} /> HLD spec</a></li>
              <li><a href="#" className="hover:text-theme-accent transition-colors">Database schema</a></li>
              <li><a href="#" className="hover:text-theme-accent transition-colors">Security policies</a></li>
              <li><a href="#" className="hover:text-theme-accent transition-colors">Editorial guidelines</a></li>
            </ul>
          </div>

          {/* Column 4: Newsletter signup */}
          <div className="space-y-4">
            <h4 className="font-display font-bold text-sm text-theme-text tracking-wide uppercase">Weekly Roadmap</h4>
            <p className="text-xs text-theme-subtle leading-relaxed">
              Get updates on new subjects, visualization modules, and assessment updates.
            </p>
            <form onSubmit={handleNewsletterSubmit} className="flex gap-2">
              <input 
                type="email" 
                placeholder="Email address"
                required
                className="bg-theme-bg border border-theme-border rounded-lg px-3 py-2 text-xs focus:border-theme-accent outline-none w-full text-theme-text"
              />
              <button 
                type="submit" 
                className="bg-theme-accent text-white hover:opacity-90 px-3 py-2 rounded-lg transition-all flex items-center justify-center cursor-pointer shadow-md"
              >
                <Send size={12} />
              </button>
            </form>
          </div>
        </div>

        {/* Separator and copyright */}
        <div className="border-t border-theme-border mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-xs text-theme-subtle">
            &copy; {new Date().getFullYear()} Ascendrite Platform. All rights reserved. • Engineered by Team Ascendrite
          </p>
          <div className="flex items-center gap-6 text-[10px] font-bold text-theme-subtle uppercase">
            <a href="#" className="hover:text-theme-accent transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-theme-accent transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-theme-accent transition-colors">System Status</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
