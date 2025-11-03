import { useEffect, useState } from 'react'

export default function Dashboard(){
  const [branding,setBranding]=useState(null)
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

  useEffect(()=>{
    const token = localStorage.getItem('token')
    if(!token){ location.href='/'; return}
    fetch(`${apiBase}/branding`, { headers:{Authorization:`Bearer ${token}`}})
      .then(r=>r.json()).then((b)=>{
        setBranding(b);
        if(b?.color_primary) document.documentElement.style.setProperty('--brand-primary', b.color_primary);
        if(b?.color_accent) document.documentElement.style.setProperty('--brand-accent', b.color_accent);
      })
  },[])

  return (
    <div className="container">
      <div className="header brand">
        <img className="logo" src={branding?.logo_url || '/logo.svg'} alt="logo"/>
        <h2>{branding?.name || 'Mi Empresa'}</h2>
      </div>

      <div className="kpi">
        <div className="card"><h3>Leads</h3><div>—</div></div>
        <div className="card"><h3>Conversaciones</h3><div>—</div></div>
        <div className="card"><h3>Citas hoy</h3><div>—</div></div>
        <div className="card"><h3>Minutos IA</h3><div>—</div></div>
      </div>

      <div className="card">
        <h3>Configuración rápida</h3>
        <ol>
          <li>Sube tu logo y colores (próximo paso de UI).</li>
          <li><a href="/agents">Agentes de IA</a> — crea tu primer agente de voz.</li>
          <li>Conecta Instagram / WhatsApp / SMS / Email.</li>
          <li>Importa contactos y lanza tu primera campaña.</li>
        </ol>
      </div>
    </div>
  )
}
