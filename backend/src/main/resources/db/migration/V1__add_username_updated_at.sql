-- Add username_updated_at column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS username_updated_at TIMESTAMP;

-- Initialize with the same value as created_at for existing records
UPDATE users SET username_updated_at = created_at WHERE username_updated_at IS NULL;

-- Set default constraint for new records
ALTER TABLE users ALTER COLUMN username_updated_at SET DEFAULT CURRENT_TIMESTAMP;
