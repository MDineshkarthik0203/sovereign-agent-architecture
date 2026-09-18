package com.sovereign.workbench.query;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/workspaces/{workspaceId}/query")
@CrossOrigin(origins = "*")
public class QueryController {

    private final QueryService queryService;

    public QueryController(QueryService queryService) {
        this.queryService = queryService;
    }

    @PostMapping
    public ResponseEntity<QueryResponse> processQuery(
            @PathVariable String workspaceId,
            @Valid @RequestBody QueryRequest request) {

        QueryResponse response =
                queryService.processQuery(
                        workspaceId,
                        request.getQuestion()
                );

        return ResponseEntity.ok(response);
    }
}