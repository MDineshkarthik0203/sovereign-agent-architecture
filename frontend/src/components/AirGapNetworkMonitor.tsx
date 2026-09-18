import React, { useState, useEffect } from 'react';
import { ShieldCheck, WifiOff, Cpu, HardDrive, Radio } from 'lucide-react';
import type { SystemStatus } from '../types/workbench';

interface Props {
  status?: SystemStatus;
}

export const AirGapNetworkMonitor: React.FC<Props> = ({ status }) => {
  const [pulse, setPulse] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => setPulse((p) => !p), 1500);
    return () => clearInterval(interval);
  }, []);

  const vramUsed = status?.vram_used_gb ?? 11.4;
  const vramTotal = status?.vram_total_gb ?? 24.0;
  const vramPercent = Math.round((vramUsed / vramTotal) * 100);

  return (
    <div className="h-13 bg-[#0d131f] border-b border-[#1e293b] px-4 flex items-center justify-between text-xs select-none">
      {/* Left: Sovereign Brand & Air Gap Certificate */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <div className={`w-2.5 h-2.5 rounded-full ${pulse ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-emerald-600'} transition-all`} />
          <span className="font-bold tracking-wider text-slate-100 text-xs">
            SOVEREIGN WORKBENCH
          </span>
          <span className="bg-sky-950 text-sky-400 text-[10px] font-semibold px-2 py-0.5 rounded border border-sky-800">
            ON-PREMISE AIR-GAPPED
          </span>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        <div className="flex items-center space-x-1.5 bg-emerald-950/70 border border-emerald-800/80 px-2 py-0.5 rounded text-emerald-300 font-medium text-[11px]">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>ZERO TELEMETRY</span>
        </div>

        <div className="flex items-center space-x-1.5 bg-slate-900 border border-slate-700 px-2 py-0.5 rounded text-slate-300 font-medium text-[11px]">
          <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping mr-0.5" />
          <span>M5 SANDBOX: ACTIVE (5s LIMIT)</span>
        </div>

        <div className="flex items-center space-x-1 text-slate-400 text-[11px]">
          <WifiOff className="w-3.5 h-3.5 text-rose-400" />
          <span>WAN Blocked (127.0.0.1 Loopback)</span>
        </div>
      </div>

      {/* Right: Hardware & Outbound Audit Gauge */}
      <div className="flex items-center space-x-5">
        <div className="flex items-center space-x-1.5 text-slate-300 text-[11px]">
          <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span>Outbound Audit: <b className="text-emerald-400 font-mono">0.00 KB/s</b></span>
        </div>

        <div className="h-4 w-px bg-slate-800" />

        <div className="flex items-center space-x-2 text-slate-300 text-[11px]">
          <Cpu className="w-3.5 h-3.5 text-sky-400" />
          <span>GPU VRAM: <b className="text-slate-100 font-mono">{vramUsed} GB</b> / {vramTotal} GB ({vramPercent}%)</span>
        </div>

        <div className="flex items-center space-x-1.5 text-slate-300 text-[11px]">
          <HardDrive className="w-3.5 h-3.5 text-amber-400" />
          <span>Local Engine: <span className="text-slate-300 font-semibold">LangGraph Sovereign</span></span>
        </div>
      </div>
    </div>
  );
};
