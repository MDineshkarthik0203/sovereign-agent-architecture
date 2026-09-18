package com.sovereign.workbench.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.sovereign.workbench.dto.AgentRequest;
import com.sovereign.workbench.dto.AgentResponse;
import com.sovereign.workbench.service.AgentService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/agent")
@CrossOrigin(origins = "*")
public class AgentController {

    private final AgentService agentService;

    public AgentController(AgentService agentService) {
        this.agentService = agentService;
    }

    @PostMapping("/run")
    public ResponseEntity<AgentResponse> runAgent(
            @Valid @RequestBody AgentRequest request) {

        AgentResponse response =
                agentService.run(
                        request.getQuestion(),
                        request.getContext()
                );

        return ResponseEntity.ok(response);
    }
}