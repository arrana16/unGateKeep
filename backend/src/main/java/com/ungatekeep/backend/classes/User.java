package com.ungatekeep.backend.classes;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
public class User {
    @Id
    private UUID id;

    @Column(name = "auth_id")
    private String authID;
    private String username;
    private String bio;

    @Column(name = "avatar_url")
    private String avatar_url;

    private String role;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "username_updated_at")
    private LocalDateTime usernameUpdatedAt;

    @Column(name = "like_emoji")
    private String likeEmoji;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        createdAt = now;
        updatedAt = now;
        usernameUpdatedAt = now;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    /**
     * Updates this User with values from another User object.
     * Only non-null fields from the source user will be used for the update,
     * except for bio and avatar_url which will be updated even if null.
     * 
     * @param sourceUser User object containing updated fields
     * @param isAdmin Whether the current user has admin privileges
     * @return this User object with updated fields
     */
    public void updateFromUser(User sourceUser, boolean isAdmin) {
        // Update username if provided
        if (sourceUser.getUsername() != null) {
            this.username = sourceUser.getUsername();
        }

        // Update bio (can be explicitly set to null)
        this.bio = sourceUser.getBio();

        // Update avatar URL (can be explicitly set to null)
        this.avatar_url = sourceUser.getAvatar_url();

        // Only admins can update roles and only if a role is provided
        if (isAdmin && sourceUser.getRole() != null) {
            this.role = sourceUser.getRole();
        }

        // Update timestamp
        this.updatedAt = LocalDateTime.now();

    }

    public User(UUID id, String authID, String username, String bio, String avatar_url, String role, LocalDateTime createdAt, LocalDateTime updatedAt, LocalDateTime usernameUpdatedAt, String likeEmoji) {
        this.id = id;
        this.authID = authID;
        this.username = username;
        this.bio = bio;
        this.avatar_url = avatar_url;
        this.role = role;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.usernameUpdatedAt = usernameUpdatedAt;
        this.likeEmoji = likeEmoji;
    }

}
