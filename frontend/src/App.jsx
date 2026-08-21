import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import memeConfig from './memeConfig.json'

export default function App() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('ANALYZING...')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const examples = [
    "Exam tomorrow, haven't studied",
    "I spent my salary in three days",
    "Production is down and I'm the only developer online",
    "I told my boss I'd finish it today",
    "Sent a screenshot of the groupchat TO the groupchat"
  ]

  const loadingPhrases = [
    "Analyzing your situation... 🧠",
    "Calculating your level of cookedness... 🔥",
    "Consulting the emergency kitchen... 💀",
    "Evaluating consequences... 📉"
  ]

  useEffect(() => {
    let interval;
    if (loading) {
      let i = 0;
      setLoadingText(loadingPhrases[i]);
      interval = setInterval(() => {
        i = (i + 1) % loadingPhrases.length;
        setLoadingText(loadingPhrases[i]);
      }, 2500);
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
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      })

      if (!res.ok) {
        throw new Error('Failed to get prediction from the local LLM.')
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message + (err.message.includes("fetch") ? " (Is the backend running?)" : ""))
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score < 20) return "text-green-400"
    if (score < 40) return "text-yellow-400"
    if (score < 60) return "text-orange-400"
    if (score < 80) return "text-red-500"
    return "text-red-700 font-bold drop-shadow-[0_0_15px_rgba(239,68,68,0.8)]"
  }

  const getUrgencyText = (val) => val > 7 ? 'Extremely urgent' : val > 4 ? 'Moderately urgent' : 'Low urgency'
  const getPrepText = (val) => val > 7 ? 'Highly prepared' : val > 4 ? 'Somewhat prepared' : 'Barely prepared'
  const getConsText = (val) => val > 7 ? 'High consequences' : val > 4 ? 'Moderate consequences' : 'Low consequences'
  const getRecovText = (val) => val > 7 ? 'Highly recoverable' : val > 3 ? 'Somewhat recoverable' : 'Difficult to recover'

  const ContextBar = ({ label, value, color, text }) => (
    <div className="mb-4 last:mb-0">
      <div className="flex justify-between mb-1 text-sm">
        <span className="text-slate-300 font-semibold">{label}</span>
        <span className="text-slate-400">{value}/10 — {text}</span>
      </div>
      <div className="w-full bg-slate-700/50 rounded-full h-2.5 overflow-hidden border border-slate-600/30">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${value * 10}%` }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
          className={`h-full rounded-full ${color}`} 
        />
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 flex flex-col items-center">
      <div className="w-full max-w-3xl mt-12">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-extrabold tracking-tight mb-4">
            ARE YOU COOKED? 💀
          </h1>
          <p className="text-xl text-slate-400">
            Describe your situation. Our local AI will tell you how badly you've screwed up.
          </p>
        </motion.div>

        {/* Input Area */}
        <motion.div 
          className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl mb-8"
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
        >
          <form onSubmit={handleSubmit}>
            <textarea
              className="w-full h-32 bg-slate-800 text-white border border-slate-700 rounded-xl p-4 focus:ring-2 focus:ring-red-500 focus:outline-none resize-none text-lg placeholder-slate-500"
              placeholder="Tell us what happened..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="flex justify-between items-center mt-4">
              <span className="text-sm text-slate-500">
                {text.length}/1500 chars
              </span>
              <button
                type="submit"
                disabled={loading || text.length < 5}
                className="bg-gradient-to-r from-red-600 to-orange-500 hover:from-red-500 hover:to-orange-400 text-white font-bold py-3 px-8 rounded-xl shadow-lg transform transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 min-w-[280px] justify-center"
              >
                {loading ? (
                  <span className="flex items-center gap-3">
                    <div className="w-4 h-4 rounded-full border-2 border-white/20 border-t-white animate-spin" />
                    {loadingText}
                  </span>
                ) : 'CHECK MY COOKEDNESS 🔥'}
              </button>
            </div>
          </form>

          {/* Examples */}
          <div className="mt-6">
            <p className="text-sm text-slate-400 mb-3">Try an example:</p>
            <div className="flex flex-wrap gap-2">
              {examples.map((ex, i) => (
                <button
                  key={i}
                  onClick={() => setText(ex)}
                  className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm px-4 py-2 rounded-full transition-colors border border-slate-700"
                >
                  "{ex}"
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Error */}
        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-200 p-4 rounded-xl mb-8 text-center">
            {error}
          </div>
        )}

        {/* Results */}
        <AnimatePresence mode="wait">
          {result && !loading && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ type: "spring", bounce: 0.4 }}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)] text-center relative overflow-hidden"
            >
              
              {result.needs_more_context ? (
                // INSUFFICIENT CONTEXT UI
                <div className="py-8">
                  <div className="text-6xl mb-6">🤔</div>
                  <h2 className="text-2xl font-bold text-slate-200 mb-4">{result.verdict}</h2>
                  <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700 max-w-lg mx-auto text-left">
                    <p className="text-slate-300 mb-3 font-medium">Try including:</p>
                    <ul className="space-y-2 text-slate-400">
                      {result.recommendations.map((r, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-orange-500 mt-0.5">💡</span>
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                // NORMAL UI
                <>
                  <div className="text-slate-400 font-medium uppercase tracking-wider mb-2">
                    Category: {result.category}
                  </div>
                  
                  <div className="mb-8 flex flex-col items-center">
                    <div className={`text-8xl font-black mb-2 ${getScoreColor(result.cooked_score)}`}>
                      {result.cooked_score}<span className="text-4xl text-slate-600">/100</span>
                    </div>
                    <div className={`text-2xl font-bold tracking-widest uppercase ${getScoreColor(result.cooked_score)}`}>
                      {result.cooked_level}
                    </div>
                    
                    {result.level_int !== undefined && memeConfig[result.level_int] && (
                      <motion.div 
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.3 }}
                        className="mt-6 mb-2 rounded-xl overflow-hidden border-4 border-slate-800 shadow-2xl max-w-sm"
                      >
                        <img 
                          src={memeConfig[result.level_int][Math.floor(Math.random() * memeConfig[result.level_int].length)]} 
                          alt="Cooked Reaction GIF" 
                          className="w-full h-auto object-cover"
                        />
                      </motion.div>
                    )}
                  </div>

                  <div className="bg-slate-950 p-6 rounded-xl mb-6 border border-slate-800">
                    <p className="text-xl italic text-slate-300">
                      "{result.verdict}"
                    </p>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6 text-left">
                    <div className="bg-slate-800/50 p-5 rounded-xl border border-slate-700">
                      <h3 className="font-bold text-slate-200 mb-4 flex items-center gap-2">
                        🔍 Why you're cooked:
                      </h3>
                      <ul className="space-y-3 text-slate-300 text-sm mb-6">
                        {result.key_factors.map((r, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-orange-500 mt-0.5">🔥</span>
                            {r}
                          </li>
                        ))}
                      </ul>
                      
                      <h3 className="font-bold text-slate-200 mb-4 flex items-center gap-2 border-t border-slate-700 pt-4">
                        🛠️ Survival Guide:
                      </h3>
                      <ul className="space-y-2 text-slate-400 text-sm">
                        {result.recommendations.map((r, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-green-500 mt-0.5">→</span>
                            {r}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div className="bg-slate-800/50 p-5 rounded-xl border border-slate-700">
                      <h3 className="font-bold text-slate-200 mb-4 flex items-center gap-2">
                        📊 Context Analysis:
                      </h3>
                      <ContextBar 
                        label="Urgency" 
                        value={result.urgency} 
                        color="bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]" 
                        text={getUrgencyText(result.urgency)} 
                      />
                      <ContextBar 
                        label="Preparation" 
                        value={result.preparation} 
                        color="bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" 
                        text={getPrepText(result.preparation)} 
                      />
                      <ContextBar 
                        label="Consequences" 
                        value={result.consequences} 
                        color="bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]" 
                        text={getConsText(result.consequences)} 
                      />
                      <ContextBar 
                        label="Recoverability" 
                        value={result.recoverability} 
                        color="bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" 
                        text={getRecovText(result.recoverability)} 
                      />
                    </div>
                  </div>
                </>
              )}
              
              <div className="mt-8">
                <button 
                  onClick={() => {
                    setResult(null);
                    setText('');
                  }}
                  className="text-slate-500 hover:text-slate-300 underline underline-offset-4 transition-colors"
                >
                  Cook again
                </button>
              </div>

            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
