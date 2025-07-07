package com.ungatekeep.backend.repository;

import com.ungatekeep.backend.classes.UserLikesPost;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserLikesPostRepository extends JpaRepository<UserLikesPost, Long> {
    // Find a like by user ID and post ID
    Optional<UserLikesPost> findByUserIdAndPostId(UUID userId, UUID postId);

    // Check if a user has liked a post
    boolean existsByUserIdAndPostId(UUID userId, UUID postId);

    // Delete a like by user ID and post ID
    void deleteByUserIdAndPostId(UUID userId, UUID postId);

    // Count likes for a post
    long countByPostId(UUID postId);

    // Find all users who liked a post
    List<UserLikesPost> findByPostId(UUID postId);

    // Find all posts liked by a user
    List<UserLikesPost> findByUserId(UUID userId);

    // Get a count of likes for each post
    @Query("SELECT ulp.postId, COUNT(ulp) FROM UserLikesPost ulp GROUP BY ulp.postId")
    List<Object[]> countLikesPerPost();
}
