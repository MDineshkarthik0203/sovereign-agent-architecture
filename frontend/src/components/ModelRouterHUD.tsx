import React from 'react';
import { Bot, Code2, FileSpreadsheet, Calculator, Eye, Sparkles } from 'lucide-react';
import type { AgentRoute } from '../types/workbench';

interface Props {
  currentAgent: string;
  activeRoute: AgentRoute;
  supervisorReason: string;
}

interface AgentCardConfig {
  key: string;
  name: string;
  route: AgentRoute;
  model: string;
  icon: React.ComponentType<{ className?: string }>;
  vram: string;
  taskType: string;
}

const AGENTS_CONFIG: AgentCardConfig[] = [
  {
    key: 'coding_agent',
    name: 'Coding Agent',
    route: 'coding',
    model: 'Qwen-2.5-Coder-7B',
    icon: Code2,
    vram: '5.2 GB',
    taskType: 'Sandbox Code & Scripting'
  },
  {
    key: 'document_agent',
    name: 'Document Agent',
    route: 'document',
    model: 'DeepSeek-R1-14B',
    icon: FileSpreadsheet,
    vram: '9.8 GB',
    taskType: 'PSU Notes & Word Deliverables'
  },
  {
    key: 'calculation_agent',
    name: 'Calculation Agent',
    route: 'calculation',
    model: 'DeepSeek-R1-Distill',
    icon: Calculator,
    vram: '4.8 GB',
    taskType: 'ASME Formulas & Pressure Math'
  },
  {
    key: 'vision_agent',
    name: 'Vision Agent',
    route: 'vision',
    model: 'Qwen2-VL-7B',
    icon: Eye,
    vram: '6.4 GB',
    taskType: 'P&ID Drawings & Scanned OCR'
  },
  {
    key: 'general_agent',
    name: 'General Agent',
    route: 'general',
    model: 'Llama-3.2-3B',
    icon: Bot,
    vram: '2.4 GB',
    taskType: 'Standard Inquiries'
  },
];

export const ModelRouterHUD: React.FC<Props> = ({ currentAgent, activeRoute, supervisorReason }) => {
  return (
    <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg p-3">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-sky-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-200">
            Supervisor Model Auto-Router
          </span>
        </div>
        {supervisorReason && (
          <div className="text-[11px] text-slate-400 truncate max-w-md bg-slate-900/80 px-2.5 py-0.5 rounded border border-slate-800">
            <span className="text-sky-400 font-medium">Supervisor Decision:</span> {supervisorReason}
          </div>
        )}
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-5 gap-2">
        {AGENTS_CONFIG.map((agent) => {
          const isActive = currentAgent === agent.key || activeRoute === agent.route;
          const Icon = agent.icon;

          return (
            <div
              key={agent.key}
              className={`p-2 rounded-md border transition-all duration-300 relative overflow-hidden ${
                isActive
                  ? 'bg-sky-950/80 border-sky-500 shadow-[0_0_12px_rgba(14,165,233,0.3)] ring-1 ring-sky-400'
                  : 'bg-[#0a0f18] border-[#1e293b]/70 opacity-60 hover:opacity-90'
              }`}
            >
              {isActive && (
                <span className="absolute top-1 right-1 flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-sky-500"></span>
                </span>
              )}
              <div className="flex items-center space-x-1.5 mb-1">
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-sky-400' : 'text-slate-400'}`} />
                <span className={`text-[11px] font-bold truncate ${isActive ? 'text-white' : 'text-slate-300'}`}>
                  {agent.name}
                </span>
              </div>
              <div className="text-[10px] text-slate-400 truncate font-mono">{agent.model}</div>
              <div className="text-[9px] text-slate-500 mt-0.5 flex justify-between">
                <span>{agent.taskType}</span>
                <span className="text-slate-400">{agent.vram}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
