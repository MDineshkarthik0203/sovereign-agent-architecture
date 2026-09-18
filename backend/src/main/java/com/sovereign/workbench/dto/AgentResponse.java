package com.sovereign.workbench.dto;

public class AgentResponse {

    private boolean success;
    private String route;
    private String currentAgent;
    private String supervisorReason;
    private Object plan;
    private String verification;
    private String finalAnswer;
    private boolean needsWebPermission;
    private boolean webPermissionGranted;

    public AgentResponse() {
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
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

    public boolean isNeedsWebPermission() {
        return needsWebPermission;
    }

    public void setNeedsWebPermission(boolean needsWebPermission) {
        this.needsWebPermission = needsWebPermission;
    }

    public boolean isWebPermissionGranted() {
        return webPermissionGranted;
    }

    public void setWebPermissionGranted(boolean webPermissionGranted) {
        this.webPermissionGranted = webPermissionGranted;
    }
}