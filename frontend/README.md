# JSE Market Lab Frontend

This folder contains the Next.js frontend for the Vercel migration.

## Local development

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Vercel setup

When importing the GitHub repo into Vercel, use:

```text
Root Directory: frontend
Framework Preset: Next.js
Install Command: npm install
Build Command: npm run build
Output Directory: .next
```

## Backend API URL

The frontend can connect to the FastAPI backend through:

```text
NEXT_PUBLIC_API_BASE_URL
```

Local example:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Production example:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-backend-host.example.com
```

If this variable is not set, the frontend still deploys and shows a frontend-ready status. API-backed product screens can be connected after the backend is hosted.

## Demo mode

Until official JSE data authorization/API access is confirmed, use demo mode when showing the site to advisors, testers, partners, or potential users.

Set:

```text
NEXT_PUBLIC_DEMO_MODE=true
```

Demo mode displays a banner and `/demo` explanation page clarifying that the current experience uses sample or transformed historical data for product demonstration. It is not an official live JSE feed and is not financial advice.

## Product guardrails

This frontend should preserve JSE Market Lab's positioning:

- decision support, not financial advice
- no buy/sell instructions
- no prediction claims
- no guaranteed returns
- user agency remains clear
- missing or weak data should be disclosed
- demo mode must not imply official JSE API/data authorization
