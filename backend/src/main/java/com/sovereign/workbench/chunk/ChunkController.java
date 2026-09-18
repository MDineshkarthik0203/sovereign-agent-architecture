package com.sovereign.workbench.chunk;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/chunk")
@CrossOrigin(origins = "*")
public class ChunkController {

    private final ChunkingService chunkingService;

    public ChunkController(ChunkingService chunkingService) {
        this.chunkingService = chunkingService;
    }

    @PostMapping
    public ResponseEntity<List<TextChunk>> createChunks(
            @RequestBody String text) {

        List<TextChunk> chunks =
                chunkingService.chunkText(text);

        return ResponseEntity.ok(chunks);
    }
}
