-- ==============================================================================
-- ASCENDRITE PostgreSQL Database Schema Initialization Contract (init_postgres.sql)
-- ==============================================================================

-- Enable UUID extension if supported
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── 1. IDENTITY & USERS DOMAIN ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY, -- Supports custom prefix IDs (e.g. usr_123) or UUIDs
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Student', -- Student | Contributor | Admin
    bio TEXT DEFAULT '',
    profile_picture_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_lower ON users (LOWER(email));

CREATE TABLE IF NOT EXISTS user_identities (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL DEFAULT 'local', -- local | google | github
    provider_user_id VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(100),
    failed_login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_provider_user UNIQUE (provider, provider_user_id)
);

CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(64) PRIMARY KEY, -- Session UUID
    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_family_id VARCHAR(100) NOT NULL,
    refresh_token_id VARCHAR(100) NOT NULL,
    device_name VARCHAR(255),
    ip_address VARCHAR(50),
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_reason VARCHAR(255),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);

-- ── 2. WORKSPACE DOMAIN ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS workspace_settings (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    theme VARCHAR(50) NOT NULL DEFAULT 'dark',
    notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workspace_notes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    content TEXT DEFAULT '',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workspace_tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ── 3. COLLABORATION DOMAIN ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS collaboration_teams (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_by VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collaboration_comments (
    id VARCHAR(64) PRIMARY KEY,
    resource_id VARCHAR(100) NOT NULL,
    author_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collaboration_assignments (
    id VARCHAR(64) PRIMARY KEY,
    resource_id VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL, -- topic | content | question | assessment
    assignee_id VARCHAR(64) REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'assigned', -- assigned | in_progress | completed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ── 4. OPERATIONS & AUDIT TELEMETRY ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_telemetry_logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(100) NOT NULL,
    resource_id VARCHAR(100),
    status VARCHAR(50) NOT NULL,
    actor_id VARCHAR(64),
    payload_json JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_telemetry_logs(created_at);
