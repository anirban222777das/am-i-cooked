import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import memeConfig from './memeConfig.json'

export default function App() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('[SYSTEM]: INITIATING TELEMETRY...')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const examples = [
    "Exam tomorrow, haven't studied",
    "I spent my salary in three days",
    "Production is down and I'm the only developer online",
    "Sent a screenshot of the groupchat TO the groupchat"
  ]

  const terminalPhrases = [
    "[SYSTEM]: INITIATING DISASTER TELEMETRY...",
    "[WARNING]: HIGH LEVELS OF PROCRASTINATION DETECTED...",
    "[CALCULATING]: ESTIMATING RADIUS OF DESTRUCTION...",
    "[ANALYSIS]: CONSULTING THE EMERGENCY KITCHEN..."
  ]

  useEffect(() => {
    let interval;
    if (loading) {
      let i = 0;
      setLoadingText(terminalPhrases[i]);
      interval = setInterval(() => {
        i = (i + 1) % terminalPhrases.length;
        setLoadingText(terminalPhrases[i]);
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleSubmit = async (e) => {
    e?.preventDefault()
    if (text.length < 5) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })

      if (!res.ok) throw new Error('Failed to reach telemetry servers.')
      
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message + (err.message.includes("fetch") ? " (Is the backend running?)" : ""))
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score < 20) return "text-green-500 drop-shadow-[0_0_10px_rgba(34,197,94,0.5)]"
    if (score < 40) return "text-yellow-400 drop-shadow-[0_0_10px_rgba(250,204,21,0.5)]"
    if (score < 60) return "text-orange-500 glow-orange"
    if (score < 80) return "text-red-500 glow-red"
    return "text-red-700 glow-red font-black"
  }

  const getUrgencyText = (val) => val > 7 ? 'CRITICAL' : val > 4 ? 'ELEVATED' : 'NOMINAL'
  const getPrepText = (val) => val > 7 ? 'OPTIMAL' : val > 4 ? 'MARGINAL' : 'DEFICIENT'
  const getConsText = (val) => val > 7 ? 'SEVERE' : val > 4 ? 'MODERATE' : 'MINIMAL'
  const getRecovText = (val) => val > 7 ? 'HIGH' : val > 3 ? 'POSSIBLE' : 'UNLIKELY'

  const ContextBar = ({ label, value, color, text }) => (
    <div className="mb-4 font-terminal">
      <div className="flex justify-between mb-1 text-xs uppercase tracking-widest">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-300">[{value}/10] {text}</span>
      </div>
      <div className="w-full bg-slate-900/80 h-3 border border-slate-700/50">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${value * 10}%` }}
          transition={{ duration: 1.5, ease: "circOut" }}
          className={`h-full ${color}`} 
        />
      </div>
    </div>
  )

  // Screen shake for extreme scores
  const containerVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: (score) => ({
      opacity: 1, 
      scale: 1,
      x: score >= 90 ? [0, -10, 10, -10, 10, 0] : 0,
      transition: {
        type: "spring",
        bounce: 0.4,
        x: { duration: 0.4, ease: "easeInOut" }
      }
    })
  }

  return (
    <div className="min-h-screen bg-slate-950 bg-grid-slate-900 text-slate-100 p-6 flex flex-col items-center font-body overflow-x-hidden relative">
      {/* Absolute ambient light */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-red-900/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="w-full max-w-4xl mt-12 z-10">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="font-display text-7xl md:text-8xl tracking-wider mb-2 text-white drop-shadow-2xl">
            AM I COOKED? <span className="text-red-500 glow-red">💀</span>
          </h1>
          <p className="font-terminal text-sm md:text-base text-slate-400 uppercase tracking-widest">
            Diagnostic Telemetry System v2.0
          </p>
        </motion.div>

        {/* Input Area */}
        <motion.div 
          className="glass-panel p-6 mb-8 relative"
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-600 via-orange-500 to-red-600 opacity-50" />
          
          <form onSubmit={handleSubmit}>
            <div className="relative">
              <div className="absolute top-3 left-3 text-red-500/50 font-terminal text-xs">
                &gt; INCIDENT_REPORT.txt
              </div>
              <textarea
                className="w-full h-36 bg-slate-950/80 text-green-400 font-terminal border border-slate-700/50 p-4 pt-8 focus:border-red-500/50 focus:ring-1 focus:ring-red-500/50 focus:outline-none resize-none text-sm placeholder-slate-600/50"
                placeholder="Describe the catastrophe..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                spellCheck="false"
              />
            </div>

            <div className="flex flex-col md:flex-row justify-between items-center mt-6 gap-4">
              <span className="font-terminal text-xs text-slate-500">
                CHARS: {text.length}/1500
              </span>
              <button
                type="submit"
                disabled={loading || text.length < 5}
                className="relative group bg-red-950/40 hover:bg-red-900/60 border border-red-500/50 text-red-400 font-display text-2xl tracking-widest py-3 px-12 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden w-full md:w-auto"
              >
                {/* Hazard stripes background effect on hover */}
                <div className="absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,#ef4444_10px,#ef4444_20px)]" />
                
                {loading ? (
                  <span className="font-terminal text-sm flex items-center justify-center gap-3 relative z-10 text-orange-400">
                    <div className="w-3 h-3 bg-orange-500 animate-ping" />
                    {loadingText}
                  </span>
                ) : (
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    <span className="text-red-500">⚠</span> INITIATE DIAGNOSTIC <span className="text-red-500">⚠</span>
                  </span>
                )}
              </button>
            </div>
          </form>

          {/* Examples */}
          <div className="mt-8 border-t border-slate-800/50 pt-4">
            <p className="font-terminal text-xs text-slate-500 mb-3 uppercase tracking-widest">Load Previous Incidents:</p>
            <div className="flex flex-wrap gap-2">
              {examples.map((ex, i) => (
                <button
                  key={i}
                  onClick={() => setText(ex)}
                  className="font-terminal text-xs bg-slate-900/50 hover:bg-slate-800 text-slate-400 px-3 py-1.5 transition-colors border border-slate-700/50"
                >
                  [{i+1}] {ex.substring(0, 20)}...
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Error */}
        {error && (
          <div className="font-terminal bg-red-950/80 border border-red-500 text-red-400 p-4 mb-8 text-sm uppercase">
            [FATAL ERROR]: {error}
          </div>
        )}

        {/* Results */}
        <AnimatePresence mode="wait">
          {result && !loading && (
            <motion.div
              key="result"
              custom={result.cooked_score || 0}
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel p-1 relative overflow-hidden"
            >
              
              {result.needs_more_context ? (
                // INSUFFICIENT CONTEXT UI (Kernel Panic Style)
                <div className="p-8 bg-blue-950/20 border border-blue-500/30">
                  <div className="font-terminal text-blue-400 mb-6">
                    <p className="text-2xl mb-2">*** STOP: 0x00000042 (INSUFFICIENT_CONTEXT_ERROR)</p>
                    <p className="text-sm">A critical diagnostic failure has occurred. The system could not evaluate your situation because you provided vague or meaningless data.</p>
                  </div>
                  
                  <div className="font-body bg-slate-950/80 p-6 border border-slate-800 text-left">
                    <p className="text-xl font-bold text-slate-200 mb-3">{result.verdict}</p>
                    <p className="font-terminal text-xs text-slate-500 mb-4 uppercase">Required Parameters:</p>
                    <ul className="space-y-3 font-terminal text-sm text-slate-400">
                      {result.recommendations.map((r, i) => (
                        <li key={i} className="flex items-start gap-3">
                          <span className="text-blue-500 mt-0.5">&gt;</span>
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                // NORMAL UI (Clinical Dashboard)
                <div className="p-1">
                  <div className="bg-slate-950/80 p-8 flex flex-col items-center border border-slate-800">
                    <div className="font-terminal text-xs text-slate-500 uppercase tracking-[0.3em] mb-4">
                      Diagnostic Result // Cat: {result.category}
                    </div>
                    
                    <div className={`font-display text-9xl leading-none mb-2 ${getScoreColor(result.cooked_score)}`}>
                      {result.cooked_score}<span className="text-4xl text-slate-600 font-terminal">/100</span>
                    </div>
                    <div className={`font-terminal text-xl tracking-widest uppercase mb-8 ${getScoreColor(result.cooked_score)}`}>
                      [{result.cooked_level}]
                    </div>
                    
                    {result.level_int !== undefined && memeConfig[result.level_int] && (
                      <motion.div 
                        initial={{ opacity: 0, filter: "blur(10px)" }}
                        animate={{ opacity: 1, filter: "blur(0px)" }}
                        transition={{ delay: 0.5, duration: 0.8 }}
                        className="w-full max-w-md border border-slate-700/50 p-2 bg-slate-900/50 mb-8"
                      >
                        <div className="font-terminal text-[10px] text-slate-500 mb-1 flex justify-between">
                          <span>VISUAL_TELEMETRY.gif</span>
                          <span>SYS_OK</span>
                        </div>
                        <img 
                          src={memeConfig[result.level_int][Math.floor(Math.random() * memeConfig[result.level_int].length)]} 
                          alt="Cooked Reaction GIF" 
                          className="w-full h-auto grayscale-[20%] contrast-125"
                        />
                      </motion.div>
                    )}

                    <div className="w-full text-center p-4 bg-slate-900/50 border border-slate-700/50">
                      <p className="font-terminal text-sm md:text-base text-slate-300">
                        "{result.verdict}"
                      </p>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-1 mt-1">
                    {/* Telemetry Breakdown */}
                    <div className="bg-slate-950/80 p-6 border border-slate-800">
                      <h3 className="font-terminal text-xs text-slate-500 uppercase tracking-widest mb-6">
                        System Analysis
                      </h3>
                      <ContextBar 
                        label="Urgency" 
                        value={result.urgency} 
                        color="bg-red-500" 
                        text={getUrgencyText(result.urgency)} 
                      />
                      <ContextBar 
                        label="Preparation" 
                        value={result.preparation} 
                        color="bg-emerald-500" 
                        text={getPrepText(result.preparation)} 
                      />
                      <ContextBar 
                        label="Consequences" 
                        value={result.consequences} 
                        color="bg-red-500" 
                        text={getConsText(result.consequences)} 
                      />
                      <ContextBar 
                        label="Recoverability" 
                        value={result.recoverability} 
                        color="bg-emerald-500" 
                        text={getRecovText(result.recoverability)} 
                      />
                    </div>
                    
                    {/* Action Items */}
                    <div className="bg-slate-950/80 p-6 border border-slate-800">
                      <h3 className="font-terminal text-xs text-slate-500 uppercase tracking-widest mb-6">
                        Incident Breakdown
                      </h3>
                      <div className="mb-6">
                        <div className="font-terminal text-[10px] text-red-400 mb-2 border-b border-red-900/50 pb-1">DETECTED VULNERABILITIES</div>
                        <ul className="space-y-2 font-terminal text-xs text-slate-300">
                          {result.key_factors.map((r, i) => (
                            <li key={i} className="flex gap-2">
                              <span className="text-red-500 opacity-70">×</span> {r}
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <div className="font-terminal text-[10px] text-emerald-400 mb-2 border-b border-emerald-900/50 pb-1">RECOMMENDED PROTOCOLS</div>
                        <ul className="space-y-2 font-terminal text-xs text-slate-400">
                          {result.recommendations.map((r, i) => (
                            <li key={i} className="flex gap-2">
                              <span className="text-emerald-500 opacity-70">↓</span> {r}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div className="bg-slate-950/90 py-4 text-center border-t border-slate-800">
                <button 
                  onClick={() => {
                    setResult(null);
                    setText('');
                  }}
                  className="font-terminal text-xs text-slate-500 hover:text-white transition-colors"
                >
                  [ RESET_DIAGNOSTIC ]
                </button>
              </div>

            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
