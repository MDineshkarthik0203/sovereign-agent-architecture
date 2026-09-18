package com.sovereign.workbench.query;

import jakarta.validation.constraints.NotBlank;

public class QueryRequest {

    @NotBlank
    private String question;

    public QueryRequest() {
    }

    public QueryRequest(String question) {
        this.question = question;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }
}