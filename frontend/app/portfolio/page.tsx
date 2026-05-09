import { InfoCard } from '@/components/shared/InfoCard';
import { getPortfolioPlan } from '@/lib/api';
import { formatJmd, formatPercent } from '@/lib/formatters';
import type { Trade } from '@/lib/types';

const DEFAULT_CAPITAL = 100000;

function TradeCard({ trade, label }: { trade: Trade; label: string }) {
  return (
    <InfoCard title={trade.ticker} label={label}>
      <p>{trade.company_name}</p>
      <p>Tier: {trade.tier}</p>
      <p>Holding window: {trade.holding_window}</p>
      <p>Allocation: {formatJmd(trade.allocation_amount)} ({formatPercent(trade.allocation_pct)})</p>
      <p>Liquidity: {trade.liquidity_status}</p>
      <p>{trade.reason}</p>
    </InfoCard>
  );
}

export default async function PortfolioPage() {
  let plan;
  let error: string | null = null;

  try {
    plan = await getPortfolioPlan(DEFAULT_CAPITAL, 'guided');
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
              <p>{plan.summary.funded_count} setups funded for review.</p>
              <p>Total allocated: {formatJmd(plan.summary.total_allocated)}</p>
            </InfoCard>
            <InfoCard title="Cash reserve" label="Risk control">
              <p>{formatJmd(plan.reserve_cash)} remains unallocated.</p>
              <p>Reserve cash is part of the plan when not enough setups meet the rules.</p>
            </InfoCard>
            <InfoCard title="Unfunded setups" label="Discipline">
              <p>{plan.summary.unfunded_count} setups were not funded.</p>
              <p>Unfunded does not mean ignored. It means the rules held back capital.</p>
            </InfoCard>
          </section>

          <section className="hero">
            <span className="eyebrow">Funded for review</span>
            <h2>Top funded setups</h2>
          </section>
          <section className="grid">
            {plan.funded_trades.slice(0, 6).map((trade) => (
              <TradeCard key={trade.ticker} trade={trade} label="Funded" />
            ))}
          </section>

          <section className="hero">
            <span className="eyebrow">Not funded</span>
            <h2>Held back by rules</h2>
          </section>
          <section className="grid">
            {plan.unfunded_trades.slice(0, 6).map((trade) => (
              <TradeCard key={trade.ticker} trade={trade} label="Not funded" />
            ))}
          </section>

          <section className="hero">
            <p>{plan.disclaimer}</p>
          </section>
        </>
      )}
    </div>
  );
}
