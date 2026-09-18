package com.sovereign.workbench.chunk;

public class TextChunk {

    private int chunkIndex;
    private String text;

    public TextChunk() {
    }

    public TextChunk(int chunkIndex, String text) {
        this.chunkIndex = chunkIndex;
        this.text = text;
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
}