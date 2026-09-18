export type AgentRoute = 'coding' | 'document' | 'calculation' | 'vision' | 'general';

export interface LocalModelInfo {
  id: string;
  name: string;
  agentKey: string;
  role: string;
  vramUsageGb: number;
  engine: string;
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
  web_permission_granted?: boolean;
  needs_web_permission?: boolean;
  elapsed_seconds?: number;
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
