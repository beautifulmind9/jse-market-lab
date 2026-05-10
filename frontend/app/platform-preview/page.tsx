import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';
import { DEMO_MODE_MESSAGE } from '@/lib/demoMode';

const futureModules = [
  {
    title: 'Research Hub',
    label: 'Future surface',
    body: 'A structured place to discover company research, market notes, source links, and saved reports once rights and hosting rules are validated.',
  },
  {
    title: 'Company Pages',
    label: 'Future surface',
    body: 'Ticker-centered pages that combine company context, dashboard signals, dividend profile, earnings context, and tradability notes.',
  },
  {
    title: 'Market Pulse',
    label: 'Future surface',
    body: 'A weekly market overview showing broad observations, unusual movement, liquidity warnings, and data-quality notes.',
  },
  {
    title: 'Dividend View',
    label: 'Future surface',
    body: 'A focused view for income-oriented investors to track dividend notices, yield context, payment timing, and company patterns.',
  },
  {
    title: 'Earnings Scorecard',
    label: 'Future surface',
    body: 'A research layer to help users review earnings events, company performance context, and post-result market behavior.',
  },
  {
    title: 'Float / Tradability View',
    label: 'Future surface',
    body: 'A market-reality layer to help users understand whether a stock may be difficult to enter or exit because of float, volume, or liquidity.',
  },
  {
    title: 'Setup Tester',
    label: 'Future simulation',
    body: 'A safe testing workflow where users can test an idea using historical market data without executing a trade or receiving advice.',
  },
  {
    title: 'Paper Portfolio',
    label: 'Future simulation',
    body: 'A practice portfolio for tracking simulated positions, planned review dates, outcome review, and lessons learned.',
  },
  {
    title: 'AI Helper',
    label: 'Future assistant',
    body: 'A grounded guide to help users navigate the platform, understand outputs, and review next steps without recommending trades.',
  },
];

const gates = [
  'Official JSE data rights / API access',
  'Research hosting and source-use rules',
  'Broker referral and account-opening boundaries',
  'User profile privacy and database design',
  'AI helper grounding and evaluation tests',
  'Sponsored content and monetization disclosures',
];

export default function PlatformPreviewPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Platform Preview</span>
        <h1>Where JSE Market Lab is going next.</h1>
        <p>
          This page shows future platform modules as mockups and product direction. These surfaces are
          not fully launched features yet.
        </p>
      </section>

      <div className="notice warning">
        <p>{DEMO_MODE_MESSAGE}</p>
      </div>

      <section className="grid">
        {futureModules.map((module) => (
          <InfoCard key={module.title} title={module.title} label={module.label}>
            <p>{module.body}</p>
          </InfoCard>
        ))}
      </section>

      <section className="hero compact">
        <span className="eyebrow">Before these go live</span>
        <h2>Compliance and data gates</h2>
        <p>
          These items need validation before the preview surfaces become public product features.
        </p>
      </section>

      <section className="grid two">
        <InfoCard title="What must be validated" label="Gates">
          <div className="list-stack">
            {gates.map((gate) => (
              <p key={gate}>{gate}</p>
            ))}
          </div>
        </InfoCard>
        <InfoCard title="What can be shown now" label="Demo-safe">
          <p>
            The current demo can show the platform vision, decision-support workflow, API-backed core
            dashboard pages, and future module concepts. It should not imply official live JSE data,
            broker approval, or investment advice.
          </p>
        </InfoCard>
      </section>

      <div className="button-row">
        <Link className="button" href="/demo">
          View Demo Mode Guide
        </Link>
        <Link className="button secondary" href="/portfolio">
          Back to Portfolio Plan
        </Link>
      </div>
    </div>
  );
}
