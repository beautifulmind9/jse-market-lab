import { InfoCard } from '@/components/shared/InfoCard';
import { MetricRow } from '@/components/shared/MetricRow';
import { getPortfolioPlan } from '@/lib/api';
import { formatJmd, formatPercent } from '@/lib/formatters';
import type { Trade } from '@/lib/types';

const DEFAULT_CAPITAL = 100000;
const DEFAULT_COST_PROFILE = 'conservative_estimate';

function TradeCard({ trade, label }: { trade: Trade; label: string }) {
  return (
    <InfoCard title={trade.ticker} label={label}>
      <p>{trade.company_name}</p>
      <MetricRow label="Tier" value={trade.tier} />
      <MetricRow label="Holding window" value={trade.holding_window} />
      <MetricRow label="Allocation" value={formatJmd(trade.allocation_amount)} />
      <MetricRow label="Allocation share" value={formatPercent(trade.allocation_pct)} />
      <MetricRow label="Liquidity" value={trade.liquidity_status} />
      <p>{trade.reason}</p>
    </InfoCard>
  );
}

export default async function PortfolioPage() {
  let plan;
  let error: string | null = null;

  try {
    plan = await getPortfolioPlan(DEFAULT_CAPITAL, 'guided', DEFAULT_COST_PROFILE);
  } catch {
    error = 'Portfolio plan data is not available right now. Please try again after the API is reachable.';
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Portfolio Plan</span>
        <h1>Review a sample capital plan.</h1>
        <p>
          This page uses the hosted FastAPI backend to show funded trades, unfunded trades, reserve
          cash, and rule-based explanations for a sample {formatJmd(DEFAULT_CAPITAL)} guided plan.
        </p>
      </section>

      {error || !plan ? (
        <section className="grid">
          <InfoCard title="Portfolio data unavailable" label="API status">
            <p>{error}</p>
          </InfoCard>
        </section>
      ) : (
        <>
          <section className="grid">
            <InfoCard title="Funded setups" label="Summary">
              <MetricRow label="Funded for review" value={plan.summary.funded_count} />
              <MetricRow label="Total allocated" value={formatJmd(plan.summary.total_allocated)} />
            </InfoCard>
            <InfoCard title="Cash reserve" label="Risk control">
              <MetricRow label="Unallocated cash" value={formatJmd(plan.reserve_cash)} />
              <p>Reserve cash is part of the plan when not enough setups meet the rules.</p>
            </InfoCard>
            <InfoCard title="Cost assumptions" label="Estimate">
              <MetricRow label="Profile" value={plan.cost_profile.label} />
              <MetricRow label="Service charge" value={formatPercent(plan.cost_profile.broker_fee)} />
              <MetricRow label="Market charge" value={formatPercent(plan.cost_profile.cess)} />
              <p>{plan.cost_profile.note}</p>
            </InfoCard>
          </section>

          <div className="notice">
            <p>{plan.disclaimer}</p>
          </div>

          <div className="notice warning">
            <p>{plan.cost_profile.disclaimer}</p>
          </div>

          <section className="hero compact">
            <span className="eyebrow">Funded for review</span>
            <h2>Top funded setups</h2>
          </section>
          <section className="grid">
            {plan.funded_trades.slice(0, 6).map((trade) => (
              <TradeCard key={trade.ticker} trade={trade} label="Funded" />
            ))}
          </section>

          <section className="hero compact">
            <span className="eyebrow">Not funded</span>
            <h2>Held back by rules</h2>
          </section>
          <section className="grid">
            {plan.unfunded_trades.slice(0, 6).map((trade) => (
              <TradeCard key={trade.ticker} trade={trade} label="Not funded" />
            ))}
          </section>
        </>
      )}
    </div>
  );
}
