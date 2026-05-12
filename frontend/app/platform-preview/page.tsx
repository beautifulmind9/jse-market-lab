import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';
import { DEMO_MODE_MESSAGE } from '@/lib/demoMode';

const builtSurfaces = [
  {
    title: 'Market-first homepage',
    label: 'Working surface',
    body: 'The homepage now opens with market context before routing users into learning, research, tools, income, and demo paths.',
    href: '/',
  },
  {
    title: 'Market Pulse',
    label: 'Working demo surface',
    body: 'A demo-safe market-intelligence page with market tape, movers mockup, signal clusters, liquidity watch, and market notes.',
    href: '/market',
  },
  {
    title: 'Companies',
    label: 'Working demo surface',
    body: 'A company research entry point with sample company cards, ticker-analysis links, and future company-page module previews.',
    href: '/companies',
  },
  {
    title: 'Tools',
    label: 'Working surface',
    body: 'A decision-support hub that links Portfolio Plan, Ticker Analysis, Decision Audit, and future simulation concepts.',
    href: '/tools',
  },
  {
    title: 'AI Helper shell',
    label: 'Working shell',
    body: 'A persistent Guide Me panel with page-aware guidance. It is rule-based for now and does not make live AI or web-search calls yet.',
    href: '/demo',
  },
];

const futureModules = [
  {
    title: 'Research Hub',
    label: 'Future / compliance-gated',
    body: 'A structured place to discover company research, market notes, source links, and saved reports once rights and hosting rules are validated.',
  },
  {
    title: 'Full Company Pages',
    label: 'Future expansion',
    body: 'Ticker-centered pages that combine company context, dashboard signals, dividend profile, earnings context, and tradability notes.',
  },
  {
    title: 'Dividend View',
    label: 'Future income layer',
    body: 'A focused view for income-oriented investors to track dividend notices, yield context, payment timing, and company patterns.',
  },
  {
    title: 'Earnings Scorecard',
    label: 'Future research layer',
    body: 'A research layer to help users review earnings events, company performance context, and post-result market behavior.',
  },
  {
    title: 'Float / Tradability View',
    label: 'Future market reality layer',
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
    title: 'AI Research Mode',
    label: 'Future assistant layer',
    body: 'A search-enabled AI Helper mode for public-source research with citations, source dates, and clear advice boundaries.',
  },
  {
    title: 'Brokerage Access Education',
    label: 'Future / compliance-gated',
    body: 'A neutral education flow explaining account-opening considerations, broker-fee checks, and investor responsibilities after validation.',
  },
];

const gates = [
  'Official JSE data rights / API access',
  'Research hosting and source-use rules',
  'Broker referral and account-opening boundaries',
  'User profile privacy and database design',
  'AI Helper grounding, web-search citations, and evaluation tests',
  'Sponsored content and monetization disclosures',
  'Public brand name and JSE attribution approach',
];

export default function PlatformPreviewPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Platform Preview</span>
        <h1>What is built now, and what comes next.</h1>
        <p>
          This page separates working demo-safe surfaces from future platform modules. It should help
          advisors, partners, testers, and reviewers understand the current product without confusing
          demo/internal data for official live JSE data.
        </p>
      </section>

      <div className="notice warning">
        <p>{DEMO_MODE_MESSAGE}</p>
      </div>

      <section className="hero compact">
        <span className="eyebrow">Built now</span>
        <h2>Current demo-safe platform surfaces</h2>
      </section>

      <section className="grid">
        {builtSurfaces.map((surface) => (
          <InfoCard key={surface.title} title={surface.title} label={surface.label}>
            <p>{surface.body}</p>
            <Link href={surface.href}>Open</Link>
          </InfoCard>
        ))}
      </section>

      <section className="hero compact">
        <span className="eyebrow">Future modules</span>
        <h2>Product direction after validation and data foundations</h2>
      </section>

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
          These items need validation before future surfaces become public product features or revenue
          channels.
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
            The current demo can show the market-first product experience, decision-support workflow,
            company research entry point, Tools hub, API-backed core dashboard pages, and AI Helper
            shell. It should not imply official live JSE data, broker approval, personal investment
            advice, or production research coverage.
          </p>
        </InfoCard>
      </section>

      <div className="button-row">
        <Link className="button" href="/demo">
          View Demo Walkthrough
        </Link>
        <Link className="button secondary" href="/market">
          Start at Market Pulse
        </Link>
        <Link className="button secondary" href="/tools">
          Open Tools Hub
        </Link>
      </div>
    </div>
  );
}
