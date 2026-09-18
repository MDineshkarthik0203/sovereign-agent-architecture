package com.sovereign.workbench.query;

import java.util.List;

import com.sovereign.workbench.vector.RetrievalResult;

public class QueryResponse {

    private boolean success;
    private String workspaceId;
    private String question;
    private String answer;
    private String source;
    private List<RetrievalResult> retrievedChunks;

    public QueryResponse() {
    }

    public QueryResponse(
            boolean success,
            String workspaceId,
            String question,
            String answer,
            String source) {

        this(
                success,
                workspaceId,
                question,
                answer,
                source,
                List.of()
        );
    }

    public QueryResponse(
            boolean success,
            String workspaceId,
            String question,
            String answer,
            String source,
            List<RetrievalResult> retrievedChunks) {

        this.success = success;
        this.workspaceId = workspaceId;
        this.question = question;
        this.answer = answer;
        this.source = source;
        this.retrievedChunks = retrievedChunks;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public String getWorkspaceId() {
        return workspaceId;
    }

    public void setWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public List<RetrievalResult> getRetrievedChunks() {
        return retrievedChunks;
    }

    public void setRetrievedChunks(
            List<RetrievalResult> retrievedChunks) {

        this.retrievedChunks = retrievedChunks;
    }
}