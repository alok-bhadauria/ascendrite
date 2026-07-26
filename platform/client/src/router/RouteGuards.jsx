import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { Spinner } from '../components/primitives/Spinner';

export function ProtectedRoute() {
  const { isAuthenticated, isCheckingSession, user } = useAuthStore();
  const location = useLocation();

  if (isCheckingSession) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-[50vh]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to root page but open login modal state or navigate to /login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Force onboarding if preferences are missing, unless they are already on /onboarding
  const needsOnboarding = user && !user.preferences?.interest;
  if (needsOnboarding && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />;
  }

  return <Outlet />;
}

export function CapabilityGate({ requiredCapability }) {
  const { user, isAuthenticated, isCheckingSession } = useAuthStore();

  if (isCheckingSession) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-[50vh]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Admin bypasses capability checks
  if (user?.role === 'Admin') {
    return <Outlet />;
  }

  const hasCapability = user?.capabilities?.includes(requiredCapability);

  if (!hasCapability) {
    return <Navigate to="/forbidden" replace />;
  }

  return <Outlet />;
}
