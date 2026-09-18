import React from 'react';
import { Download, FileText, Code2, CheckCircle2 } from 'lucide-react';
import type { DeliverableFile } from '../types/workbench';

interface Props {
  deliverables: DeliverableFile[];
}

export const DeliverableExportPanel: React.FC<Props> = ({ deliverables }) => {
  const handleDownload = (file: DeliverableFile) => {
    const blob = new Blob([file.content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = file.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg p-3.5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center space-x-1.5">
          <FileText className="w-3.5 h-3.5 text-sky-400" />
          <span>Industrial Deliverables</span>
        </h3>
        <span className="text-[10px] bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800 flex items-center">
          <CheckCircle2 className="w-3 h-3 mr-1" /> On-Premise Export
        </span>
      </div>

      <div className="space-y-2">
        {deliverables.length === 0 ? (
          <div className="text-[11px] text-slate-500 py-3 text-center italic">
            No deliverables generated yet. Run a task to synthesize approval notes or code.
          </div>
        ) : (
          deliverables.map((file) => (
            <div
              key={file.id}
              className="bg-[#0a0f18] border border-[#1e293b] hover:border-sky-700/80 rounded p-2.5 flex items-center justify-between transition-colors"
            >
              <div className="flex items-center space-x-2.5 overflow-hidden">
                {file.format === 'py' ? (
                  <Code2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : (
                  <FileText className="w-4 h-4 text-sky-400 shrink-0" />
                )}
                <div className="truncate">
                  <div className="text-xs font-medium text-slate-200 truncate">{file.name}</div>
                  <div className="text-[10px] text-slate-500">
                    {file.size} • {file.agentSource}
                  </div>
                </div>
              </div>

              <button
                onClick={() => handleDownload(file)}
                className="bg-slate-800 hover:bg-sky-600 text-slate-300 hover:text-white p-1.5 rounded transition-colors ml-2 shrink-0"
                title="Download Deliverable"
              >
                <Download className="w-3.5 h-3.5" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
