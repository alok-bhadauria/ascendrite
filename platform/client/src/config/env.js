/**
 * Ascendrite V1 Global Client Environment Configuration
 * Decouples API endpoints, subdomain paths, and OAuth parameters
 * to ensure scalability and ease migration to future V2 subdomain structures.
 */

// Deployment environment selector
export const ENV = import.meta.env.MODE || 'development';

// API services base endpoint configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Google OAuth configuration
// V1: Server maps authentication session onto a main domain cookie
// V2: Cross-subdomain CORS cookies or JWT exchange protocols will be configured here
export const OAUTH_LOGIN_URL = import.meta.env.VITE_OAUTH_LOGIN_URL || 'http://localhost:8000/api/v1/auth/google/login';

// Subdomain routes configuration definitions
// In V1, these resolve to empty strings to keep operations under a single host.
// In V2, these will resolve to target domains (e.g. 'https://studio.ascendrite.com').
export const SUBDOMAINS = {
  learner: import.meta.env.VITE_SUBDOMAIN_LEARNER || '',
  creator: import.meta.env.VITE_SUBDOMAIN_CREATOR || '',
  admin: import.meta.env.VITE_SUBDOMAIN_ADMIN || '',
  api: import.meta.env.VITE_SUBDOMAIN_API || '',
  docs: import.meta.env.VITE_SUBDOMAIN_DOCS || '',
};

// CORS / Authentication cookie attributes configuration recommendations:
// - V1 Dev: SameSite=Lax, Secure=False, Domain=localhost
// - V2 Production: SameSite=Lax, Secure=True, Domain=.ascendrite.com (allows cross-subdomain sessions)
export const AUTH_COOKIE_DOMAIN = import.meta.env.VITE_AUTH_COOKIE_DOMAIN || 'localhost';

// Local dev settings checklist:
// For testing subdomains locally, update hosts mapping in Windows:
// 127.0.0.1  ascendrite.local studio.ascendrite.local admin.ascendrite.local

