-- Make the likes column nullable since we're moving to the user_likes_post table
ALTER TABLE posts ALTER COLUMN likes DROP NOT NULL;
