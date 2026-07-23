import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export function ProtectedRoute() {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to root page but open login modal state or navigate to /login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}

export function CapabilityGate({ requiredCapability }) {
  const { user, isAuthenticated } = useAuthStore();

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
