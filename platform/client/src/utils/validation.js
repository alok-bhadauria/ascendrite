/**
 * Ascendrite V1 Client-Side Validation Utilities
 */

/**
 * Validates if a string matches standard RFC email format regex
 * @param {string} email 
 * @returns {boolean}
 */
export function validateEmail(email) {
  if (!email) return false;
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return regex.test(email.trim());
}

/**
 * Validates password strength according to security standards:
 * - At least 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one numeric digit
 * - At least one special character
 * @param {string} password 
 * @returns {{isValid: boolean, error: string}}
 */
export function validatePassword(password) {
  if (!password) {
    return { isValid: false, error: 'Password is required.' };
  }
  if (password.length < 8) {
    return { isValid: false, error: 'Password must be at least 8 characters long.' };
  }
  if (!/[A-Z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one uppercase letter.' };
  }
  if (!/[a-z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one lowercase letter.' };
  }
  if (!/[0-9]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one numeric digit.' };
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one special character (e.g. !@#$%).' };
  }
  return { isValid: true, error: '' };
}

/**
 * Verifies that all fields in an object are present and not empty
 * @param {Object} fields - key-value pairs of fields to validate
 * @returns {{isValid: boolean, missing: string[]}}
 */
export function validateRequired(fields) {
  const missing = [];
  for (const [key, value] of Object.entries(fields)) {
    if (value === undefined || value === null || (typeof value === 'string' && !value.trim())) {
      missing.push(key);
    }
  }
  return {
    isValid: missing.length === 0,
    missing
  };
}
