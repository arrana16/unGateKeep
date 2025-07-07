import requests
import json
import time
import uuid
from datetime import datetime
from variables import *


def get_auth_token():
    """Get an authentication token from Auth0"""
    print("\n🔐 Getting authentication token...")

    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
        "grant_type": "client_credentials"
    }

    headers = {
        "content-type": "application/json"
    }

    try:
        response = requests.post(AUTH0_TOKEN_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        token_data = response.json()
        print("✅ Auth token received successfully")
        return token_data["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting auth token: {e}")
        print(f"Response content: {response.content}")
        exit(1)


def print_response(response, operation):
    """Print formatted response data"""
    print(f"\n--- {operation} Response (Status: {response.status_code}) ---")
    print(f"Headers: {dict(response.headers)}")

    try:
        formatted_json = json.dumps(response.json(), indent=2)
        print(f"Body: {formatted_json}")
    except json.JSONDecodeError:
        print(f"Body: {response.text}")

    print("-" * 50)


def create_user(token):
    """Create a new user for testing"""
    print("\n➕ Creating a new test user...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Generate a unique username to avoid conflicts
    test_username = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    payload = {
        "username": test_username,
        "bio": "This is a test user for the posts API test script",
        "avatar_url": "https://example.com/avatar.png",
        "role": "user"
    }

    try:
        response = requests.post(f"{USERS_API_URL}/addUser", headers=headers, data=json.dumps(payload))
        print_response(response, "Create User")

        if response.status_code == 201:
            user_id = response.json().get("id")
            print(f"✅ Test user created successfully with ID: {user_id}")
            return user_id, test_username
        else:
            print(f"❌ Failed to create test user: {response.text}")
            return None, test_username
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating test user: {e}")
        return None, test_username


def delete_user(token, user_id):
    """Delete a user account"""
    print(f"\n❌ Deleting test user with ID: {user_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(f"{USERS_API_URL}/{user_id}", headers=headers)
        print_response(response, "Delete User")

        if response.status_code == 200:
            print("✅ Test user deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete test user: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting test user: {e}")
        return False


def create_post(token, image_urls, caption=None):
    """Create a new post"""
    print("\n📝 Creating a new post...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "imageUrls": image_urls,
        "caption": caption
    }

    try:
        response = requests.post(f"{POSTS_API_URL}", headers=headers, data=json.dumps(payload))
        print_response(response, "Create Post")

        if response.status_code == 201:
            post_id = response.json().get("id")
            print(f"✅ Post created successfully with ID: {post_id}")
            return post_id
        else:
            print(f"❌ Failed to create post: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating post: {e}")
        return None


def create_post_with_empty_images(token):
    """Create a post with empty image URLs (should fail)"""
    print("\n❗ Testing post creation with empty image URLs (should fail)...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "imageUrls": [],
        "caption": "This post should fail due to empty image URLs"
    }

    try:
        response = requests.post(f"{POSTS_API_URL}", headers=headers, data=json.dumps(payload))
        print_response(response, "Create Post with Empty Images (Expected Failure)")

        if response.status_code == 400:
            print("✅ Server correctly rejected post with empty image URLs")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}. Server should have rejected this request.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during test: {e}")
        return False


def get_post_by_id(token, post_id):
    """Get a post by its ID"""
    print(f"\n🔍 Getting post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{POSTS_API_URL}/{post_id}", headers=headers)
        print_response(response, "Get Post by ID")

        if response.status_code == 200:
            print("✅ Post retrieved successfully")
            return response.json()
        else:
            print(f"❌ Failed to retrieve post: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting post: {e}")
        return None


def get_post_with_invalid_id(token):
    """Get a post with an invalid ID (should fail)"""
    print("\n❗ Testing post retrieval with invalid ID (should fail)...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    invalid_id = str(uuid.uuid4())  # Random UUID that shouldn't exist

    try:
        response = requests.get(f"{POSTS_API_URL}/{invalid_id}", headers=headers)
        print_response(response, "Get Post with Invalid ID (Expected Failure)")

        if response.status_code == 404:
            print("✅ Server correctly returned 404 for non-existent post")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}. Server should have returned 404.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during test: {e}")
        return False


def get_posts_by_user(token, user_id):
    """Get all posts by a user"""
    print(f"\n🔍 Getting all posts for user with ID: {user_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{POSTS_API_URL}/user/{user_id}", headers=headers)
        print_response(response, "Get Posts by User")

        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Retrieved {len(posts)} posts for user")
            return posts
        else:
            print(f"❌ Failed to retrieve posts: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting posts: {e}")
        return None


def update_post_caption(token, post_id, new_caption):
    """Update a post's caption"""
    print(f"\n✏️ Updating caption for post {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "caption": new_caption
    }

    try:
        response = requests.put(f"{POSTS_API_URL}/{post_id}/caption", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Post Caption")

        if response.status_code == 200:
            print("✅ Caption updated successfully")
            return True
        else:
            print(f"❌ Failed to update caption: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating caption: {e}")
        return False


def update_caption_on_others_post(token, post_id):
    """Attempt to update someone else's post caption (should fail)"""
    print(f"\n❗ Testing caption update on someone else's post (should fail)...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "caption": "This update should fail - unauthorized"
    }

    try:
        response = requests.put(f"{POSTS_API_URL}/{post_id}/caption", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Others' Post Caption (Expected Failure)")

        if response.status_code in [401, 403]:
            print("✅ Server correctly rejected unauthorized caption update")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}. Server should have rejected this request.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during test: {e}")
        return False


def like_post(token, post_id):
    """Like a post"""
    print(f"\n👍 Liking post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(f"{POSTS_API_URL}/{post_id}/like", headers=headers)
        print_response(response, "Like Post")

        if response.status_code == 200:
            print("✅ Post liked successfully")
            return response.json()
        else:
            print(f"❌ Failed to like post: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error liking post: {e}")
        return None


def unlike_post(token, post_id):
    """Unlike a post (by liking it again)"""
    print(f"\n👎 Unliking post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(f"{POSTS_API_URL}/{post_id}/like", headers=headers)
        print_response(response, "Unlike Post")

        if response.status_code == 200:
            print("✅ Post unliked successfully")
            return response.json()
        else:
            print(f"❌ Failed to unlike post: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error unliking post: {e}")
        return None


def get_like_status(token, post_id):
    """Get like status for a post"""
    print(f"\n👍 Getting like status for post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{POSTS_API_URL}/{post_id}/like/status", headers=headers)
        print_response(response, "Get Like Status")

        if response.status_code == 200:
            print("✅ Like status retrieved successfully")
            return response.json()
        else:
            print(f"❌ Failed to get like status: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting like status: {e}")
        return None


def get_post_likes(token, post_id):
    """Get users who liked a post"""
    print(f"\n👨‍👩‍👧‍👦 Getting users who liked post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{POSTS_API_URL}/{post_id}/likes", headers=headers)
        print_response(response, "Get Post Likes")

        if response.status_code == 200:
            users = response.json()
            print(f"✅ Retrieved {len(users)} users who liked the post")
            return users
        else:
            print(f"❌ Failed to get post likes: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting post likes: {e}")
        return None


def delete_post(token, post_id):
    """Delete a post"""
    print(f"\n🗑️ Deleting post with ID: {post_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(f"{POSTS_API_URL}/{post_id}", headers=headers)
        print_response(response, "Delete Post")

        if response.status_code == 200:
            print("✅ Post deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete post: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting post: {e}")
        return False


def delete_others_post(token, post_id):
    """Attempt to delete someone else's post (should fail)"""
    print(f"\n❗ Testing deletion of someone else's post (should fail)...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(f"{POSTS_API_URL}/{post_id}", headers=headers)
        print_response(response, "Delete Others' Post (Expected Failure)")

        if response.status_code in [401, 403]:
            print("✅ Server correctly rejected unauthorized post deletion")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}. Server should have rejected this request.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during test: {e}")
        return False


def run_tests():
    """Run all the Post API tests in sequence"""
    print("\n🧪 STARTING POST API TESTS 🧪")
    print("=" * 50)

    # Get authentication token
    token = get_auth_token()

    # Create a user for testing
    user_id, username = create_user(token)

    if not user_id:
        print("❌ Cannot proceed with tests without a test user")
        return

    # 1. Test creating a post with valid data
    post_id = create_post(
        token, 
        ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        "Test post with multiple images"
    )

    if not post_id:
        print("❌ Cannot proceed with further tests without a valid post")
        delete_user(token, user_id)
        return

    # 2. Test creating a post with empty image URLs (should fail)
    create_post_with_empty_images(token)

    # 3. Test getting a post by ID
    post = get_post_by_id(token, post_id)

    # 4. Test getting a post with an invalid ID
    get_post_with_invalid_id(token)

    # 5. Test getting all posts by user
    user_posts = get_posts_by_user(token, user_id)

    # 6. Test updating a post's caption
    update_post_caption(token, post_id, "Updated caption from API test")

    # 7. Test liking a post
    like_result = like_post(token, post_id)

    # 8. Test getting like status
    like_status = get_like_status(token, post_id)

    # 9. Test getting users who liked a post
    liked_users = get_post_likes(token, post_id)

    # 10. Test unliking a post
    unlike_result = unlike_post(token, post_id)

    # 11. Test deleting a post
    delete_post(token, post_id)

    # Create a second user to test permissions
    print("\n⚠️ Creating a second user to test permission boundaries...")
    second_user_id, second_username = create_user(token)

    if second_user_id:
        # Create a post with the second user
        second_token = get_auth_token()  # Get a fresh token to simulate second user
        second_post_id = create_post(
            second_token,
            ["https://example.com/second_user_image.jpg"],
            "Post created by second test user"
        )

        if second_post_id:
            # Try to update caption on second user's post (should fail)
            update_caption_on_others_post(token, second_post_id)

            # Try to delete second user's post (should fail)
            delete_others_post(token, second_post_id)

            # Clean up second user's post
            delete_post(second_token, second_post_id)

        # Clean up second user
        delete_user(second_token, second_user_id)

    # Clean up test user
    delete_user(token, user_id)

    print("\n✅ POST API TESTS COMPLETED ✅")
    print("=" * 50)


if __name__ == "__main__":
    run_tests()
