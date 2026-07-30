import { SUBDOMAINS } from '../config/env';

/**
 * Resolves the fully qualified URL or local route path for a given sub-app and sub-path.
 * @param {'learner'|'creator'|'admin'|'api'|'docs'} appName 
 * @param {string} path 
 * @returns {string}
 */
export function getAppUrl(appName, path = '') {
  // NOTE: For client side routing parameters context, ensure clean path formats
  // are normalized to prevent route matching gaps.

  const domain = SUBDOMAINS[appName];
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  
  // If subdomain domains are configured (V2), return fully qualified absolute URL
  if (domain) {
    return `${domain}${cleanPath}`;
  }
  
  // Single domain routing path prefixes mapping (V1 fallback)
  const appPrefixes = {
    learner: '/learn',
    creator: '/creator',
    admin: '/admin',
    api: '/api/v1',
    docs: '/docs'
  };
  
  // Handlers for top level pages that don't need prefixes
  if (appName === 'learner' && (path === '/' || path === '/workspace' || path === '/profile' || path === '/collaboration' || path === '/onboarding')) {
    return path;
  }
  
  const prefix = appPrefixes[appName] || '';
  if (path === '/' || path === '') {
    return prefix;
  }
  
  return `${prefix}${cleanPath}`;
}

/**
 * Handles navigation to a specific sub-app route.
 * In V1, performs local React Router navigation.
 * In V2, triggers window.location relocation across subdomain boundaries.
 * @param {Function} navigate - react-router-dom useNavigate instance
 * @param {'learner'|'creator'|'admin'|'docs'} appName 
 * @param {string} path 
 */
export function navigateToApp(navigate, appName, path = '') {
  const domain = SUBDOMAINS[appName];
  if (domain) {
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    window.location.href = `${domain}${cleanPath}`;
  } else {
    const targetPath = getAppUrl(appName, path);
    navigate(targetPath);
  }
}
