package com.ungatekeep.backend.config;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Standard response model for authentication failures
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AuthenticationFailureResponse {
    private String error;
    private String message;

    public AuthenticationFailureResponse(String message) {
        this.error = "Authentication Error";
        this.message = message;
    }
}
