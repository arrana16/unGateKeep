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
    """Create a new user"""
    print("\n➕ Creating a new user...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Generate a unique username to avoid conflicts
    test_username = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    payload = {
        "username": test_username,
        "bio": "This is a test user created by the API test script",
        "avatar_url": "https://example.com/avatar.png",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/addUser", headers=headers, data=json.dumps(payload))
        print_response(response, "Create User")
        
        if response.status_code == 201:
            user_id = response.json().get("id")
            print(f"✅ User created successfully with ID: {user_id}")
            return user_id, test_username
        else:
            print(f"❌ Failed to create user: {response.text}")
            return None, test_username
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating user: {e}")
        return None, test_username

def update_username(token, user_id, new_username):
    """Update a user's username"""
    print(f"\n✏️ Updating username for user {user_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "username": new_username
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{user_id}/username", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Username")
        
        if response.status_code == 200:
            print("✅ Username updated successfully")
        else:
            print(f"❌ Failed to update username: {response.text}")
        
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating username: {e}")
        return False

def update_bio(token, user_id, new_bio):
    """Update a user's bio"""
    print(f"\n✏️ Updating bio for user {user_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "bio": new_bio
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{user_id}/bio", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Bio")
        
        if response.status_code == 200:
            print("✅ Bio updated successfully")
        else:
            print(f"❌ Failed to update bio: {response.text}")
        
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating bio: {e}")
        return False

def update_avatar(token, user_id, new_avatar_url):
    """Update a user's avatar"""
    print(f"\n✏️ Updating avatar for user {user_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "avatar_url": new_avatar_url
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{user_id}/avatar", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Avatar")
        
        if response.status_code == 200:
            print("✅ Avatar updated successfully")
        else:
            print(f"❌ Failed to update avatar: {response.text}")
        
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating avatar: {e}")
        return False

def update_like_emoji(token, user_id, new_emoji):
    """Update a user's like emoji"""
    print(f"\n✏️ Updating like emoji for user {user_id}...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "like_emoji": new_emoji
    }

    try:
        response = requests.put(f"{BASE_URL}/{user_id}/like_emoji", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Like Emoji")

        if response.status_code == 200:
            print("✅ Like emoji updated successfully")
        else:
            print(f"❌ Failed to update like emoji: {response.text}")

        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating like emoji: {e}")
        return False

def update_role(token, user_id, new_role):
    """Update a user's role (should fail without admin privileges)"""
    print(f"\n✏️ Attempting to update role for user {user_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "role": new_role
    }
    
    try:
        response = requests.put(f"{BASE_URL}/{user_id}/role", headers=headers, data=json.dumps(payload))
        print_response(response, "Update Role")
        
        if response.status_code == 200:
            print("⚠️ WARNING: Role was updated successfully, but this should have failed without admin privileges")
        else:
            print(f"✅ As expected, failed to update role without admin privileges: {response.text}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during role update attempt: {e}")
        return None

def get_user_by_id(token, user_id):
    """Get user by ID"""
    print(f"\n🔍 Getting user with ID: {user_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/getUser/{user_id}", headers=headers)
        print_response(response, "Get User by ID")
        
        if response.status_code == 200:
            print("✅ User retrieved successfully")
        else:
            print(f"❌ Failed to retrieve user: {response.text}")
        
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting user by ID: {e}")
        return None

def get_current_user(token):
    """Get current user based on the auth token"""
    print("\n🔍 Getting current user profile...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/getUser/me", headers=headers)
        print_response(response, "Get Current User")
        
        if response.status_code == 200:
            print("✅ Current user retrieved successfully")
        else:
            print(f"❌ Failed to retrieve current user: {response.text}")
        
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting current user: {e}")
        return None


def delete_user(token, user_id):
    """Delete a user account"""
    print(f"\n❌ Deleting user with ID: {user_id}...")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(f"{BASE_URL}/{user_id}", headers=headers)
        print_response(response, "Delete User")

        if response.status_code == 200:
            print("✅ User deleted successfully")
            # Verify deletion by attempting to get the user
            verification = get_user_by_id(token, user_id)
            if verification is None:
                print("✅ Verified: User no longer exists")
            else:
                print("⚠️ Warning: User still exists after deletion")
        else:
            print(f"❌ Failed to delete user: {response.text}")

        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting user: {e}")
        return False

def run_tests():
    """Run all the API tests in sequence"""
    print("\n🧪 STARTING API TESTS 🧪")
    print("=" * 50)

    # Get authentication token
    token = get_auth_token()

    # Create a user
    user_id, username = create_user(token)

    if user_id:
        # Update the username
        new_username = f"{username}_updated"
        update_username(token, user_id, new_username)

        # Update the bio
        update_bio(token, user_id, "This is an updated bio from the test script")

        # Update the avatar
        update_avatar(token, user_id, "https://example.com/updated_avatar.png")

        # Update the like emoji
        update_like_emoji(token, user_id, "👍")

        # Try to update the role (should fail without admin privileges)
        update_role(token, user_id, "admin")

        # Get the user by ID to verify changes
        get_user_by_id(token, user_id)

        # Get the current user
        get_current_user(token)

        # Finally, delete the user
        delete_user(token, user_id)

    # Get an existing user by ID
    get_user_by_id(token, EXISTING_USER_ID)



    print("\n✅ API TESTS COMPLETED ✅")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()