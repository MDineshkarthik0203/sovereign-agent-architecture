package com.sovereign.workbench.agent;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import com.sovereign.workbench.dto.AgentRequest;
import com.sovereign.workbench.dto.AgentResponse;

@Component
public class AgentClient {

    private final RestClient restClient;

    public AgentClient(
            RestClient.Builder builder,
            @Value("${agent.base-url:http://localhost:8000}") String agentBaseUrl) {

        this.restClient = builder
                .baseUrl(agentBaseUrl)
                .build();
    }

    public AgentResponse runAgent(
            String question,
            String context,
            Boolean webPermissionGranted,
            Boolean needsWebPermission) {

        AgentRequest request =
                new AgentRequest(
                        question,
                        context,
                        webPermissionGranted,
                        needsWebPermission
                );

        return restClient.post()
                .uri("/agent/run")
                .body(request)
                .retrieve()
                .body(AgentResponse.class);
    }
}