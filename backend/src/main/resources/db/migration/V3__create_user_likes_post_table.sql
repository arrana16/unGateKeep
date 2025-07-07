-- Create user_likes_post table
CREATE TABLE IF NOT EXISTS user_likes_post (
    id       SERIAL PRIMARY KEY,
    user_id  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id  UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    liked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (user_id, post_id)
);

-- Set the owner to ungate_user
ALTER TABLE user_likes_post OWNER TO ungate_user;
