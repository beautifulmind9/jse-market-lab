import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const sections = [
  {
    title: 'Market Pulse',
    label: 'Preview',
    body: 'A future weekly view of broad market context, unusual movement, liquidity watch areas, and data-quality notes.',
  },
  {
    title: 'Signals overview',
    label: 'Future surface',
    body: 'A future summary of recent signal activity by quality tier, holding window, liquidity, and risk context.',
  },
  {
    title: 'Liquidity watch',
    label: 'Future surface',
    body: 'A future market-reality view for spotting thin trading, spread risk, and stocks that may be difficult to enter or exit.',
  },
];

export default function MarketPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Market</span>
        <h1>See the broader market context before drilling into one ticker.</h1>
        <p>
          Market views will help users understand what is happening across the JSE before reviewing a
          company, setup, or portfolio plan.
        </p>
      </section>

      <section className="grid">
        {sections.map((section) => (
          <InfoCard key={section.title} title={section.title} label={section.label}>
            <p>{section.body}</p>
          </InfoCard>
        ))}
      </section>

      <div className="button-row">
        <Link className="button" href="/ticker/JMMBGL">
          Review sample ticker
        </Link>
        <Link className="button secondary" href="/platform-preview">
          See future market modules
        </Link>
      </div>
    </div>
  );
}
