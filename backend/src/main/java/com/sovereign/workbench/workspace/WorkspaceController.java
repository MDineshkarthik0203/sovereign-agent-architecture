package com.sovereign.workbench.workspace;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/workspaces")
@CrossOrigin(origins = "*")
public class WorkspaceController {

    private final WorkspaceService workspaceService;

    public WorkspaceController(WorkspaceService workspaceService) {
        this.workspaceService = workspaceService;
    }

    @PostMapping
    public ResponseEntity<Workspace> createWorkspace(
            @RequestBody Map<String, String> request) {

        String name = request.get("name");

        Workspace workspace =
                workspaceService.createWorkspace(name);

        return ResponseEntity.ok(workspace);
    }

    @GetMapping
    public ResponseEntity<List<Workspace>> getAllWorkspaces() {

        return ResponseEntity.ok(
                workspaceService.getAllWorkspaces()
        );
    }
}