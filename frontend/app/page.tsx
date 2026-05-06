import Link from 'next/link';
import { ApiStatusCard } from '@/components/shared/ApiStatusCard';
import { InfoCard } from '@/components/shared/InfoCard';

export default function HomePage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Decision support for the JSE</span>
        <h1>Understand the setup before you decide what to do.</h1>
        <p>
          JSE Market Lab helps Jamaican investors review opportunities with structure: signal context,
          quality tiers, liquidity checks, holding windows, and portfolio rules.
        </p>
        <div className="button-row">
          <Link className="button" href="/portfolio">
            View Portfolio Plan
          </Link>
          <Link className="button secondary" href="/ticker/JMMBGL">
            Start with a ticker
          </Link>
        </div>
      </section>

      <section className="grid">
        <ApiStatusCard />
        <InfoCard title="Plan with structure" label="Portfolio">
          <p>
            Enter capital, review funded and unfunded setups, and keep reserve cash visible when the
            system does not find enough fundable opportunities.
          </p>
        </InfoCard>
        <InfoCard title="Learn one ticker at a time" label="Ticker">
          <p>
            Use ticker analysis to see quick takes, holding-window behavior, risk context, and what to
            watch before acting.
          </p>
        </InfoCard>
        <InfoCard title="Review the rules" label="Audit">
          <p>
            The review layer explains how ranking, quality, liquidity, and allocation rules shaped the
            plan. It supports discipline, not blind action.
          </p>
        </InfoCard>
      </section>
    </div>
  );
}
