import React, { useState } from 'react';
import { 
  CheckCircle2, 
  CircleDashed, 
  Terminal, 
  ShieldCheck, 
  AlertTriangle, 
  Layers, 
  FileCheck,
  ChevronRight,
  BookOpen,
  FileText,
  History,
  Workflow
} from 'lucide-react';
import type { AgentExecutionState } from '../types/workbench';

interface Props {
  state: AgentExecutionState | null;
  isRunning: boolean;
}

export const AgentExecutionTree: React.FC<Props> = ({ state, isRunning }) => {
  const [viewMode, setViewMode] = useState<'pipeline' | 'audit'>('pipeline');

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
      {/* Header with View Toggle */}
      <div className="flex items-center justify-between pb-3 border-b border-[#1e293b] mb-3">
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 bg-[#090d14] p-0.5 rounded border border-[#1e293b]">
            <button
              onClick={() => setViewMode('pipeline')}
              className={`flex items-center space-x-1 px-2.5 py-0.5 rounded text-xs font-semibold transition-all ${
                viewMode === 'pipeline'
                  ? 'bg-sky-600 text-white'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Workflow className="w-3 h-3" />
              <span>Pipeline Graph</span>
            </button>
            <button
              onClick={() => setViewMode('audit')}
              className={`flex items-center space-x-1 px-2.5 py-0.5 rounded text-xs font-semibold transition-all ${
                viewMode === 'audit'
                  ? 'bg-sky-600 text-white'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <History className="w-3 h-3" />
              <span>Execution Audit ({state?.execution_history?.length ?? 0})</span>
            </button>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {isRunning && (
            <div className="flex items-center space-x-1.5 text-xs text-amber-400 bg-amber-950/40 px-2 py-0.5 rounded border border-amber-800">
              <CircleDashed className="w-3.5 h-3.5 animate-spin" />
              <span>LangGraph Nodes Executing...</span>
            </div>
          )}
          {state && !isRunning && (
            <span className="text-[11px] text-slate-400 font-mono">
              Elapsed: {state.elapsed_seconds ?? '1.2'}s
            </span>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
        {viewMode === 'audit' ? (
          /* Execution History Audit Trail */
          <div className="space-y-2">
            <div className="text-[11px] text-slate-400 font-mono mb-2">
              Chronological LangGraph Execution Trace:
            </div>
            {state?.execution_history && state.execution_history.length > 0 ? (
              state.execution_history.map((step, idx) => (
                <div
                  key={idx}
                  className="bg-[#0a0f18] border border-[#1e293b] rounded p-2.5 flex items-start space-x-2.5 font-mono"
                >
                  <span className="w-5 h-5 rounded bg-sky-950 border border-sky-800 text-sky-400 flex items-center justify-center text-[10px] shrink-0 font-bold">
                    {idx + 1}
                  </span>
                  <div className="text-slate-200 text-[11px] leading-relaxed">
                    {step}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-slate-500 italic py-4 text-center">
                No execution history records found.
              </div>
            )}
          </div>
        ) : (
          /* Pipeline Graph Mode */
          <>
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

            {/* Node 2: Autonomous Planner Agent */}
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

            {/* Node 3: Specialist Agent Execution */}
            <div className="bg-[#0a0f18] border border-[#1e293b] rounded p-3">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  {isRunning ? (
                    <CircleDashed className="w-4 h-4 text-amber-400 animate-spin" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  )}
                  <span className="font-semibold text-slate-200">
                    3. Specialist Agent: {state?.current_agent || 'specialized_agent'}
                  </span>
                </div>
                <span className="font-mono text-[10px] bg-slate-900 text-slate-300 px-2 py-0.5 rounded border border-slate-700 flex items-center">
                  <Terminal className="w-3 h-3 mr-1 text-sky-400" />
                  LangGraph Specialist
                </span>
              </div>
              <div className="bg-slate-950 p-2.5 rounded border border-slate-900 font-mono text-[11px] text-slate-300 max-h-48 overflow-y-auto whitespace-pre-wrap">
                {state?.agent_result || 'Executing specialist agent logic...'}
              </div>
            </div>

            {/* Node 4: Tool Policy & Executor Node (if tool results exist) */}
            {state?.tool_results && state.tool_results.length > 0 && (
              <div className="bg-[#0a0f18] border border-[#1e293b] rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span className="font-semibold text-slate-200">
                      4. Tool Policy & Sandbox Executor
                    </span>
                  </div>
                  <span className="font-mono text-[10px] bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800">
                    M5 Tool Dispatcher
                  </span>
                </div>
                <div className="space-y-1.5 font-mono text-[11px]">
                  {state.tool_results.map((tr, idx) => (
                    <div key={idx} className="bg-slate-950 p-2 rounded border border-slate-900 text-slate-300 whitespace-pre-wrap">
                      {tr}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Node 5: Document Processor (if document_content read from sandbox) */}
            {state?.document_content && (
              <div className="bg-[#0a0f18] border border-sky-900/60 rounded p-3">
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-sky-400" />
                    <span className="font-semibold text-slate-200">
                      Document Processor Node
                    </span>
                  </div>
                  <span className="font-mono text-[10px] text-sky-300 bg-sky-950 px-2 py-0.5 rounded border border-sky-800">
                    File Ingestion Active
                  </span>
                </div>
                <div className="bg-slate-950 p-2.5 rounded border border-slate-900 font-mono text-[11px] text-sky-100 whitespace-pre-wrap">
                  {state.document_content}
                </div>
              </div>
            )}

            {/* Node 6: RAG Evidence Grounding (if rag_evidence exists) */}
            {state?.rag_evidence && state.rag_evidence.length > 0 && (
              <div className="bg-[#0a0f18] border border-amber-900/60 rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <BookOpen className="w-4 h-4 text-amber-400" />
                    <span className="font-semibold text-slate-200">
                      RAG Retrieved Evidence Grounding
                    </span>
                  </div>
                  <span className="font-mono text-[10px] text-amber-300 bg-amber-950 px-2 py-0.5 rounded border border-amber-800">
                    ChromaDB Vector Retrieval
                  </span>
                </div>
                <div className="space-y-1.5 font-mono text-[11px]">
                  {state.rag_evidence.map((ev, idx) => (
                    <div key={idx} className="bg-slate-950 p-2 rounded border border-slate-900 text-slate-300">
                      <div className="text-[10px] text-amber-400 font-semibold mb-0.5">
                        Source: {ev.source ?? 'sample.pdf'} {ev.page ? `(Page ${ev.page})` : ''}
                      </div>
                      <div className="text-slate-200">{ev.text ?? ev.content ?? JSON.stringify(ev)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Node 7: Formal Verification Node */}
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
                    <span className="font-semibold text-slate-200">Verification Agent Node</span>
                  </div>
                  <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                    state.verification_status
                      ? 'bg-emerald-900 text-emerald-300 border border-emerald-700'
                      : 'bg-rose-900 text-rose-300 border border-rose-700'
                  }`}>
                    {state.verification_status ? 'PASSED VERIFICATION' : 'FLAGGED - REPLANNING'}
                  </span>
                </div>
                <p className="text-[11px] text-slate-300 font-mono whitespace-pre-wrap">
                  {state.verification}
                </p>
              </div>
            )}

            {/* Node 8: Deliver Agent */}
            {state?.final_answer && (
              <div className="bg-[#0b1424] border border-sky-800/70 rounded p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <FileCheck className="w-4 h-4 text-sky-400" />
                  <span className="font-semibold text-slate-100">Deliver Agent Final Output</span>
                </div>
                <div className="bg-slate-950 p-3 rounded border border-slate-900 text-[11px] text-slate-200 font-mono whitespace-pre-wrap max-h-60 overflow-y-auto">
                  {state.final_answer}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
