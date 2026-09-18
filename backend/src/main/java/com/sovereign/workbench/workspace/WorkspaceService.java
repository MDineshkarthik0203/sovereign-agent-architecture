package com.sovereign.workbench.workspace;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import org.springframework.stereotype.Service;

@Service
public class WorkspaceService {

    private final List<Workspace> workspaces = new ArrayList<>();

    public Workspace createWorkspace(String name) {

        String id = UUID.randomUUID().toString();

        Workspace workspace = new Workspace(id, name);

        workspaces.add(workspace);

        return workspace;
    }

    public List<Workspace> getAllWorkspaces() {
        return workspaces;
    }

    public Workspace getWorkspace(String id) {

        return workspaces.stream()
                .filter(workspace -> workspace.getId().equals(id))
                .findFirst()
                .orElse(null);
    }
}