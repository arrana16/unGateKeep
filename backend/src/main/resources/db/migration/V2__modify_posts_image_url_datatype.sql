-- Modify the image_url column to support longer text for storing multiple URLs
ALTER TABLE posts ALTER COLUMN image_url TYPE TEXT;
