package com.sovereign.workbench.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AgentResponse {

    private boolean success;
    private String question;
    private String route;
    private String currentAgent;
    private String supervisorReason;
    private Object plan;
    private String verification;
    private String finalAnswer;

    @JsonAlias({"needs_web_permission", "needsWebPermission"})
    private Boolean needsWebPermission;

    private String source;

    @JsonAlias({"web_results", "webResults"})
    private Object webResults;

    @JsonAlias({"file_path", "filePath"})
    private String filePath;

    public AgentResponse() {
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getRoute() {
        return route;
    }

    public void setRoute(String route) {
        this.route = route;
    }

    public String getCurrentAgent() {
        return currentAgent;
    }

    public void setCurrentAgent(String currentAgent) {
        this.currentAgent = currentAgent;
    }

    public String getSupervisorReason() {
        return supervisorReason;
    }

    public void setSupervisorReason(String supervisorReason) {
        this.supervisorReason = supervisorReason;
    }

    public Object getPlan() {
        return plan;
    }

    public void setPlan(Object plan) {
        this.plan = plan;
    }

    public String getVerification() {
        return verification;
    }

    public void setVerification(String verification) {
        this.verification = verification;
    }

    public String getFinalAnswer() {
        return finalAnswer;
    }

    public void setFinalAnswer(String finalAnswer) {
        this.finalAnswer = finalAnswer;
    }

    public Boolean getNeedsWebPermission() {
        return needsWebPermission;
    }

    public void setNeedsWebPermission(Boolean needsWebPermission) {
        this.needsWebPermission = needsWebPermission;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public Object getWebResults() {
        return webResults;
    }

    public void setWebResults(Object webResults) {
        this.webResults = webResults;
    }

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }
}