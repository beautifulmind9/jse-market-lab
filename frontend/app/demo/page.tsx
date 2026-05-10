import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';
import { DEMO_MODE_MESSAGE } from '@/lib/demoMode';

const demoSurfaces = [
  'Portfolio Plan',
  'Ticker Analysis',
  'Decision Audit',
  'Platform Preview',
  'Company Pages concept',
  'Market Pulse concept',
  'Research Hub concept',
  'Setup Tester concept',
  'AI Helper concept',
];

const notYetLive = [
  'Official JSE API integration',
  'Broker referral routing',
  'Trade execution',
  'User accounts or saved portfolios',
  'Paid research or sponsored placements',
  'Public AI helper responses',
];

export default function DemoPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Demo Mode</span>
        <h1>What this demo is showing.</h1>
        <p>{DEMO_MODE_MESSAGE}</p>
      </section>

      <section className="grid">
        <InfoCard title="What is real" label="Working product">
          <p>
            The Vercel frontend, Render FastAPI backend, and API-backed Portfolio, Ticker Analysis,
            and Decision Audit pages are working product surfaces.
          </p>
        </InfoCard>
        <InfoCard title="What is sample/demo" label="Data status">
          <p>
            The current market data should be treated as internal sample or transformed historical data
            for demonstration until official data rights and API access are confirmed.
          </p>
        </InfoCard>
        <InfoCard title="What this is not" label="Boundary">
          <p>
            This is not financial advice, not an official JSE data feed, not broker/dealer activity, and
            not a live trading system.
          </p>
        </InfoCard>
      </section>

      <section className="hero compact">
        <span className="eyebrow">Advisor demo flow</span>
        <h2>Suggested walkthrough</h2>
        <p>
          Use this order when showing the product to an advisor, partner, tester, or potential user.
        </p>
      </section>

      <section className="grid">
        <InfoCard title="1. Start Here" label="Context">
          <p>Explain the product: market intelligence and decision support for Jamaican investors.</p>
        </InfoCard>
        <InfoCard title="2. Portfolio Plan" label="Decision engine">
          <p>Show how capital, funded setups, unfunded setups, and reserve cash are structured.</p>
        </InfoCard>
        <InfoCard title="3. Ticker Analysis" label="Single-company view">
          <p>Open one ticker to show holding windows, risk context, and what to review.</p>
        </InfoCard>
        <InfoCard title="4. Decision Audit" label="Trust layer">
          <p>Explain why the plan looks the way it does and how the rules guide discipline.</p>
        </InfoCard>
        <InfoCard title="5. Platform Preview" label="Expansion">
          <p>Show Research Hub, Company Pages, Market Pulse, Setup Tester, and AI Helper concepts.</p>
        </InfoCard>
        <InfoCard title="6. Compliance path" label="Before launch">
          <p>Explain that JSE/FSC/legal validation is needed before official data, referrals, or monetization.</p>
        </InfoCard>
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

      <div className="notice warning">
        <p>
          Before public launch, JSE Market Lab still needs validation around data rights, research
          hosting, broker access flows, sponsored content, paid products, and AI-assisted explanations.
        </p>
      </div>

      <div className="button-row">
        <Link className="button" href="/portfolio">
          View Portfolio Plan
        </Link>
        <Link className="button secondary" href="/ticker/JMMBGL">
          Open Ticker Analysis
        </Link>
        <Link className="button secondary" href="/platform-preview">
          Open Platform Preview
        </Link>
      </div>
    </div>
  );
}
