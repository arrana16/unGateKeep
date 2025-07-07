-- Insert test users
DO $$
DECLARE
    test_user1_id UUID := '11111111-1111-1111-1111-111111111111';
    test_user2_id UUID := '22222222-2222-2222-2222-222222222222';
    test_user3_id UUID := '33333333-3333-3333-3333-333333333333';

    test_post1_id UUID := 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
    test_post2_id UUID := 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
    test_post3_id UUID := 'cccccccc-cccc-cccc-cccc-cccccccccccc';
BEGIN
    -- Only insert if the users don't already exist
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = test_user1_id) THEN
        INSERT INTO users (id, auth_id, username, bio, avatar_url, role, created_at, updated_at)
        VALUES 
            (test_user1_id, 'auth0|test1', 'testuser1', 'This is test user 1', 'https://example.com/avatar1.jpg', 'user', NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days'),
            (test_user2_id, 'auth0|test2', 'testuser2', 'This is test user 2', 'https://example.com/avatar2.jpg', 'user', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
            (test_user3_id, 'auth0|test3', 'testuser3', 'This is test user 3', 'https://example.com/avatar3.jpg', 'admin', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days');
    END IF;

    -- Only insert if the posts don't already exist
    IF NOT EXISTS (SELECT 1 FROM posts WHERE id = test_post1_id) THEN
        INSERT INTO posts (id, user_id, image_url, caption, created_at, likes)
        VALUES 
            (test_post1_id, test_user1_id, 'https://example.com/image1.jpg,https://example.com/image1b.jpg', 'Test post 1 with multiple images', NOW() - INTERVAL '6 days', 0),
            (test_post2_id, test_user2_id, 'https://example.com/image2.jpg', 'Test post 2 with single image', NOW() - INTERVAL '4 days', 0),
            (test_post3_id, test_user1_id, 'https://example.com/image3.jpg', 'Another test post from user 1', NOW() - INTERVAL '2 days', 0);
    END IF;

    -- Only insert likes if they don't already exist
    IF NOT EXISTS (SELECT 1 FROM user_likes_post WHERE user_id = test_user1_id AND post_id = test_post2_id) THEN
        -- User1 likes Post2 (from User2)
        INSERT INTO user_likes_post (user_id, post_id, liked_at)
        VALUES (test_user1_id, test_post2_id, NOW() - INTERVAL '3 days');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM user_likes_post WHERE user_id = test_user2_id AND post_id = test_post1_id) THEN
        -- User2 likes Post1 (from User1)
        INSERT INTO user_likes_post (user_id, post_id, liked_at)
        VALUES (test_user2_id, test_post1_id, NOW() - INTERVAL '5 days');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM user_likes_post WHERE user_id = test_user3_id AND post_id = test_post1_id) THEN
        -- User3 likes Post1 (from User1)
        INSERT INTO user_likes_post (user_id, post_id, liked_at)
        VALUES (test_user3_id, test_post1_id, NOW() - INTERVAL '4 days');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM user_likes_post WHERE user_id = test_user3_id AND post_id = test_post2_id) THEN
        -- User3 likes Post2 (from User2)
        INSERT INTO user_likes_post (user_id, post_id, liked_at)
        VALUES (test_user3_id, test_post2_id, NOW() - INTERVAL '3 days');
    END IF;

    -- Output the test data IDs for reference
    RAISE NOTICE 'Test User IDs: %, %, %', test_user1_id, test_user2_id, test_user3_id;
    RAISE NOTICE 'Test Post IDs: %, %, %', test_post1_id, test_post2_id, test_post3_id;

END;
$$;
