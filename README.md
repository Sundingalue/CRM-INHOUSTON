# CRM - INHOUSTON

Monorepo listo para **Render + GitHub + WordPress**, con un solo dominio público `crm.inhoustontexas.us`.
Incluye: **Login**, **Multi-empresa (tenant) + branding por cliente**, **CRM base**, **Omnicanal (conector pendiente)**,
**Agentes de IA** (servicio propio con JWT y tenant en token), **Campañas/Journeys (placeholder)** y **plugin de WordPress** para embeber el CRM.

> Versión: v0.2.1 (scaffold funcional con Agents + JWT + tenant).
> Tras el deploy, verás Login, Dashboard por tenant, Configuración de marca y módulo de **Agentes** protegido.

## Servicios
- **crm-api** (FastAPI, Postgres): Auth, Tenants, Branding, /me (JWT con `tid`).
- **agents-service** (FastAPI): CRUD de agentes IA + llamadas salientes y webhook entrante (TwiML), **protegido con JWT**.
- **crm-web** (Next.js): UI del CRM (login, dashboard, agentes).
- **Postgres** y **Redis** (colas) vía Docker Compose local. En Render se crean como recursos gestionados.
- **wp-plugin/inh-crm-embed**: plugin para embeber el CRM en WordPress.

## Desarrollo local (rápido)
1) Copia `.env.example` a `.env` y ajusta valores mínimos.
2) Ejecuta: `docker compose up --build`
3) Abre **http://localhost:3000** (web) y **http://localhost:8000/docs** (API).

## Despliegue en Render
- Crea 3 servicios: **CRM-API (Web Service)**, **CRM-WEB (Web Service/Static)**, **AGENTS (Web Service)**.
- Crea **Postgres** y **Redis** administrados por Render.
- En **CRM-WEB** define `NEXT_PUBLIC_API_BASE=https://<TU-API>.onrender.com` y `NEXT_PUBLIC_AGENTS_BASE=https://<TU-AGENTS>.onrender.com`.
- Asigna **crm.inhoustontexas.us** al **CRM-WEB** (o frontal con Nginx si prefieres).

## Estructura
- `apps/crm-api/` → FastAPI (auth/tenants/branding/usuarios)
- `apps/agents-service/` → FastAPI (voz IA, llamadas)
- `apps/crm-web/` → Next.js (UI)
- `wp-plugin/inh-crm-embed/` → Plugin WP para embeber el CRM
- `docker-compose.yml` → entorno local
- `.env.example` → variables de entorno

## Notas
- Un solo dominio: tras login, el usuario ve **su** empresa (tenant) y **branding**.
- Agentes IA: servicio propio protegido con JWT; toma el tenant del token.
- Omnicanal: se conecta luego (IG/FB/WA/SMS/Email) vía asistentes de conexión.

---

© In Houston Texas
