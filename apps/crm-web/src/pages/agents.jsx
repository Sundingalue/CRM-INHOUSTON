import { useEffect, useState } from 'react'

export default function Agents(){
  const [items, setItems] = useState([])
  const [form, setForm] = useState({
    tenant: '',
    name: '',
    provider: 'elevenlabs',
    model: '',
    voice_id: '',
    language: 'es',
    prompt: '',
    caller_id: '',
    provider_phone: '',
    temperature: '0.7',
    enabled: true
  })
  const [toNumber, setToNumber] = useState('')
  const apiBase = process.env.NEXT_PUBLIC_AGENTS_BASE || 'http://localhost:8010'

  const headers = ()=>{
    const tk = localStorage.getItem('token')
    return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${tk}` }
  }

  const load = async ()=>{
    const r = await fetch(`${apiBase}/agents`, { headers: headers() })
    const data = await r.json()
    setItems(data || [])
  }

  useEffect(()=>{ const tk = localStorage.getItem('token'); if(!tk){ location.href='/'; return } ; load() }, [])

  const save = async ()=>{
    if(!form.name){ alert('Nombre requerido'); return }
    const r = await fetch(`${apiBase}/agents`, { method: 'POST', headers: headers(), body: JSON.stringify(form) })
    const data = await r.json()
    if(data && data.id){ setForm({...form, name:'', prompt:'', voice_id:'', model:''}); load(); alert('Agente creado') }
    else alert(JSON.stringify(data))
  }

  const callNow = async (id)=>{
    if(!toNumber){ alert('Coloca número destino en formato +1...'); return }
    const r = await fetch(`${apiBase}/agents/${id}/outbound_call`, { method: 'POST', headers: headers(), body: JSON.stringify({ to_number: toNumber }) })
    const data = await r.json()
    alert('Llamada enviada: '+ JSON.stringify(data))
  }

  return (
    <div className="container">
      <div className="header">
        <h2>Agentes de IA (voz & texto)</h2>
      </div>

      <div className="card">
        <h3>Crear agente</h3>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'12px'}}>
          <input className="input" placeholder="Nombre" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/>
          <select className="input" value={form.provider} onChange={e=>setForm({...form, provider:e.target.value})}>
            <option value="elevenlabs">ElevenLabs</option>
            <option value="openai">OpenAI</option>
            <option value="gemini">Gemini</option>
          </select>
          <input className="input" placeholder="Modelo (opcional)" value={form.model} onChange={e=>setForm({...form, model:e.target.value})}/>
          <input className="input" placeholder="Voz ID (opcional)" value={form.voice_id} onChange={e=>setForm({...form, voice_id:e.target.value})}/>
          <input className="input" placeholder="Idioma (es/en...)" value={form.language} onChange={e=>setForm({...form, language:e.target.value})}/>
          <input className="input" placeholder="Caller ID (+1... saliente)" value={form.caller_id} onChange={e=>setForm({...form, caller_id:e.target.value})}/>
          <input className="input" placeholder="Número del proveedor (bridge)" value={form.provider_phone} onChange={e=>setForm({...form, provider_phone:e.target.value})}/>
          <input className="input" placeholder="Temperatura" value={form.temperature} onChange={e=>setForm({...form, temperature:e.target.value})}/>
        </div>
        <textarea className="input" placeholder="Prompt del agente" value={form.prompt} onChange={e=>setForm({...form, prompt:e.target.value})}/>
        <button className="button" onClick={save}>Guardar agente</button>
      </div>

      <div className="card">
        <h3>Agentes creados</h3>
        <input className="input" placeholder="Número destino (+1...)" value={toNumber} onChange={e=>setToNumber(e.target.value)}/>
        {items.map(it=> (
          <div className="card" key={it.id}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
              <div>
                <b>{it.name}</b> — {it.provider} {it.model? `(${it.model})`:''} — idioma {it.language}
                <div style={{opacity:.7}}>callerId: {it.caller_id || '—'} | provider_phone: {it.provider_phone || '—'}</div>
              </div>
              <button className="button" onClick={()=>callNow(it.id)}>Llamar</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
