package com.sovereign.workbench.workspace;

public class FileInfo {

    private String name;
    private String path;
    private long size;
    private String status;
    private String extractedTextPath;

    public FileInfo() {
    }

    public FileInfo(
            String name,
            String path,
            long size,
            String status,
            String extractedTextPath) {

        this.name = name;
        this.path = path;
        this.size = size;
        this.status = status;
        this.extractedTextPath = extractedTextPath;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public long getSize() {
        return size;
    }

    public void setSize(long size) {
        this.size = size;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getExtractedTextPath() {
        return extractedTextPath;
    }

    public void setExtractedTextPath(String extractedTextPath) {
        this.extractedTextPath = extractedTextPath;
    }
}