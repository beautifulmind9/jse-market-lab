import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const incomeModules = [
  {
    title: 'Dividend View',
    label: 'Future surface',
    body: 'A future income-focused view for dividend notices, payment timing, yield context, and company dividend patterns.',
  },
  {
    title: 'Company income profile',
    label: 'Future company context',
    body: 'A future company-level view connecting dividend history, earnings context, and risk notes for income investors.',
  },
  {
    title: 'Portfolio income estimate',
    label: 'Future planning',
    body: 'A future estimate layer for simulated portfolio income. Dividend history will not be treated as a guarantee.',
  },
];

export default function IncomePage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Income</span>
        <h1>Track dividend and income context with risk in view.</h1>
        <p>
          Income tools will help dividend-focused users review distributions, timing, company context,
          and portfolio implications without implying that past dividends guarantee future income.
        </p>
      </section>

      <section className="grid">
        {incomeModules.map((module) => (
          <InfoCard key={module.title} title={module.title} label={module.label}>
            <p>{module.body}</p>
          </InfoCard>
        ))}
      </section>

      <div className="button-row">
        <Link className="button" href="/companies">
          Research companies
        </Link>
        <Link className="button secondary" href="/platform-preview">
          View income roadmap
        </Link>
      </div>
    </div>
  );
}
