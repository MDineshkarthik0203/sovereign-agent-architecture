package com.sovereign.workbench.dto;

import jakarta.validation.constraints.NotBlank;

public class AgentRequest {

    @NotBlank
    private String question;

    private String context;
    private Boolean webPermissionGranted = false;
    private Boolean needsWebPermission = false;

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

    public AgentRequest(
            String question,
            String context,
            Boolean webPermissionGranted,
            Boolean needsWebPermission) {

        this.question = question;
        this.context = context;
        this.webPermissionGranted = webPermissionGranted;
        this.needsWebPermission = needsWebPermission;
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

    public Boolean getWebPermissionGranted() {
        return webPermissionGranted;
    }

    public void setWebPermissionGranted(Boolean webPermissionGranted) {
        this.webPermissionGranted = webPermissionGranted;
    }

    public Boolean getNeedsWebPermission() {
        return needsWebPermission;
    }

    public void setNeedsWebPermission(Boolean needsWebPermission) {
        this.needsWebPermission = needsWebPermission;
    }
}