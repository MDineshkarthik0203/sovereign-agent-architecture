package com.sovereign.workbench.vector;

public class VectorDocument {

    private int chunkIndex;
    private String text;
    private double[] vector;

    public VectorDocument() {
    }

    public VectorDocument(
            int chunkIndex,
            String text,
            double[] vector) {

        this.chunkIndex = chunkIndex;
        this.text = text;
        this.vector = vector;
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

    public double[] getVector() {
        return vector;
    }

    public void setVector(double[] vector) {
        this.vector = vector;
    }
}
