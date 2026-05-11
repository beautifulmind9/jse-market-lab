import Link from 'next/link';
import { ApiStatusCard } from '@/components/shared/ApiStatusCard';
import { HomeMarketSnapshot } from '@/components/shared/HomeMarketSnapshot';
import { InfoCard } from '@/components/shared/InfoCard';

const intentCards = [
  {
    title: 'Learn how the JSE works',
    label: 'Learn',
    body: 'Start with plain-language education on market basics, liquidity, costs, dividends, and responsible decision support.',
    href: '/learn',
  },
  {
    title: 'See what is happening in the market',
    label: 'Market',
    body: 'Use market context to understand broad activity before drilling into one ticker or setup.',
    href: '/market',
  },
  {
    title: 'Research a company',
    label: 'Companies',
    body: 'Start from a company or ticker and connect signals, dividend context, earnings context, and tradability notes over time.',
    href: '/companies',
  },
  {
    title: 'Plan or test a setup',
    label: 'Tools',
    body: 'Use Portfolio Plan, Ticker Analysis, and Decision Audit to review setups with structure. Simulation tools are future work.',
    href: '/tools',
  },
  {
    title: 'Track dividend and income context',
    label: 'Income',
    body: 'Review the future income-focused direction for dividend context, company income profiles, and portfolio income planning.',
    href: '/income',
  },
  {
    title: 'View the product demo',
    label: 'Demo',
    body: 'Use Demo Mode and Platform Preview for advisor, partner, and stakeholder walkthroughs before official data/API authorization.',
    href: '/demo',
  },
];

export default function HomePage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Decision support and market intelligence for the JSE</span>
        <h1>Start with the market, then choose your path.</h1>
        <p>
          JSE Market Lab helps Jamaican, Caribbean, and diaspora investors see market context, learn,
          research companies, and use structured tools before making their own decisions.
        </p>
        <div className="button-row">
          <Link className="button" href="/tools">
            Open Tools
          </Link>
          <Link className="button secondary" href="/companies">
            Research Companies
          </Link>
          <Link className="button secondary" href="/demo">
            View Demo
          </Link>
        </div>
      </section>

      <HomeMarketSnapshot />

      <section className="hero compact">
        <span className="eyebrow">Choose your path</span>
        <h2>What are you trying to do today?</h2>
      </section>

      <section className="grid">
        <ApiStatusCard />
        {intentCards.map((card) => (
          <InfoCard key={card.title} title={card.title} label={card.label}>
            <p>{card.body}</p>
            <Link href={card.href}>Start here</Link>
          </InfoCard>
        ))}
      </section>

      <div className="notice">
        <p>
          JSE Market Lab is a decision-support platform. It helps users review information, risks,
          costs, and context. It does not provide personal investment advice, execute trades, or hold
          client funds.
        </p>
      </div>
    </div>
  );
}
