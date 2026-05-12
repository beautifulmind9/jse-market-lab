import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';
import { DEMO_MODE_MESSAGE } from '@/lib/demoMode';

const demoSurfaces = [
  'Market-first homepage',
  'Demo Market Pulse',
  'Companies research entry page',
  'Tools decision-support hub',
  'Portfolio Plan',
  'Ticker Analysis',
  'Decision Audit',
  'AI Helper shell',
  'Platform Preview',
];

const notYetLive = [
  'Official JSE API integration',
  'Official live JSE data feed',
  'Broker referral routing',
  'Trade execution',
  'User accounts or saved portfolios',
  'Setup Tester / Paper Portfolio persistence',
  'Search-enabled AI research mode',
  'Paid research or sponsored placements',
];

const walkthroughSteps = [
  {
    title: '1. Start with the homepage',
    label: 'Market first',
    body: 'Show that users see market context immediately before choosing a path.',
    href: '/',
  },
  {
    title: '2. Open Market Pulse',
    label: 'Market context',
    body: 'Explain demo/internal market notes, signal clusters, and liquidity watch.',
    href: '/market',
  },
  {
    title: '3. Open Companies',
    label: 'Research entry',
    body: 'Show how users move from broad market context into company/ticker research.',
    href: '/companies',
  },
  {
    title: '4. Open Tools',
    label: 'Decision support',
    body: 'Show the working tools and future simulation tools in one decision-support hub.',
    href: '/tools',
  },
  {
    title: '5. Open Portfolio Plan',
    label: 'Decision engine',
    body: 'Show funded setups, unfunded setups, reserve cash, and cost assumptions.',
    href: '/portfolio',
  },
  {
    title: '6. Open Ticker Analysis',
    label: 'Single ticker',
    body: 'Use one ticker to explain holding windows, risk context, and what to watch.',
    href: '/ticker/JMMBGL',
  },
  {
    title: '7. Open Decision Audit',
    label: 'Trust layer',
    body: 'Show how the platform explains the rules behind the output.',
    href: '/review',
  },
  {
    title: '8. Use Guide Me',
    label: 'AI Helper shell',
    body: 'Open the floating helper to show page-aware guidance and future research mode boundaries.',
    href: '/platform-preview',
  },
  {
    title: '9. End with Platform Preview',
    label: 'Roadmap',
    body: 'Show future modules, compliance/data gates, and what must be validated before launch.',
    href: '/platform-preview',
  },
];

const validationGates = [
  'JSE data rights / API authorization',
  'FSC/legal review for public claims and advice boundaries',
  'Broker referral and account-opening rules',
  'Research hosting and source-use permissions',
  'User profile privacy and database design',
  'AI Helper grounding, search citations, and safety evaluation',
  'Sponsored content and monetization disclosures',
];

export default function DemoPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Demo Mode</span>
        <h1>Advisor walkthrough for the current platform.</h1>
        <p>{DEMO_MODE_MESSAGE}</p>
      </section>

      <section className="grid">
        <InfoCard title="What is working" label="Current product">
          <p>
            The Vercel frontend, Render FastAPI backend, market-first homepage, Market Pulse,
            Companies, Tools, Portfolio Plan, Ticker Analysis, Decision Audit, and AI Helper shell are
            working product surfaces.
          </p>
        </InfoCard>
        <InfoCard title="What is demo/internal" label="Data status">
          <p>
            Current market views should be treated as demo/internal or transformed historical data for
            product demonstration until official JSE data rights and API access are confirmed.
          </p>
        </InfoCard>
        <InfoCard title="What this is not" label="Boundary">
          <p>
            This is not financial advice, not an official live JSE data feed, not broker/dealer
            activity, not a broker referral engine, and not a live trading system.
          </p>
        </InfoCard>
      </section>

      <section className="hero compact">
        <span className="eyebrow">Advisor demo flow</span>
        <h2>Suggested walkthrough order</h2>
        <p>
          Use this order when showing the product to an advisor, partner, tester, potential user,
          school, institution, or grant/program reviewer.
        </p>
      </section>

      <section className="grid">
        {walkthroughSteps.map((step) => (
          <InfoCard key={step.title} title={step.title} label={step.label}>
            <p>{step.body}</p>
            <Link href={step.href}>Open</Link>
          </InfoCard>
        ))}
      </section>

      <section className="grid two">
        <InfoCard title="Demo surfaces" label="Can be shown">
          <div className="list-stack">
            {demoSurfaces.map((surface) => (
              <p key={surface}>{surface}</p>
            ))}
          </div>
        </InfoCard>
        <InfoCard title="Not live yet" label="Gated">
          <div className="list-stack">
            {notYetLive.map((item) => (
              <p key={item}>{item}</p>
            ))}
          </div>
        </InfoCard>
      </section>

      <section className="grid two">
        <InfoCard title="Validation gates" label="Before broader launch">
          <div className="list-stack">
            {validationGates.map((gate) => (
              <p key={gate}>{gate}</p>
            ))}
          </div>
        </InfoCard>
        <InfoCard title="How to describe the demo" label="Safe language">
          <p>
            This is a demo-safe market intelligence and decision-support platform for Jamaican,
            Caribbean, and diaspora investors. It shows product workflow, education, research entry,
            and planning support without giving personal investment advice or executing trades.
          </p>
        </InfoCard>
      </section>

      <div className="notice warning">
        <p>
          Before public launch or monetization, JSE Market Lab still needs validation around data
          rights, research hosting, broker access flows, sponsored content, paid products, and
          AI-assisted explanations.
        </p>
      </div>

      <div className="button-row">
        <Link className="button" href="/market">
          Start Demo Flow
        </Link>
        <Link className="button secondary" href="/tools">
          Open Tools Hub
        </Link>
        <Link className="button secondary" href="/platform-preview">
          Open Platform Preview
        </Link>
      </div>
    </div>
  );
}
