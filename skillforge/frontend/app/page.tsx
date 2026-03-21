"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import GraphVisualizer from "@/components/GraphVisualizer";
import ReasoningPanel from "@/components/ReasoningPanel";
import { UploadCloud, Zap, Code, FileText } from "lucide-react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [pathData, setPathData] = useState<any>(null);

  const generatePath = async () => {
    setLoading(true);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/api/generate_path`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
      });
      const json = await res.json();
      setPathData(json.data);
    } catch (e) {
      console.error(e);
      alert("Backend error. Make sure FastAPI is running on port 8000.");
    }
    setLoading(false);
  };

  const loadDemoData = () => {
    setResumeText("Passionate Backend Software Engineer. Built microservices with Python and Django. Familiar with HTML/CSS and basic Javascript.");
    setJdText("Looking for a Fullstack Cloud Developer. Must have strong skills in Python, FastAPI, React, and Kubernetes for scaling containers.");
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      setResumeText("Extracting text from PDF (Talking to FastAPI)...");
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/api/upload`, {
        method: "POST",
        body: formData
      });
      const json = await res.json();
      setResumeText(json.text);
    } catch (err) {
      console.error(err);
      setResumeText("Failed to extract PDF. Make sure backend is running on 8000.");
    }
  };

  return (
    <main className="min-h-screen p-8 max-w-[1600px] mx-auto flex flex-col gap-6">
      <header className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600 flex items-center">
            <Zap className="mr-3 text-cyan-400" size={36} /> SkillForge
          </h1>
          <p className="text-slate-400 mt-1 font-mono text-sm tracking-wide uppercase">AI-Adaptive Onboarding Engine</p>
        </div>
        {!pathData && (
           <button onClick={loadDemoData} className="text-xs bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded border border-slate-700 font-mono text-slate-300 transition">
             Load Demo Data
           </button>
        )}
      </header>

      {!pathData ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
          {/* Resume Upload */}
          <div className="glass-panel p-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition duration-500"></div>
            <div className="flex justify-between items-center mb-4 relative z-10">
              <h2 className="text-2xl font-bold flex items-center">
                <FileText className="mr-2 text-indigo-400" /> Resume / Experience
              </h2>
              <label className="cursor-pointer bg-indigo-500/20 hover:bg-indigo-500/40 text-indigo-300 px-4 py-2 rounded-lg text-sm font-bold border border-indigo-500/30 transition flex items-center">
                 <UploadCloud size={16} className="mr-2" />
                 Upload PDF
                 <input type="file" className="hidden" accept=".pdf,.txt" onChange={handleFileUpload} />
              </label>
            </div>
            <textarea 
              className="w-full h-72 bg-slate-950/50 text-slate-200 border border-slate-700 rounded-xl p-5 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition font-medium relative z-10"
              placeholder="Paste Candidate Resume or current skills here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          </div>

          {/* JD Upload */}
          <div className="glass-panel p-8 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl group-hover:bg-emerald-500/20 transition duration-500"></div>
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Code className="mr-2 text-emerald-400" /> Target Job Description
            </h2>
            <textarea 
              className="w-full h-72 bg-slate-950/50 text-slate-200 border border-slate-700 rounded-xl p-5 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition font-medium"
              placeholder="Paste target Job Description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>

          <div className="col-span-1 md:col-span-2 flex justify-center mt-6">
            <button 
              onClick={generatePath}
              disabled={loading || !resumeText || !jdText}
              className="bg-sky-500 hover:bg-sky-400 text-slate-950 font-extrabold text-xl py-5 px-14 rounded-full transition-all flex items-center shadow-[0_0_40px_rgba(56,189,248,0.4)] disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105 active:scale-95"
            >
              {loading ? (
                <span className="flex items-center"><div className="animate-spin h-6 w-6 border-3 border-slate-950 border-t-transparent rounded-full mr-3"></div> Mapping Graph...</span>
              ) : (
                <span className="flex items-center"><UploadCloud className="mr-3" size={24} /> Engine Start: Analyze Gap</span>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[75vh]">
          {/* Dashboard Left: Reasoning */}
          <div className="col-span-1 flex flex-col gap-6 h-full">
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4 }}
              className="glass-panel p-8 shrink-0 shadow-[0_0_40px_rgba(56,189,248,0.1)] border-t border-sky-500/30"
            >
              <h3 className="text-2xl font-extrabold mb-5 flex items-center text-slate-100">
                <Zap className="text-yellow-400 mr-2 drop-shadow-[0_0_10px_rgba(250,204,21,0.8)]" size={24}/> 
                Validation Data
              </h3>
              <div className="flex flex-col gap-5 mb-6">
                <motion.div 
                  whileHover={{ scale: 1.01 }}
                  className="bg-emerald-950/40 border-2 border-emerald-800/60 rounded-xl flex-1 p-5 overflow-y-auto max-h-48 shadow-inner"
                >
                  <p className="text-[11px] text-emerald-400 font-bold tracking-widest uppercase mb-4 flex items-center">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span> Validated Skills & Levels
                  </p>
                  <div className="flex flex-wrap gap-3">
                    {pathData.user_skills.length > 0 ? pathData.user_skills.map((sk: any, i: number) => (
                      <motion.span 
                        whileHover={{ scale: 1.1, y: -2 }}
                        key={i} 
                        className="cursor-pointer inline-flex items-center bg-slate-900 border border-emerald-500/40 text-sm px-3 py-1.5 rounded-lg shadow-lg hover:shadow-emerald-500/20 hover:border-emerald-400 transition-colors"
                      >
                        {sk.skill} <span className="text-emerald-400 font-mono ml-2 font-bold bg-emerald-950/50 px-1.5 rounded">[{sk.level}]</span>
                      </motion.span>
                    )) : <span className="text-sm text-emerald-200/50 italic">None selected</span>}
                  </div>
                </motion.div>
                <motion.div 
                  whileHover={{ scale: 1.01 }}
                  className="bg-rose-950/40 border-2 border-rose-800/60 rounded-xl flex-1 p-5 overflow-y-auto max-h-48 shadow-inner"
                >
                  <p className="text-[11px] text-rose-400 font-bold tracking-widest uppercase mb-4 flex items-center">
                    <span className="w-2 h-2 rounded-full bg-rose-500 mr-2 animate-pulse shadow-[0_0_8px_rgba(244,63,94,0.8)]"></span> Competency Gap
                  </p>
                  <div className="flex flex-wrap gap-3">
                    {pathData.required_skills.filter((rSk: any) => !pathData.user_skills.find((uSk: any) => uSk.skill === rSk.skill)).length > 0 
                      ? pathData.required_skills.filter((rSk: any) => !pathData.user_skills.find((uSk: any) => uSk.skill === rSk.skill)).map((sk: any, i: number) => (
                        <motion.span 
                          whileHover={{ scale: 1.1, y: -2 }}
                          key={i} 
                          className="cursor-pointer inline-flex items-center bg-slate-900 border border-rose-500/40 text-sm px-3 py-1.5 rounded-lg shadow-lg hover:shadow-rose-500/20 hover:border-rose-400 transition-colors"
                        >
                          {sk.skill} <span className="text-rose-400 font-mono ml-2 font-bold bg-rose-950/50 px-1.5 rounded">[{sk.level}]</span>
                        </motion.span>
                    )) : <span className="text-sm text-rose-200/50 italic">Target Match Perfect</span>}
                  </div>
                </motion.div>
              </div>
              <motion.button 
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setPathData(null)}
                className="w-full py-4 bg-slate-800 hover:bg-slate-700 transition rounded-xl text-base font-bold border border-slate-600 shadow-md text-slate-200"
              >
                ← Back to Upload
              </motion.button>
            </motion.div>
            
            <ReasoningPanel items={pathData.reasoning} />
          </div>

          {/* Dashboard Right: Interactive Graph */}
          <div className="col-span-1 lg:col-span-2 h-full">
             <GraphVisualizer nodes={pathData.graph.nodes} edges={pathData.graph.edges} />
          </div>
        </div>
      )}
    </main>
  );
}
