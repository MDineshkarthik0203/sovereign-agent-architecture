package com.sovereign.workbench.vector;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/workspaces/{workspaceId}/search")
@CrossOrigin(origins = "*")
public class SearchController {

    private final RetrievalService retrievalService;

    public SearchController(
            RetrievalService retrievalService) {

        this.retrievalService = retrievalService;
    }

    @GetMapping
    public ResponseEntity<List<RetrievalResult>> search(
            @PathVariable String workspaceId,
            @RequestParam String question,
            @RequestParam(defaultValue = "3") int topK) {

        List<RetrievalResult> results =
                retrievalService.search(
                        workspaceId,
                        question,
                        topK
                );

        return ResponseEntity.ok(results);
    }
}