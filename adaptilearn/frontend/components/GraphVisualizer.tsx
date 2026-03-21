"use client";

import React from 'react';
import ReactFlow, { Background, Controls, Node, Edge, Handle, Position, MarkerType, BackgroundVariant } from 'reactflow';
import 'reactflow/dist/style.css';

interface GraphVisualizerProps {
  nodes: Node[];
  edges: Edge[];
}

// Highly attractive custom node component
const CustomNode = ({ data }: any) => {
  return (
    <div className="relative group px-6 py-4 bg-gradient-to-br from-slate-900 via-indigo-950/60 to-slate-900 border border-sky-400/40 rounded-2xl shadow-[0_4px_25px_rgba(56,189,248,0.25)] hover:shadow-[0_0_40px_rgba(56,189,248,0.9)] hover:scale-110 hover:-translate-y-1 hover:border-sky-300 transition-all duration-300 backdrop-blur-xl">
      {/* Glowing pulsing dot on top rim */}
      <div className="absolute -top-1.5 right-4 w-2.5 h-2.5 rounded-full bg-cyan-300 animate-ping opacity-75"></div>
      <div className="absolute -top-1.5 right-4 w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_12px_#22d3ee]"></div>
      
      <Handle type="target" position={Position.Top} className="!w-3 !h-3 !bg-cyan-400 !border-none !rounded-full shadow-[0_0_12px_rgba(34,211,238,1)]" />
      <div className="flex items-center justify-center min-w-[140px]">
        <span className="font-black text-transparent bg-clip-text bg-gradient-to-br from-cyan-300 to-indigo-300 tracking-widest text-[16px] drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">
          {data.label}
        </span>
      </div>
      <Handle type="source" position={Position.Bottom} className="!w-3 !h-3 !bg-indigo-400 !border-none !rounded-full shadow-[0_0_12px_rgba(129,140,248,1)]" />
    </div>
  );
};

const nodeTypes = { custom: CustomNode };

export default function GraphVisualizer({ nodes, edges }: GraphVisualizerProps) {
  const styledNodes = nodes.map((n, i) => ({
    ...n,
    type: 'custom',
    position: { x: i % 2 === 0 ? 100 : 350, y: i * 90 }, 
  }));

  const styledEdges = edges.map(e => ({
    ...e,
    animated: true,
    style: { stroke: '#818cf8', strokeWidth: 3, filter: 'drop-shadow(0 0 10px rgba(129,140,248,0.8))' },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      width: 20,
      height: 20,
      color: '#818cf8',
    },
  }));

  return (
    <div className="w-full h-full rounded-2xl overflow-hidden relative group shadow-[0_0_50px_rgba(56,189,248,0.05)] border-t border-sky-500/20 bg-[#0a0f1c]">
      
      {/* Insanely Cool Animated Background Orbs (Theme Matched) */}
      <div className="absolute -top-32 -left-32 w-[30rem] h-[30rem] bg-indigo-500/15 rounded-full blur-[120px] mix-blend-screen pointer-events-none animate-pulse"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[40rem] h-[40rem] bg-sky-600/10 rounded-full blur-[150px] mix-blend-screen pointer-events-none"></div>
      <div className="absolute -bottom-32 -right-32 w-[30rem] h-[30rem] bg-indigo-500/15 rounded-full blur-[120px] mix-blend-screen pointer-events-none animate-pulse" style={{ animationDelay: '1s' }}></div>

      {/* Topology Badge */}
      <div className="absolute top-6 left-6 z-10 bg-slate-900/60 px-6 py-3 border border-sky-500/30 rounded-xl text-sm font-black tracking-widest text-sky-400 shadow-[0_4px_30px_rgba(56,189,248,0.2)] flex items-center backdrop-blur-md transition-all">
        <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 mr-3 animate-ping shadow-[0_0_12px_rgba(34,211,238,0.8)] absolute"></span>
        <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 mr-3 relative shadow-[0_0_12px_rgba(34,211,238,0.8)]"></span>
        Learning Path Topology
      </div>
      
      {/* Foreground ReactFlow */}
      <ReactFlow 
        nodes={styledNodes} 
        edges={styledEdges} 
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-right"
        className="z-10"
      >
        <Background 
          color="#1e293b" 
          gap={32} 
          lineWidth={1.5} 
          variant={BackgroundVariant.Lines} 
          className="opacity-70" 
        />
        <Controls className="!bg-slate-900/80 !border-sky-500/30 !fill-sky-400 hover:!fill-white shadow-[0_0_20px_rgba(56,189,248,0.1)] backdrop-blur-xl rounded-xl overflow-hidden" />
      </ReactFlow>
    </div>
  );
}
