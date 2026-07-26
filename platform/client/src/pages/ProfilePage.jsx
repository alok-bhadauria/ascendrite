import React from 'react';
import { useAuthStore } from '../store/authStore';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/primitives/Card';
import { Button } from '../components/primitives/Button';
import { Shield, BookOpen, Trash2 } from 'lucide-react';
import { useToast } from '../components/ui/ToastProvider';

export default function ProfilePage() {
  const { user } = useAuthStore();
  const { showToast } = useToast();

  const handleClearCache = () => {
    // Clear custom user namespaced localStorage keys only
    if (user?.id) {
      let keysRemoved = 0;
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.includes(user.id)) {
          localStorage.removeItem(key);
          keysRemoved++;
        }
      });
      showToast('success', 'Workspace Cache Cleared', `Successfully removed ${keysRemoved} local state caches from your browser.`);
    } else {
      showToast('error', 'Action Failed', 'No active user session detected.');
    }
  };

  const trackNames = {
    'ai': 'Artificial Intelligence',
    'core-cs': 'Core Computer Science',
    'software-engineering': 'Software Engineering',
    'web-development': 'Web Development',
    'explore': 'Explore Track (Unset)'
  };

  return (
    <div className="page-container py-8 flex-1 flex flex-col gap-8 select-none">
      <div>
        <h1 className="font-display font-extrabold text-3xl text-theme-text">Account Settings</h1>
        <p className="text-xs text-theme-subtle mt-1">Manage security details, preferences, and local cache allocations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        {/* Profile Card */}
        <Card className="md:col-span-8">
          <CardHeader className="flex flex-row items-center gap-4 mb-2">
            <div className="w-14 h-14 rounded-2xl bg-theme-accent/10 text-theme-accent font-display font-extrabold text-xl flex items-center justify-center">
              {user?.first_name?.[0] || 'U'}{user?.last_name?.[0] || 'U'}
            </div>
            <div>
              <CardTitle className="text-xl font-bold">{user?.first_name} {user?.last_name}</CardTitle>
              <CardDescription>{user?.email}</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col gap-6 pt-4 border-t border-theme-border/60">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <span className="text-[10px] font-mono text-theme-accent uppercase font-bold tracking-wider">Security Role</span>
                <p className="text-sm font-semibold text-theme-text mt-1 flex items-center gap-1.5">
                  <Shield className="h-4 w-4 text-theme-accent" />
                  {user?.role || 'Student'}
                </p>
              </div>
              <div>
                <span className="text-[10px] font-mono text-theme-accent uppercase font-bold tracking-wider">Active Path Preference</span>
                <p className="text-sm font-semibold text-theme-text mt-1 flex items-center gap-1.5">
                  <BookOpen className="h-4 w-4 text-theme-accent" />
                  {trackNames[user?.preferences?.interest] || trackNames.explore}
                </p>
              </div>
            </div>

            <div>
              <span className="text-[10px] font-mono text-theme-accent uppercase font-bold tracking-wider mb-2 block">System Capabilities</span>
              <div className="flex flex-wrap gap-2">
                {user?.capabilities && user.capabilities.length > 0 ? (
                  user.capabilities.map((cap, idx) => (
                    <span key={idx} className="text-[10px] font-mono font-semibold bg-theme-border/40 border border-theme-border/60 text-theme-text px-2 py-1 rounded-md">
                      {cap}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-theme-subtle">No explicit capabilities list mapped to session principal.</span>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Maintenance Actions Card */}
        <Card className="md:col-span-4">
          <CardHeader>
            <CardTitle>System & Cache</CardTitle>
            <CardDescription>Maintenance operations.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            <div className="bg-theme-bg border border-theme-border rounded-xl p-4">
              <h4 className="text-xs font-bold text-theme-text mb-1">Clear Local Workspace</h4>
              <p className="text-[11px] text-theme-subtle leading-relaxed mb-4">
                Safely wipe browser local storage namespaces (tasks planner, bookmarks, local text notes) allocated to your account.
              </p>
              <Button variant="secondary" className="w-full flex items-center justify-center gap-2" onClick={handleClearCache}>
                <Trash2 className="h-4 w-4" />
                <span>Clear Cache</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
