package com.ungatekeep.backend.request_helpers;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.stereotype.Service;

import java.util.Collection;

@Service
public class PermissionService {

    /**
     * Get the authenticated user's Auth0 ID from the JWT (`sub` claim).
     */
    public String getAuthenticatedUserId() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null) {
            throw new RuntimeException("No authentication found in context");
        }

        Object principal = authentication.getPrincipal();
        if (principal instanceof Jwt jwt) {
            return jwt.getSubject();
        }

        throw new RuntimeException("Unexpected authentication principal type");
    }

    /**
     * Check if the authenticated user has the "admin" role.
     */
    public boolean isAdmin() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null) {
            return false;
        }

        Object principal = authentication.getPrincipal();
        if (principal instanceof Jwt jwt) {
            // Adjust this if your roles are under a different claim.
            // For Auth0, roles often come from `roles` or a custom claim like `https://yourdomain.com/roles`.
            Object rolesClaim = jwt.getClaims().get("roles");
            if (rolesClaim instanceof Collection<?> roles) {
                return roles.contains("admin");
            }
        }

        return false;
    }

    /**
     * Assert that the authenticated user can access a resource.
     * Admins can access any resource. Users can only access their own resource.
     *
     * @param targetUserId the user ID the request is trying to modify
     */
    public void assertUserAccess(String targetUserId) {
        String authenticatedUserId = getAuthenticatedUserId();
        if (!authenticatedUserId.equals(targetUserId) && !isAdmin()) {
            throw new UnauthorizedException("You are not authorized to access this resource");
        }
    }
}
