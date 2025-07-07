package com.ungatekeep.backend.repository;

import com.ungatekeep.backend.classes.Post;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface PostRepository extends JpaRepository<Post, UUID> {
    // Find all posts by a specific user
    List<Post> findByUserIdOrderByCreatedAtDesc(UUID userId);

    // Count posts by a specific user
    long countByUserId(UUID userId);
}
