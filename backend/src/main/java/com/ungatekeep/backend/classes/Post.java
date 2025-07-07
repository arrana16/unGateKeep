package com.ungatekeep.backend.classes;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "posts")
@Getter
@Setter
@NoArgsConstructor
public class Post {
    @Id
    private UUID id;

    @Column(name = "user_id")
    private UUID userId;

    /**
     * Stores image URLs as a comma-separated string in the database
     * but exposes them as a List<String> in the API
     */
    @Column(name = "image_url")
    private String imageUrl;

    // Transient field for handling the list of image URLs
    @Transient
    private List<String> imageUrls = new ArrayList<>();

    private String caption;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // This field is kept for backward compatibility but won't be used anymore
    // Likes are now tracked in the user_likes_post table
    private Integer likes;

    // Transient field for returning the like count in API responses
    @Transient
    private Long likeCount = 0L;

    // Transient field to indicate if current user has liked this post
    @Transient
    private Boolean likedByCurrentUser = false;

    @PrePersist
    protected void onCreate() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
        if (likes == null) {
            likes = 0;
        }
        // Convert the list to a comma-separated string before saving
        if (imageUrls != null && !imageUrls.isEmpty()) {
            this.imageUrl = String.join(",", imageUrls);
        }
    }

    @PostLoad
    protected void onLoad() {
        // Convert the comma-separated string to a list after loading
        if (imageUrl != null && !imageUrl.isEmpty()) {
            this.imageUrls = List.of(imageUrl.split(","));
        } else {
            this.imageUrls = new ArrayList<>();
        }
    }

    public void setImageUrls(List<String> imageUrls) {
        this.imageUrls = imageUrls;
        // Update the database field whenever the list is set
        if (imageUrls != null && !imageUrls.isEmpty()) {
            this.imageUrl = String.join(",", imageUrls);
        } else {
            this.imageUrl = "";
        }
    }

    public List<String> getImageUrls() {
        // Ensure we always return the parsed list
        if (this.imageUrls == null || this.imageUrls.isEmpty()) {
            onLoad(); // Parse from the database string if needed
        }
        return this.imageUrls;
    }

    public Post(UUID id, UUID userId, List<String> imageUrls, String caption) {
        this.id = id;
        this.userId = userId;
        this.setImageUrls(imageUrls);
        this.caption = caption;
        this.likes = 0;
    }

    public Post(UUID id, UUID userId, List<String> imageUrls, String caption, LocalDateTime createdAt, Integer likes) {
        this.id = id;
        this.userId = userId;
        this.setImageUrls(imageUrls);
        this.caption = caption;
        this.createdAt = createdAt;
        this.likes = likes;
    }
}
