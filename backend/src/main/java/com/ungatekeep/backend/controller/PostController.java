package com.ungatekeep.backend.controller;

import com.ungatekeep.backend.classes.Post;
import com.ungatekeep.backend.classes.User;
import com.ungatekeep.backend.classes.UserLikesPost;
import com.ungatekeep.backend.repository.PostRepository;
import com.ungatekeep.backend.repository.UserLikesPostRepository;
import com.ungatekeep.backend.repository.UserRepository;
import com.ungatekeep.backend.request_helpers.PermissionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/posts")
public class PostController {

    @Autowired
    private PostRepository postRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PermissionService permissionService;

    /**
     * Create a new post
     */
    @PostMapping
    public ResponseEntity<Map<String, String>> createPost(@RequestBody Post post) {
        // Validate required fields
        if (post.getImageUrls() == null || post.getImageUrls().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "At least one image URL is required");
        }

        // Find the current user
        String authId = permissionService.getAuthenticatedUserId();
        User currentUser = userRepository.findByAuthID(authId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User profile not found"));

        // Generate a unique ID for the post
        post.setId(UUID.randomUUID());
        post.setUserId(currentUser.getId());
        post.setCreatedAt(LocalDateTime.now());
        post.setLikes(0);

        // Save the post to the database
        Post savedPost = postRepository.save(post);

        // Return success response with the generated ID
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(Map.of("id", savedPost.getId().toString(), "message", "Post created successfully"));
    }

    /**
     * Get a post by its ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Post> getPostById(@PathVariable String id) {
        UUID postId = UUID.fromString(id);
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Get like count for this post
        long likeCount = userLikesPostRepository.countByPostId(postId);
        post.setLikeCount(likeCount);

        // Check if current user has liked this post
        try {
            String authId = permissionService.getAuthenticatedUserId();
            User currentUser = userRepository.findByAuthID(authId).orElse(null);
            if (currentUser != null) {
                boolean liked = userLikesPostRepository.existsByUserIdAndPostId(currentUser.getId(), postId);
                post.setLikedByCurrentUser(liked);
            }
        } catch (Exception e) {
            // If we can't get the current user, assume not liked
            post.setLikedByCurrentUser(false);
        }

        return ResponseEntity.ok(post);
    }

    /**
     * Get all posts by a specific user
     */
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Post>> getPostsByUserId(@PathVariable String userId) {
        UUID userUUID = UUID.fromString(userId);

        // Verify the user exists
        userRepository.findById(userUUID)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Fetch posts for this user
        List<Post> posts = postRepository.findByUserIdOrderByCreatedAtDesc(userUUID);

        // Get current user for like status
        UUID currentUserId = null;
        try {
            String authId = permissionService.getAuthenticatedUserId();
            User currentUser = userRepository.findByAuthID(authId).orElse(null);
            if (currentUser != null) {
                currentUserId = currentUser.getId();
            }
        } catch (Exception e) {
            // If we can't get the current user, continue without like status
        }

        // Enhance posts with like information
        for (Post post : posts) {
            // Set like count
            long likeCount = userLikesPostRepository.countByPostId(post.getId());
            post.setLikeCount(likeCount);

            // Set if current user has liked this post
            if (currentUserId != null) {
                boolean liked = userLikesPostRepository.existsByUserIdAndPostId(currentUserId, post.getId());
                post.setLikedByCurrentUser(liked);
            } else {
                post.setLikedByCurrentUser(false);
            }
        }

        return ResponseEntity.ok(posts);
    }

    /**
     * Update a post's caption
     */
    @PutMapping("/{id}/caption")
    public ResponseEntity<Map<String, String>> updateCaption(
            @PathVariable String id,
            @RequestBody Map<String, String> payload) {

        // Convert the path variable to UUID
        UUID postId = UUID.fromString(id);

        // Find the existing post
        Post existingPost = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Find the post owner
        User postOwner = userRepository.findById(existingPost.getUserId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post owner not found"));

        // Check if the current user has permission to update this post
        permissionService.assertUserAccess(postOwner.getAuthID());

        // Update caption (can be null)
        existingPost.setCaption(payload.get("caption"));

        // Save the updated post
        postRepository.save(existingPost);

        return ResponseEntity.ok(Map.of("message", "Caption updated successfully"));
    }

    /**
     * Delete a post
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deletePost(@PathVariable String id) {
        // Convert the path variable to UUID
        UUID postId = UUID.fromString(id);

        // Find the existing post
        Post existingPost = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Find the post owner
        User postOwner = userRepository.findById(existingPost.getUserId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post owner not found"));

        // Check if the current user has permission to delete this post
        permissionService.assertUserAccess(postOwner.getAuthID());

        // Delete the post
        postRepository.delete(existingPost);

        return ResponseEntity.ok(Map.of("message", "Post deleted successfully"));
    }

    @Autowired
    private UserLikesPostRepository userLikesPostRepository;

    /**
     * Like or unlike a post
     */
    @PostMapping("/{id}/like")
    public ResponseEntity<Map<String, Object>> likePost(@PathVariable String id) {
        // Convert the path variable to UUID
        UUID postId = UUID.fromString(id);

        // Find the existing post
        Post existingPost = postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Get the current user
        String authId = permissionService.getAuthenticatedUserId();
        User currentUser = userRepository.findByAuthID(authId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User profile not found"));

        // Check if the user has already liked this post
        Optional<UserLikesPost> existingLike = userLikesPostRepository.findByUserIdAndPostId(currentUser.getId(), postId);
        boolean liked;

        if (existingLike.isPresent()) {
            // User has already liked the post, so unlike it
            userLikesPostRepository.delete(existingLike.get());
            liked = false;
        } else {
            // User hasn't liked the post yet, so add a like
            UserLikesPost newLike = new UserLikesPost(currentUser.getId(), postId);
            userLikesPostRepository.save(newLike);
            liked = true;
        }

        // Count the current number of likes
        long likeCount = userLikesPostRepository.countByPostId(postId);

        return ResponseEntity.ok(Map.of(
                "message", liked ? "Post liked successfully" : "Post unliked successfully",
                "likes", likeCount,
                "liked", liked
        ));
    }

    /**
     * Check if the current user has liked a post
     */
    @GetMapping("/{id}/like/status")
    public ResponseEntity<Map<String, Object>> getLikeStatus(@PathVariable String id) {
        // Convert the path variable to UUID
        UUID postId = UUID.fromString(id);

        // Find the existing post
        postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Get the current user
        String authId = permissionService.getAuthenticatedUserId();
        User currentUser = userRepository.findByAuthID(authId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User profile not found"));

        // Check if the user has liked this post
        boolean liked = userLikesPostRepository.existsByUserIdAndPostId(currentUser.getId(), postId);

        // Count the current number of likes
        long likeCount = userLikesPostRepository.countByPostId(postId);

        return ResponseEntity.ok(Map.of(
                "liked", liked,
                "likes", likeCount
        ));
    }

    /**
     * Get users who liked a post
     */
    @GetMapping("/{id}/likes")
    public ResponseEntity<List<User>> getPostLikes(@PathVariable String id) {
        // Convert the path variable to UUID
        UUID postId = UUID.fromString(id);

        // Find the existing post
        postRepository.findById(postId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Post not found"));

        // Get all likes for this post
        List<UserLikesPost> likes = userLikesPostRepository.findByPostId(postId);

        // Get the user details for each like
        List<User> users = likes.stream()
                .map(like -> userRepository.findById(like.getUserId())
                        .orElse(null))
                .filter(user -> user != null)
                .toList();

        return ResponseEntity.ok(users);
    }
}
