package com.sovereign.workbench.vector;

public class RetrievalResult {

    private int chunkIndex;
    private String text;
    private double similarity;

    public RetrievalResult() {
    }

    public RetrievalResult(
            int chunkIndex,
            String text,
            double similarity) {

        this.chunkIndex = chunkIndex;
        this.text = text;
        this.similarity = similarity;
    }

    public int getChunkIndex() {
        return chunkIndex;
    }

    public void setChunkIndex(int chunkIndex) {
        this.chunkIndex = chunkIndex;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public double getSimilarity() {
        return similarity;
    }

    public void setSimilarity(double similarity) {
        this.similarity = similarity;
    }
}