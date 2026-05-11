import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const topics = [
  {
    title: 'JSE basics',
    body: 'Start with how stocks trade in Jamaica, what brokers do, and how to read basic market information.',
  },
  {
    title: 'Holding windows',
    body: 'Learn why the platform compares 5D, 10D, 20D, and 30D outcomes instead of treating every setup the same.',
  },
  {
    title: 'Liquidity and spreads',
    body: 'Understand why volume, entry/exit difficulty, and spread widening matter in the Jamaican market.',
  },
  {
    title: 'Trading costs',
    body: 'See how estimated charges can affect net returns and why fees should be confirmed with a licensed broker.',
  },
  {
    title: 'Dividends',
    body: 'Learn how dividend history, timing, and income context can support longer-term investor review.',
  },
  {
    title: 'Decision support',
    body: 'Understand what the dashboard can and cannot do. The platform supports review, not blind action.',
  },
];

export default function LearnPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Learn</span>
        <h1>Build your JSE foundation before using the tools.</h1>
        <p>
          Start here if you want plain-language education on the Jamaican market, trading costs,
          liquidity, holding windows, dividends, and decision-support basics.
        </p>
      </section>

      <section className="grid">
        {topics.map((topic) => (
          <InfoCard key={topic.title} title={topic.title} label="Education">
            <p>{topic.body}</p>
          </InfoCard>
        ))}
      </section>

      <div className="button-row">
        <Link className="button" href="/ticker/JMMBGL">
          Try a sample ticker
        </Link>
        <Link className="button secondary" href="/tools">
          View planning tools
        </Link>
      </div>
    </div>
  );
}
