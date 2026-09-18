package com.sovereign.workbench.vector;

import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class VectorStoreService {

    private final Map<String, List<VectorDocument>> workspaceDocuments =
            new HashMap<>();

    private final Map<String, List<String>> workspaceVocabularies =
            new HashMap<>();

    private final VectorService vectorService;

    public VectorStoreService(VectorService vectorService) {
        this.vectorService = vectorService;
    }

    public void store(
            String workspaceId,
            List<VectorDocument> newDocuments) {

        List<String> texts = new ArrayList<>();

        for (VectorDocument document : newDocuments) {
            texts.add(document.getText());
        }

        List<String> vocabulary =
                vectorService.buildVocabulary(texts);

        List<VectorDocument> storedDocuments =
                new ArrayList<>();

        for (VectorDocument document : newDocuments) {

            double[] vector =
                    vectorService.createVector(
                            document.getText(),
                            vocabulary
                    );

            storedDocuments.add(
                    new VectorDocument(
                            document.getChunkIndex(),
                            document.getText(),
                            vector
                    )
            );
        }

        workspaceDocuments.put(
                workspaceId,
                storedDocuments
        );

        workspaceVocabularies.put(
                workspaceId,
                vocabulary
        );
    }

    public List<VectorDocument> getDocuments(
            String workspaceId) {

        return new ArrayList<>(
                workspaceDocuments.getOrDefault(
                        workspaceId,
                        new ArrayList<>()
                )
        );
    }

    public List<String> getVocabulary(
            String workspaceId) {

        return new ArrayList<>(
                workspaceVocabularies.getOrDefault(
                        workspaceId,
                        new ArrayList<>()
                )
        );
    }

    public int size(String workspaceId) {

        return workspaceDocuments
                .getOrDefault(
                        workspaceId,
                        new ArrayList<>()
                )
                .size();
    }
}