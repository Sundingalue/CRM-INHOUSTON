import { useState } from 'react'

export default function Home(){
  const [email, setEmail] = useState('owner@example.com')
  const [password, setPassword] = useState('test1234')
  const [tenantName, setTenantName] = useState('Empresa Demo')
  const [tenantSlug, setTenantSlug] = useState('empresa-demo')
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

  const register = async ()=>{
    const r = await fetch(`${apiBase}/auth/register`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({tenant_name:tenantName, tenant_slug:tenantSlug, email, password, full_name:'Demo Owner'})
    })
    const data = await r.json()
    if(data.access_token){ localStorage.setItem('token', data.access_token); location.href='/dashboard'}
    else alert(JSON.stringify(data))
  }

  const login = async ()=>{
    const r = await fetch(`${apiBase}/auth/login`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email, password})
    })
    const data = await r.json()
    if(data.access_token){ localStorage.setItem('token', data.access_token); location.href='/dashboard'}
    else alert(JSON.stringify(data))
  }

  return (
    <div className="container">
      <div className="header">
        <img className="logo" src="/logo.svg" alt="logo"/>
        <h2>CRM - INHOUSTON</h2>
      </div>
      <div className="card">
        <h3>Iniciar sesión</h3>
        <input className="input" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/>
        <input className="input" value={password} onChange={e=>setPassword(e.target.value)} type="password" placeholder="Contraseña"/>
        <button className="button" onClick={login}>Entrar</button>
      </div>
      <div className="card">
        <h3>Crear empresa (demo rápida)</h3>
        <input className="input" value={tenantName} onChange={e=>setTenantName(e.target.value)} placeholder="Nombre de empresa"/>
        <input className="input" value={tenantSlug} onChange={e=>setTenantSlug(e.target.value)} placeholder="Slug (ej. mi-empresa)"/>
        <input className="input" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email dueño"/>
        <input className="input" value={password} onChange={e=>setPassword(e.target.value)} type="password" placeholder="Contraseña"/>
        <button className="button" onClick={register}>Crear y entrar</button>
      </div>
      <p style={{opacity:.6}}>API: {apiBase}</p>
    </div>
  )
}
