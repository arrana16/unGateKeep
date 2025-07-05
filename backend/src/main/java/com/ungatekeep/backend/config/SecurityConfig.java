package com.ungatekeep.backend.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.oauth2.server.resource.web.BearerTokenAuthenticationEntryPoint;
import org.springframework.security.oauth2.server.resource.web.access.BearerTokenAccessDeniedHandler;
import org.springframework.security.web.SecurityFilterChain;

import java.util.HashMap;
import java.util.Map;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(authz -> authz
                        .requestMatchers("/public/**").permitAll()
                        .anyRequest().authenticated()
                )
                .oauth2ResourceServer(oauth2 -> oauth2
                        .jwt()
                        .and()
                        .authenticationEntryPoint((request, response, authException) -> {
                            // Set response status and content type
                            response.setStatus(HttpStatus.UNAUTHORIZED.value());
                            response.setContentType(MediaType.APPLICATION_JSON_VALUE);

                            // Create error response using our model class
                            AuthenticationFailureResponse errorResponse = new AuthenticationFailureResponse(
                                "Authentication failed. Please provide a valid authentication token."
                            );

                            // Write error response
                            ObjectMapper mapper = new ObjectMapper();
                            mapper.writeValue(response.getWriter(), errorResponse);
                        })
                        .accessDeniedHandler((request, response, accessDeniedException) -> {
                            // Set response status and content type
                            response.setStatus(HttpStatus.FORBIDDEN.value());
                            response.setContentType(MediaType.APPLICATION_JSON_VALUE);

                            // Create error response using our model class
                            AuthenticationFailureResponse errorResponse = new AuthenticationFailureResponse(
                                "Access denied. You don't have permission to access this resource."
                            );

                            // Write error response
                            ObjectMapper mapper = new ObjectMapper();
                            mapper.writeValue(response.getWriter(), errorResponse);
                        })
                );
        return http.build();
    }
}
