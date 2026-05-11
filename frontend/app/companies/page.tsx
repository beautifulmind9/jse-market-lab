import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const modules = [
  {
    title: 'Company Pages',
    label: 'Future anchor',
    body: 'Company pages will combine ticker analysis, company context, dividend notes, earnings context, and tradability review.',
  },
  {
    title: 'Ticker Analysis',
    label: 'Working surface',
    body: 'Use the current ticker page to review quick take, holding windows, risk context, and what to watch.',
  },
  {
    title: 'Earnings and tradability',
    label: 'Future context',
    body: 'Future company views will add earnings scorecards and float/tradability context where data is available and rights are clear.',
  },
];

export default function CompaniesPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Companies</span>
        <h1>Research one company at a time.</h1>
        <p>
          Company pages will become the main place to connect market data, dashboard signals, dividend
          context, earnings context, and research notes for a single ticker.
        </p>
      </section>

      <section className="grid">
        {modules.map((module) => (
          <InfoCard key={module.title} title={module.title} label={module.label}>
            <p>{module.body}</p>
          </InfoCard>
        ))}
      </section>

      <div className="button-row">
        <Link className="button" href="/ticker/JMMBGL">
          Open sample ticker
        </Link>
        <Link className="button secondary" href="/research">
          View research direction
        </Link>
      </div>
    </div>
  );
}
