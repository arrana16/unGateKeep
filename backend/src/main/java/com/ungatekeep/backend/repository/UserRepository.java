package com.ungatekeep.backend.repository;

import com.ungatekeep.backend.classes.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, UUID> {
    // Find a user by their Auth0 ID
    Optional<User> findByAuthID(String authID);

    // Check if username exists (excluding the given ID)
    boolean existsByUsernameAndIdNot(String username, UUID id);

    // Check if username exists for any user
    boolean existsByUsername(String username);
}
