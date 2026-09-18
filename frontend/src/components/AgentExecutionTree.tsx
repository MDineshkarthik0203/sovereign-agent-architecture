import React from 'react';
import { 
  CheckCircle2, 
  CircleDashed, 
  Terminal, 
  ShieldCheck, 
  AlertTriangle, 
  Layers, 
  FileCheck,
  ChevronRight
} from 'lucide-react';
import type { AgentExecutionState } from '../types/workbench';

interface Props {
  state: AgentExecutionState | null;
  isRunning: boolean;
}

export const AgentExecutionTree: React.FC<Props> = ({ state, isRunning }) => {
  if (!state && !isRunning) {
    return (
      <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg p-8 flex flex-col items-center justify-center text-center h-full">
        <div className="w-12 h-12 rounded-full bg-slate-900 flex items-center justify-center mb-3 border border-slate-800">
          <Layers className="w-6 h-6 text-slate-500" />
        </div>
        <h4 className="text-sm font-semibold text-slate-300">Agentic Execution Pipeline Idle</h4>
        <p className="text-xs text-slate-500 max-w-sm mt-1">
          Submit an industrial task, inspection prompt, or engineering calculation to watch the sovereign supervisor plan and verify the steps.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg p-4 h-full flex flex-col overflow-hidden">
      <div className="flex items-center justify-between pb-3 border-b border-[#1e293b] mb-3">
        <div className="flex items-center space-x-2">
          <Layers className="w-4 h-4 text-sky-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-200">
            LangGraph Agentic Execution Graph
          </span>
        </div>
        {isRunning && (
          <div className="flex items-center space-x-1.5 text-xs text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-800">
            <CircleDashed className="w-3.5 h-3.5 animate-spin" />
            <span>Agent Iterating in Air-Gapped Sandbox...</span>
          </div>
        )}
        {state && !isRunning && (
          <span className="text-[11px] text-slate-400 font-mono">
            Elapsed: {state.elapsed_seconds ?? '1.4'}s
          </span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
        {/* Node 1: Router / Supervisor Decision */}
        <div className="bg-[#0a0f18] border border-[#1e293b] rounded p-3">
          <div className="flex items-center justify-between mb-1">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="font-semibold text-slate-200">1. Supervisor Router Node</span>
            </div>
            <span className="font-mono text-[10px] bg-sky-950 text-sky-400 px-2 py-0.5 rounded border border-sky-800">
              Route: {state?.route ?? 'analyzing...'}
            </span>
          </div>
          <p className="text-slate-400 text-[11px]">
            {state?.supervisor_reason || 'Analyzing prompt syntax and domain intent...'}
          </p>
        </div>

        {/* Node 2: Planner Agent */}
        <div className="bg-[#0a0f18] border border-[#1e293b] rounded p-3">
          <div className="flex items-center space-x-2 mb-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold text-slate-200">2. Autonomous Planner Node</span>
          </div>
          {state?.plan && state.plan.length > 0 ? (
            <div className="space-y-1 bg-slate-950/60 p-2.5 rounded border border-slate-900 font-mono text-[11px] text-slate-300">
              {state.plan.map((step, idx) => (
                <div key={idx} className="flex items-start space-x-1.5">
                  <ChevronRight className="w-3.5 h-3.5 text-sky-400 mt-0.5 shrink-0" />
                  <span>{step}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-slate-500 text-[11px] italic">Synthesizing execution plan...</div>
          )}
        </div>

        {/* Node 3: Specialized Agent Execution */}
        <div className="bg-[#0a0f18] border border-[#1e293b] rounded p-3">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              {isRunning ? (
                <CircleDashed className="w-4 h-4 text-amber-400 animate-spin" />
              ) : (
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              )}
              <span className="font-semibold text-slate-200">
                3. Active Execution: {state?.current_agent || 'specialized_agent'}
              </span>
            </div>
            <span className="font-mono text-[10px] bg-slate-900 text-slate-300 px-2 py-0.5 rounded border border-slate-700 flex items-center">
              <Terminal className="w-3 h-3 mr-1 text-sky-400" />
              Isolated Sandbox
            </span>
          </div>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-900 font-mono text-[11px] text-slate-300 max-h-48 overflow-y-auto whitespace-pre-wrap">
            {state?.agent_result || 'Executing isolated sandboxed logic...'}
          </div>
        </div>

        {/* Node 4: Formal Verification Node */}
        {state?.verification && (
          <div className={`rounded p-3 border ${
            state.verification_status
              ? 'bg-emerald-950/30 border-emerald-800/80'
              : 'bg-rose-950/30 border-rose-800/80'
          }`}>
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center space-x-2">
                {state.verification_status ? (
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-rose-400" />
                )}
                <span className="font-semibold text-slate-200">4. Sovereign Verification Node</span>
              </div>
              <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                state.verification_status
                  ? 'bg-emerald-900 text-emerald-300 border border-emerald-700'
                  : 'bg-rose-900 text-rose-300 border border-rose-700'
              }`}>
                {state.verification_status ? 'PASSED VERIFICATION' : 'FLAGGED - REPLANNING'}
              </span>
            </div>
            <p className="text-[11px] text-slate-300 font-mono">
              {state.verification}
            </p>
          </div>
        )}

        {/* Node 5: Deliver Agent */}
        {state?.final_answer && (
          <div className="bg-[#0b1424] border border-sky-800/70 rounded p-3">
            <div className="flex items-center space-x-2 mb-2">
              <FileCheck className="w-4 h-4 text-sky-400" />
              <span className="font-semibold text-slate-100">5. Final Verified Deliverable Output</span>
            </div>
            <div className="bg-slate-950 p-3 rounded border border-slate-900 text-[11px] text-slate-200 font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
              {state.final_answer}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
