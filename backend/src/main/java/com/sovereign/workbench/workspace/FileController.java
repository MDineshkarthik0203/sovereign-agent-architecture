package com.sovereign.workbench.workspace;

import com.sovereign.workbench.chunk.ChunkingService;
import com.sovereign.workbench.chunk.TextChunk;
import com.sovereign.workbench.document.DocumentProcessorService;
import com.sovereign.workbench.vector.VectorDocument;
import com.sovereign.workbench.vector.VectorStoreService;

import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/workspaces/{workspaceId}/files")
@CrossOrigin(origins = "*")
public class FileController {

    private final WorkspaceService workspaceService;
    private final DocumentProcessorService documentProcessorService;
    private final ChunkingService chunkingService;
    private final VectorStoreService vectorStoreService;

    private final Path uploadDirectory =
            Paths.get("uploads")
                    .toAbsolutePath()
                    .normalize();

    public FileController(
            WorkspaceService workspaceService,
            DocumentProcessorService documentProcessorService,
            ChunkingService chunkingService,
            VectorStoreService vectorStoreService) {

        this.workspaceService = workspaceService;
        this.documentProcessorService =
                documentProcessorService;
        this.chunkingService =
                chunkingService;
        this.vectorStoreService =
                vectorStoreService;
    }

    @PostMapping
    public ResponseEntity<?> uploadFile(
            @PathVariable String workspaceId,
            @RequestParam("file") MultipartFile file) {

        Workspace workspace =
                workspaceService.getWorkspace(workspaceId);

        if (workspace == null) {
            return ResponseEntity.notFound().build();
        }

        if (file.isEmpty()) {
            return ResponseEntity.badRequest()
                    .body("File cannot be empty");
        }

        try {
            Path workspaceDirectory =
                    uploadDirectory
                            .resolve(workspaceId)
                            .normalize();

            Files.createDirectories(workspaceDirectory);

            String fileName =
                    Paths.get(
                            file.getOriginalFilename()
                    )
                    .getFileName()
                    .toString();

            Path filePath =
                    workspaceDirectory
                            .resolve(fileName)
                            .normalize();

            if (!filePath.startsWith(
                    workspaceDirectory)) {

                return ResponseEntity.badRequest()
                        .body("Invalid file name");
            }

            file.transferTo(filePath);

            String status;
            String extractedTextPath = null;

            try {

                Path extractedFile =
                        documentProcessorService
                                .process(filePath);

                extractedTextPath =
                        extractedFile.toString();

                String extractedText =
                        Files.readString(
                                extractedFile,
                                StandardCharsets.UTF_8
                        );

                List<TextChunk> chunks =
                        chunkingService
                                .chunkText(extractedText);

                List<VectorDocument> vectorDocuments =
                        new ArrayList<>();

                for (TextChunk chunk : chunks) {

                    vectorDocuments.add(
                            new VectorDocument(
                                    chunk.getChunkIndex(),
                                    chunk.getText(),
                                    null
                            )
                    );
                }

                vectorStoreService.store(
                        workspaceId,
                        vectorDocuments
                );

                status = "READY";

            } catch (IOException processingError) {

                status = "PROCESSING_FAILED";
            }

            FileInfo fileInfo =
                    new FileInfo(
                            fileName,
                            filePath.toString(),
                            file.getSize(),
                            status,
                            extractedTextPath
                    );

            return ResponseEntity.ok(fileInfo);

        } catch (IOException e) {

            return ResponseEntity
                    .internalServerError()
                    .body("Failed to upload file");
        }
    }

    @GetMapping
    public ResponseEntity<?> getFiles(
            @PathVariable String workspaceId) {

        Workspace workspace =
                workspaceService.getWorkspace(
                        workspaceId
                );

        if (workspace == null) {
            return ResponseEntity.notFound()
                    .build();
        }

        Path workspaceDirectory =
                uploadDirectory
                        .resolve(workspaceId)
                        .normalize();

        if (!Files.exists(workspaceDirectory)) {
            return ResponseEntity.ok(
                    new ArrayList<>()
            );
        }

        try {

            List<FileInfo> files =
                    new ArrayList<>();

            try (var paths =
                         Files.list(
                                 workspaceDirectory
                         )) {

                paths.forEach(path -> {

                    try {

                        if (!Files.isRegularFile(path)) {
                            return;
                        }

                        String fileName =
                                path.getFileName()
                                        .toString();

                        Path processedFile =
                                workspaceDirectory
                                        .resolve("processed")
                                        .resolve(
                                                getBaseName(
                                                        fileName
                                                ) + ".txt"
                                        );

                        String status =
                                Files.exists(
                                        processedFile
                                )
                                        ? "READY"
                                        : "NOT_PROCESSED";

                        String extractedPath =
                                Files.exists(
                                        processedFile
                                )
                                        ? processedFile.toString()
                                        : null;

                        files.add(
                                new FileInfo(
                                        fileName,
                                        path.toString(),
                                        Files.size(path),
                                        status,
                                        extractedPath
                                )
                        );

                    } catch (IOException ignored) {
                    }
                });
            }

            return ResponseEntity.ok(files);

        } catch (IOException e) {

            return ResponseEntity
                    .internalServerError()
                    .body("Failed to read files");
        }
    }

    @GetMapping("/{fileName}")
    public ResponseEntity<?> downloadFile(
            @PathVariable String workspaceId,
            @PathVariable String fileName) {

        Workspace workspace =
                workspaceService.getWorkspace(
                        workspaceId
                );

        if (workspace == null) {
            return ResponseEntity.notFound()
                    .build();
        }

        try {

            Path workspaceDirectory =
                    uploadDirectory
                            .resolve(workspaceId)
                            .normalize();

            Path filePath =
                    workspaceDirectory
                            .resolve(fileName)
                            .normalize();

            if (!filePath.startsWith(
                    workspaceDirectory)) {

                return ResponseEntity.badRequest()
                        .body("Invalid file name");
            }

            if (!Files.exists(filePath)
                    || !Files.isRegularFile(filePath)) {

                return ResponseEntity.notFound()
                        .build();
            }

            Resource resource =
                    new UrlResource(
                            filePath.toUri()
                    );

            String contentType =
                    Files.probeContentType(
                            filePath
                    );

            if (contentType == null) {
                contentType =
                        "application/octet-stream";
            }

            return ResponseEntity.ok()
                    .header(
                            HttpHeaders.CONTENT_DISPOSITION,
                            "attachment; filename=\"" +
                                    filePath.getFileName() +
                                    "\""
                    )
                    .header(
                            HttpHeaders.CONTENT_TYPE,
                            contentType
                    )
                    .body(resource);

        } catch (Exception e) {

            return ResponseEntity
                    .internalServerError()
                    .body(
                            "Failed to download file"
                    );
        }
    }

    private String getBaseName(String fileName) {

        int dotIndex =
                fileName.lastIndexOf('.');

        if (dotIndex == -1) {
            return fileName;
        }

        return fileName.substring(
                0,
                dotIndex
        );
    }
}