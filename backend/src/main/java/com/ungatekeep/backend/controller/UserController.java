package com.ungatekeep.backend.controller;

import com.ungatekeep.backend.classes.User;
import com.ungatekeep.backend.repository.UserRepository;
import com.ungatekeep.backend.request_helpers.PermissionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PermissionService permissionService;

    @PostMapping("/addUser")
    public ResponseEntity<Map<String, String>> createUser(@RequestBody User user) {
        // Check if username is provided and not taken
        if (user.getUsername() != null && !user.getUsername().trim().isEmpty()) {
            if (userRepository.existsByUsername(user.getUsername())) {
                throw new ResponseStatusException(HttpStatus.CONFLICT, "Username already taken");
            }
        }

        // Generate a unique ID for the user
        user.setId(UUID.randomUUID());

        // Set Auth ID from the authenticated user if not provided
        if (user.getAuthID() == null) {
            user.setAuthID(permissionService.getAuthenticatedUserId());
        }

        // Initialize username update timestamp
        user.setUsernameUpdatedAt(LocalDateTime.now());

        // Save the user to the database
        User savedUser = userRepository.save(user);

        // Return success response with the generated ID
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(Map.of("id", savedUser.getId().toString(), "message", "User created successfully"));
    }

    @PutMapping("/{id}/username")
    public ResponseEntity<Map<String, String>> updateUsername(
            @PathVariable String id, 
            @RequestBody Map<String, String> payload) {

        String newUsername = payload.get("username");
        if (newUsername == null || newUsername.trim().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Username cannot be empty");
        }

        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Check if the current user has permission to update this user
        permissionService.assertUserAccess(existingUser.getAuthID());

        // Check if username already exists for another user
        if (userRepository.existsByUsernameAndIdNot(newUsername, userId)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username already taken");
        }

        // Check if 7 days have passed since last username update
        LocalDateTime lastUpdate = existingUser.getUsernameUpdatedAt();
        if (lastUpdate != null && LocalDateTime.now().minusDays(7).isBefore(lastUpdate)) {
            throw new ResponseStatusException(HttpStatus.TOO_MANY_REQUESTS, 
                "Username can only be updated once every 7 days. Next update available on: " + 
                lastUpdate.plusDays(7));
        }

        // Update username and timestamp
        existingUser.setUsername(newUsername);
        existingUser.setUsernameUpdatedAt(LocalDateTime.now());
        existingUser.setUpdatedAt(LocalDateTime.now());

        // Save the updated user
        userRepository.save(existingUser);

        return ResponseEntity.ok(Map.of("message", "Username updated successfully"));
    }

    @PutMapping("/{id}/bio")
    public ResponseEntity<Map<String, String>> updateBio(
            @PathVariable String id, 
            @RequestBody Map<String, String> payload) {

        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Check if the current user has permission to update this user
        permissionService.assertUserAccess(existingUser.getAuthID());

        // Update bio (can be null)
        existingUser.setBio(payload.get("bio"));
        existingUser.setUpdatedAt(LocalDateTime.now());

        // Save the updated user
        userRepository.save(existingUser);

        return ResponseEntity.ok(Map.of("message", "Bio updated successfully"));
    }

    @PutMapping("/{id}/avatar")
    public ResponseEntity<Map<String, String>> updateAvatar(
            @PathVariable String id, 
            @RequestBody Map<String, String> payload) {

        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Check if the current user has permission to update this user
        permissionService.assertUserAccess(existingUser.getAuthID());

        // Update avatar URL (can be null)
        existingUser.setAvatar_url(payload.get("avatar_url"));
        existingUser.setUpdatedAt(LocalDateTime.now());

        // Save the updated user
        userRepository.save(existingUser);

        return ResponseEntity.ok(Map.of("message", "Avatar updated successfully"));
    }

    @PutMapping("/{id}/like_emoji")
    public ResponseEntity<Map<String, String>> updateLikeEmoji(
            @PathVariable String id,
            @RequestBody Map<String, String> payload) {

        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Check if the current user has permission to update this user
        permissionService.assertUserAccess(existingUser.getAuthID());

        // Update avatar URL (can be null)
        existingUser.setLikeEmoji(payload.get("like_emoji"));
        existingUser.setUpdatedAt(LocalDateTime.now());

        // Save the updated user
        userRepository.save(existingUser);

        return ResponseEntity.ok(Map.of("message", "Like emoji updated successfully"));
    }

    @PutMapping("/{id}/role")
    public ResponseEntity<Map<String, String>> updateRole(
            @PathVariable String id, 
            @RequestBody Map<String, String> payload) {

        String newRole = payload.get("role");
        if (newRole == null || newRole.trim().isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Role cannot be empty");
        }

        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Only admins can update roles
        if (!permissionService.isAdmin()) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Only administrators can update roles");
        }

        // Update role
        existingUser.setRole(newRole);
        existingUser.setUpdatedAt(LocalDateTime.now());

        // Save the updated user
        userRepository.save(existingUser);

        return ResponseEntity.ok(Map.of("message", "Role updated successfully"));
    }

    @GetMapping("/getUser/{id}")
    public ResponseEntity<User> getUserById(@PathVariable String id) {
        UUID userId = UUID.fromString(id);
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        return ResponseEntity.ok(user);
    }

    @GetMapping("/getUser/me")
    public ResponseEntity<User> getCurrentUser() {
        String authId = permissionService.getAuthenticatedUserId();
        User user = userRepository.findByAuthID(authId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User profile not found"));

        return ResponseEntity.ok(user);
    }


    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteUser(@PathVariable String id) {
        // Convert the path variable to UUID
        UUID userId = UUID.fromString(id);

        // Find the existing user
        User existingUser = userRepository.findById(userId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));

        // Check if the current user has permission to delete this user
        permissionService.assertUserAccess(existingUser.getAuthID());

        // TODO: Add Auth0 user deletion logic here
        // This would involve calling Auth0's Management API to delete the user

        // Delete the user from our database
        userRepository.delete(existingUser);

        return ResponseEntity.ok(Map.of("message", "User account deleted successfully"));
    }
}
