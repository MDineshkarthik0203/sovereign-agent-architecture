package com.sovereign.workbench.service;

import org.springframework.stereotype.Service;

import com.sovereign.workbench.agent.AgentClient;
import com.sovereign.workbench.dto.AgentResponse;

@Service
public class AgentService {

    private final AgentClient agentClient;

    public AgentService(AgentClient agentClient) {
        this.agentClient = agentClient;
    }

    public AgentResponse run(
            String question,
            String context) {

        return agentClient.runAgent(
                question,
                context
        );
    }
}