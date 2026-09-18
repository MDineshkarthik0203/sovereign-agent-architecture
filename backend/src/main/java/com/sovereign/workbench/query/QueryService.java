package com.sovereign.workbench.query;

import java.util.List;

import org.springframework.stereotype.Service;

import com.sovereign.workbench.service.AgentService;
import com.sovereign.workbench.vector.RetrievalResult;
import com.sovereign.workbench.vector.RetrievalService;
import com.sovereign.workbench.workspace.Workspace;
import com.sovereign.workbench.workspace.WorkspaceService;

@Service
public class QueryService {

    private final WorkspaceService workspaceService;
    private final RetrievalService retrievalService;
    private final AgentService agentService;

    public QueryService(
            WorkspaceService workspaceService,
            RetrievalService retrievalService,
            AgentService agentService) {

        this.workspaceService = workspaceService;
        this.retrievalService = retrievalService;
        this.agentService = agentService;
    }

    public QueryResponse processQuery(
            String workspaceId,
            String question) {

        Workspace workspace =
                workspaceService.getWorkspace(
                        workspaceId
                );

        if (workspace == null) {

            return new QueryResponse(
                    false,
                    workspaceId,
                    question,
                    "Workspace not found",
                    "JAVA_BACKEND",
                    List.of()
            );
        }

        List<RetrievalResult> retrievedChunks =
                retrievalService.search(
                        workspaceId,
                        question,
                        3
                );

        if (retrievedChunks.isEmpty()) {

            return new QueryResponse(
                    true,
                    workspaceId,
                    question,
                    "No relevant information was found " +
                    "in the workspace documents.",
                    "JAVA_RAG",
                    retrievedChunks
            );
        }

        StringBuilder contextBuilder =
                new StringBuilder();

        for (RetrievalResult result : retrievedChunks) {

            contextBuilder
                    .append("Chunk ")
                    .append(result.getChunkIndex())
                    .append(":\n")
                    .append(result.getText())
                    .append("\n\n");
        }

        String context =
                contextBuilder.toString();

        try {

            var agentResponse =
                    agentService.run(
                            question,
                            context
                    );

            String finalAnswer =
                    agentResponse.getFinalAnswer();

            if (finalAnswer == null ||
                    finalAnswer.isBlank()) {

                finalAnswer =
                        "The agent did not return a final answer.";
            }

            return new QueryResponse(
                    true,
                    workspaceId,
                    question,
                    finalAnswer,
                    "JAVA_RAG_AGENT",
                    retrievedChunks
            );

        } catch (Exception e) {

            return new QueryResponse(
                    true,
                    workspaceId,
                    question,
                    "Relevant information was retrieved, " +
                    "but the agent service is currently unavailable.",
                    "JAVA_RAG",
                    retrievedChunks
            );
        }
    }
}