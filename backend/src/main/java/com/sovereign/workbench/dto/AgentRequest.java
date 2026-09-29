package com.sovereign.workbench.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import jakarta.validation.constraints.NotBlank;

public class AgentRequest {

    @NotBlank
    private String question;

    private String context;

    @JsonAlias({"file_path", "filePath"})
    private String filePath;

    @JsonAlias({"web_permission_granted", "webPermissionGranted"})
    private Boolean webPermissionGranted;

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
            String filePath,
            Boolean webPermissionGranted) {
        this.question = question;
        this.context = context;
        this.filePath = filePath;
        this.webPermissionGranted = webPermissionGranted;
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

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public Boolean getWebPermissionGranted() {
        return webPermissionGranted;
    }

    public void setWebPermissionGranted(Boolean webPermissionGranted) {
        this.webPermissionGranted = webPermissionGranted;
    }
}