package com.sovereign.workbench.document;

import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class DocumentProcessorService {

    public Path process(Path filePath) throws IOException {

        String fileName =
                filePath.getFileName().toString();

        String lowerName =
                fileName.toLowerCase();

        String extractedText;

        if (lowerName.endsWith(".txt")
                || lowerName.endsWith(".md")) {

            extractedText =
                    Files.readString(
                            filePath,
                            StandardCharsets.UTF_8
                    );

        } else if (lowerName.endsWith(".pdf")) {

            extractedText =
                    extractPdfText(filePath);

        } else {

            throw new IOException(
                    "Unsupported document format"
            );
        }

        Path processedDirectory =
                filePath.getParent()
                        .resolve("processed");

        Files.createDirectories(
                processedDirectory
        );

        String baseName =
                fileName.substring(
                        0,
                        fileName.lastIndexOf('.')
                );

        Path extractedFile =
                processedDirectory.resolve(
                        baseName + ".txt"
                );

        Files.writeString(
                extractedFile,
                extractedText,
                StandardCharsets.UTF_8
        );

        return extractedFile;
    }

    private String extractPdfText(
            Path filePath) throws IOException {

        try (PDDocument document =
                     Loader.loadPDF(filePath.toFile())) {

            PDFTextStripper stripper =
                    new PDFTextStripper();

            return stripper.getText(document);
        }
    }
}