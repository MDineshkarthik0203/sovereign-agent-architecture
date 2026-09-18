import React, { useState } from 'react';
import { Download, FileText, Code2, CheckCircle2, Eye, X, Copy, Check } from 'lucide-react';
import type { DeliverableFile } from '../types/workbench';

interface Props {
  deliverables: DeliverableFile[];
}

export const DeliverableExportPanel: React.FC<Props> = ({ deliverables }) => {
  const [previewFile, setPreviewFile] = useState<DeliverableFile | null>(null);
  const [copied, setCopied] = useState(false);

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

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg p-3.5 flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center space-x-1.5">
          <FileText className="w-3.5 h-3.5 text-sky-400" />
          <span>Industrial Deliverables</span>
        </h3>
        <span className="text-[10px] bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800 flex items-center">
          <CheckCircle2 className="w-3 h-3 mr-1" /> On-Premise Export
        </span>
      </div>

      <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
        {deliverables.length === 0 ? (
          <div className="text-[11px] text-slate-500 py-3 text-center italic">
            No deliverables generated yet. Run an agent or M5 sandbox task.
          </div>
        ) : (
          deliverables.map((file) => (
            <div
              key={file.id}
              className="bg-[#0a0f18] border border-[#1e293b] hover:border-sky-700/80 rounded p-2.5 flex items-center justify-between transition-colors"
            >
              <div 
                onClick={() => setPreviewFile(file)}
                className="flex items-center space-x-2.5 overflow-hidden flex-1 cursor-pointer"
                title="Click to preview deliverable"
              >
                {file.format === 'py' ? (
                  <Code2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : (
                  <FileText className="w-4 h-4 text-sky-400 shrink-0" />
                )}
                <div className="truncate">
                  <div className="text-xs font-medium text-slate-200 truncate hover:text-sky-300">
                    {file.name}
                  </div>
                  <div className="text-[10px] text-slate-500">
                    {file.size} • {file.agentSource}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-1 ml-2 shrink-0">
                <button
                  onClick={() => setPreviewFile(file)}
                  className="bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white p-1.5 rounded transition-colors"
                  title="Preview Content"
                >
                  <Eye className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleDownload(file)}
                  className="bg-slate-800 hover:bg-sky-600 text-slate-300 hover:text-white p-1.5 rounded transition-colors"
                  title="Download Deliverable"
                >
                  <Download className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Deliverable Preview Modal */}
      {previewFile && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#0f1724] border border-[#1e293b] rounded-lg max-w-2xl w-full flex flex-col max-h-[80vh] shadow-2xl overflow-hidden">
            <div className="flex items-center justify-between p-3.5 border-b border-[#1e293b] bg-[#0a0f18]">
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-sky-400" />
                <span className="text-xs font-bold text-slate-100">{previewFile.name}</span>
                <span className="text-[10px] font-mono text-slate-400">({previewFile.size} • {previewFile.agentSource})</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleCopy(previewFile.content)}
                  className="flex items-center space-x-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded transition-colors"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
                <button
                  onClick={() => setPreviewFile(null)}
                  className="text-slate-400 hover:text-white p-1 rounded hover:bg-slate-800"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="p-3.5 overflow-y-auto flex-1 bg-[#05080e]">
              <pre className="font-mono text-xs text-sky-100 whitespace-pre-wrap leading-relaxed select-text">
                {previewFile.content}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
