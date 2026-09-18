package com.sovereign.workbench.vector;

import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class VectorService {

    public List<String> buildVocabulary(List<String> texts) {

        Set<String> vocabulary = new HashSet<>();

        for (String text : texts) {
            String[] words = tokenize(text);
            Collections.addAll(vocabulary, words);
        }

        List<String> result =
                new ArrayList<>(vocabulary);

        Collections.sort(result);

        return result;
    }

    public double[] createVector(
            String text,
            List<String> vocabulary) {

        String[] words = tokenize(text);

        Map<String, Integer> frequency =
                new HashMap<>();

        for (String word : words) {
            frequency.put(
                    word,
                    frequency.getOrDefault(word, 0) + 1
            );
        }

        double[] vector =
                new double[vocabulary.size()];

        if (words.length == 0) {
            return vector;
        }

        for (int i = 0; i < vocabulary.size(); i++) {

            String word = vocabulary.get(i);

            vector[i] =
                    (double) frequency.getOrDefault(word, 0)
                            / words.length;
        }

        return vector;
    }

    public double cosineSimilarity(
            double[] vectorA,
            double[] vectorB) {

        if (vectorA.length != vectorB.length) {
            throw new IllegalArgumentException(
                    "Vectors must have the same dimension"
            );
        }

        double dotProduct = 0;
        double magnitudeA = 0;
        double magnitudeB = 0;

        for (int i = 0; i < vectorA.length; i++) {

            dotProduct +=
                    vectorA[i] * vectorB[i];

            magnitudeA +=
                    vectorA[i] * vectorA[i];

            magnitudeB +=
                    vectorB[i] * vectorB[i];
        }

        if (magnitudeA == 0 ||
                magnitudeB == 0) {

            return 0;
        }

        return dotProduct /
                (Math.sqrt(magnitudeA) *
                        Math.sqrt(magnitudeB));
    }

    private String[] tokenize(String text) {

        String cleaned =
                text.toLowerCase()
                        .replaceAll("[^a-z0-9 ]", " ")
                        .trim();

        if (cleaned.isEmpty()) {
            return new String[0];
        }

        return cleaned.split("\\s+");
    }
}