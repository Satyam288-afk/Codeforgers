import { Info, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

interface Reasoning {
  skill: string;
  reason: string;
}

export default function ReasoningPanel({ items }: { items: Reasoning[] }) {
  if (!items || items.length === 0) return (
     <div className="glass-panel p-6">
         <p className="text-slate-400">No competency gap detected.</p>
     </div>
  );

  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass-panel p-6 overflow-y-auto flex-1 shadow-[0_0_30px_rgba(56,189,248,0.05)] border-t border-indigo-500/20"
    >
      <h3 className="text-2xl font-extrabold mb-4 flex items-center text-white">
        <Sparkles className="mr-3 text-sky-400 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" size={24} /> Reasoning Trace Engine
      </h3>
      <p className="text-slate-300 text-sm mb-6 leading-relaxed">
        Absolute explainability. The system explicitly traces back to your target Job Description to justify required learning modules.
      </p>

      <motion.div 
        initial="hidden"
        animate="visible"
        variants={{
          visible: { transition: { staggerChildren: 0.15 } }
        }}
        className="space-y-4"
      >
        {items.map((item, idx) => (
          <motion.div 
            key={idx} 
            variants={{
              hidden: { opacity: 0, x: -20 },
              visible: { opacity: 1, x: 0 }
            }}
            whileHover={{ scale: 1.02, x: 5 }}
            className="bg-slate-800/90 p-5 rounded-xl border-l-4 border-l-sky-500 border-y border-r border-slate-700 shadow-xl cursor-default transition-shadow hover:shadow-sky-500/10"
          >
            <h4 className="font-extrabold text-sky-400 mb-3 truncate flex items-center text-lg">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-400 mr-3 animate-pulse shadow-[0_0_8px_rgba(56,189,248,0.8)]"></span>
              {item.skill} Node
            </h4>
            <p className="text-sm text-slate-200 leading-relaxed font-medium">
              <span className="font-mono text-[10px] tracking-wider font-extrabold bg-slate-950 px-2 py-1 rounded text-pink-400 mr-3 align-middle border border-slate-800 shadow-inner">CITED LOGIC</span>
              {item.reason}
            </p>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}
