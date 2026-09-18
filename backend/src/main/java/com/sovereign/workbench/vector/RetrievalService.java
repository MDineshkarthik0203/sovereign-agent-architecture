package com.sovereign.workbench.vector;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import org.springframework.stereotype.Service;

@Service
public class RetrievalService {

    private final VectorService vectorService;
    private final VectorStoreService vectorStoreService;

    public RetrievalService(
            VectorService vectorService,
            VectorStoreService vectorStoreService) {

        this.vectorService = vectorService;
        this.vectorStoreService = vectorStoreService;
    }

    public List<RetrievalResult> search(
            String workspaceId,
            String question,
            int topK) {

        List<VectorDocument> documents =
                vectorStoreService.getDocuments(
                        workspaceId
                );

        List<String> vocabulary =
                vectorStoreService.getVocabulary(
                        workspaceId
                );

        List<RetrievalResult> results =
                new ArrayList<>();

        if (documents.isEmpty() ||
                vocabulary.isEmpty()) {

            return results;
        }

        double[] questionVector =
                vectorService.createVector(
                        question,
                        vocabulary
                );

        for (VectorDocument document : documents) {

            double similarity =
                    vectorService.cosineSimilarity(
                            questionVector,
                            document.getVector()
                    );

            results.add(
                    new RetrievalResult(
                            document.getChunkIndex(),
                            document.getText(),
                            similarity
                    )
            );
        }

        results.sort(
                Comparator.comparingDouble(
                        RetrievalResult::getSimilarity
                ).reversed()
        );

        int resultCount =
                Math.min(topK, results.size());

        return new ArrayList<>(
                results.subList(0, resultCount)
        );
    }
}