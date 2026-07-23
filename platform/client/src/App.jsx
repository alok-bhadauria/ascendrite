import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import LandingPage from './pages/LandingPage';
import { ProtectedRoute, CapabilityGate } from './router/RouteGuards';
import { Spinner } from './components/primitives/Spinner';

import AppLayout from './components/layout/AppLayout';

// Lazy load page views
const LearnPage = lazy(() => import('./pages/LearnPage'));
const WorkspacePage = lazy(() => import('./pages/WorkspacePage'));
const CreatorPage = lazy(() => import('./pages/CreatorPage'));
const AdminPage = lazy(() => import('./pages/AdminPage'));
const ForbiddenPage = lazy(() => import('./pages/ForbiddenPage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'));

// Setup global TanStack Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div id="app-content" className="min-h-screen flex flex-col justify-between bg-theme-bg text-theme-text transition-all duration-200">
          <Navbar />
          
          <main className="flex-1 flex flex-col w-full relative">
            <Suspense fallback={
              <div className="flex-1 flex items-center justify-center min-h-[50vh]">
                <Spinner size="lg" />
              </div>
            }>
              <Routes>
                {/* Public and Auth overlay entry routes */}
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LandingPage />} />
                <Route path="/forbidden" element={<ForbiddenPage />} />

                {/* Protected client channels */}
                <Route element={<ProtectedRoute />}>
                  <Route element={<AppLayout />}>
                    <Route path="/learn" element={<LearnPage />} />
                    <Route path="/workspace" element={<WorkspacePage />} />
                    
                    {/* Creator authoring channel */}
                    <Route element={<CapabilityGate requiredCapability="creator:write" />}>
                      <Route path="/creator" element={<CreatorPage />} />
                    </Route>

                    {/* Governance admin channel */}
                    <Route element={<CapabilityGate requiredCapability="admin:write" />}>
                      <Route path="/admin" element={<AdminPage />} />
                    </Route>
                  </Route>
                </Route>

                {/* 404 handler fallback */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </Suspense>
          </main>

          <Footer />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
