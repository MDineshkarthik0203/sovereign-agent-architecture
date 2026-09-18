package com.sovereign.workbench.dto;

import jakarta.validation.constraints.NotBlank;

public class AgentRequest {

    @NotBlank
    private String question;

    private String context;

    public AgentRequest() {
    }

    public AgentRequest(String question) {
        this.question = question;
    }

    public AgentRequest(
            String question,
            String context) {

        this.question = question;
        this.context = context;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getContext() {
        return context;
    }

    public void setContext(String context) {
        this.context = context;
    }
}