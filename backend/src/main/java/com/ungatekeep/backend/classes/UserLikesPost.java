package com.ungatekeep.backend.classes;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "user_likes_post")
@Getter
@Setter
@NoArgsConstructor
public class UserLikesPost {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user_id")
    private UUID userId;

    @Column(name = "post_id")
    private UUID postId;

    @Column(name = "liked_at")
    private LocalDateTime likedAt;

    @PrePersist
    protected void onCreate() {
        if (likedAt == null) {
            likedAt = LocalDateTime.now();
        }
    }

    public UserLikesPost(UUID userId, UUID postId) {
        this.userId = userId;
        this.postId = postId;
    }
}
