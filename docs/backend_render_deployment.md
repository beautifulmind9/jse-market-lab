# Backend Render Deployment — JSE Market Lab

## Purpose

This document explains how to deploy the FastAPI backend to Render so the Vercel frontend can call a hosted API.

This is an infrastructure step only. It does not launch broker referral, research hosting, user accounts, AI helper, paid products, or any compliance-gated platform features.

---

## Current architecture after deployment

```text
Vercel Next.js frontend
        ↓
Render FastAPI backend
        ↓
Existing Python decision engine
        ↓
Demo/generated data
```

---

## Render service settings

Use the repo:

```text
beautifulmind9/jse-market-lab
```

Service type:

```text
Web Service
```

Runtime:

```text
Python
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Health check path:

```text
/health
```

---

## Environment variables

Set this in Render after the Vercel frontend URL is known:

```text
BACKEND_CORS_ORIGINS=https://your-vercel-project.vercel.app
```

For multiple allowed origins, use a comma-separated list:

```text
BACKEND_CORS_ORIGINS=https://your-vercel-project.vercel.app,http://localhost:3000
```

Do not set secrets directly in code.

---

## Local backend test

From repo root:

```bash
python3 -m uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "jse-market-lab-api"
}
```

---

## Hosted API verification

After Render deploys, test:

```text
https://your-render-service.onrender.com/health
https://your-render-service.onrender.com/api/data/status
```

Expected:

- `/health` returns status ok
- `/api/data/status` returns dataset status JSON

---

## Connect Vercel to Render

In Vercel:

```text
Project Settings
→ Environment Variables
→ Add
```

Name:

```text
NEXT_PUBLIC_API_BASE_URL
```

Value:

```text
https://your-render-service.onrender.com
```

Then redeploy the Vercel frontend.

The homepage data connection card should change from frontend-ready to API-ready once the hosted backend is reachable.

---

## Guardrails

This deployment must preserve the product boundary:

- decision support only
- no personal investment advice
- no buy/sell instructions
- no guaranteed outcomes
- no prediction claims
- no trade execution
- no holding client funds
- no broker-dealer positioning

---

## What not to deploy yet

Do not launch these until data, compliance, storage, and review gates are ready:

- Brokerage Access Flow
- broker referral routing
- sponsored content
- Research Hub hosting
- analyst scoring / leaderboard
- public AI helper
- user profiles
- Setup Tester / Paper Portfolio
- paid subscriptions

---

## Troubleshooting

### Frontend cannot reach backend

Check:

- Render service is awake/running
- `/health` works directly in browser
- `BACKEND_CORS_ORIGINS` includes the exact Vercel URL
- Vercel has `NEXT_PUBLIC_API_BASE_URL` set correctly
- Vercel frontend was redeployed after setting environment variable

### Render build fails

Check:

- `requirements.txt` installs successfully
- Python version is supported
- Start command uses `$PORT`
- Backend imports do not depend on local-only files

### First request is slow

Free/low-cost services may sleep after inactivity. This is acceptable for beta testing but should be upgraded before paid users rely on the platform.
