export type AgentRoute = 'coding' | 'document' | 'calculation' | 'vision' | 'general';

export interface LocalModelInfo {
  id: string;
  name: string;
  agentKey: string;
  role: string;
  vramUsageGb: number;
  engine: string;
}

export interface RagEvidenceItem {
  text?: string;
  content?: string;
  source?: string;
  page?: number | string;
  score?: number;
}

export interface AgentExecutionState {
  question: string;
  route: AgentRoute;
  supervisor_reason: string;
  plan: string[];
  current_agent: string;
  agent_result: string;
  tool_results: string[];
  observations: string[];
  verification: string;
  verification_status: boolean;
  retry_count: number;
  final_answer: string;
  elapsed_seconds?: number;
  execution_history?: string[];
  document_content?: string;
  rag_query?: string;
  rag_evidence?: RagEvidenceItem[];
}

export interface SystemStatus {
  is_air_gapped: boolean;
  outbound_wan_kb_s: number;
  loopback_active: boolean;
  gpu_name: string;
  vram_used_gb: number;
  vram_total_gb: number;
  gpu_temp_c: number;
}

export interface DeliverableFile {
  id: string;
  name: string;
  format: 'docx' | 'py' | 'xlsx' | 'txt';
  size: string;
  agentSource: string;
  content: string;
}

export interface SandboxTool {
  name: string;
  description: string;
  requiredArgs: string[];
  optionalArgs?: string[];
}

export interface SandboxExecutionResult {
  status: 'success' | 'failed' | 'timeout' | 'blocked';
  stdout?: string;
  stderr?: string;
  exit_code?: number;
  execution_time?: number;
  error?: string;
  artifact_name?: string;
}

export interface SandboxState {
  workspaceActive: boolean;
  isolationMode: 'tempfs' | 'process_isolation';
  timeoutSeconds: number;
  zeroEgressPolicy: boolean;
  registeredTools: string[];
  recentExecutions: SandboxExecutionResult[];
}

export interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  mode?: string;
  engine?: string;
  latencySec?: number | string;
  sources?: { document: string; page?: number | string }[];
  timestamp?: string;
}

export interface PipelineStep {
  stepNumber: number;
  title: string;
  detail?: string;
  status: 'pending' | 'active' | 'completed';
}

export type DocAnalysisMode = 'fast' | 'vlm';

export interface DocAnalysisResult {
  latency: string;
  confidence: string;
  fields: Record<string, any>;
  ocrText?: string;
  imagePreview?: string;
}
