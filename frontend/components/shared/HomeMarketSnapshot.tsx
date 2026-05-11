import Link from 'next/link';
import { getDataStatus, getPortfolioPlan } from '@/lib/api';
import { formatJmd, formatPercent } from '@/lib/formatters';

const SNAPSHOT_CAPITAL = 100000;

export async function HomeMarketSnapshot() {
  let status;
  let plan;
  let unavailable = false;

  try {
    [status, plan] = await Promise.all([
      getDataStatus(),
      getPortfolioPlan(SNAPSHOT_CAPITAL, 'guided', 'conservative_estimate'),
    ]);
  } catch {
    unavailable = true;
  }

  if (unavailable || !status || !plan) {
    return (
      <section className="market-snapshot">
        <div>
          <span className="eyebrow">Demo Market Snapshot</span>
          <h2>Market snapshot unavailable</h2>
          <p>
            The homepage snapshot could not reach the API right now. The platform pages are still
            available for navigation and demo review.
          </p>
        </div>
        <div className="snapshot-card">
          <span>Mode</span>
          <strong>Demo / internal data</strong>
          <p>Not an official live JSE feed.</p>
        </div>
      </section>
    );
  }

  const funded = plan.funded_trades.slice(0, 3);
  const unfundedCount = plan.summary.unfunded_count;

  return (
    <section className="market-snapshot">
      <div className="snapshot-lead">
        <span className="eyebrow">Demo Market Snapshot</span>
        <h2>Latest available market view</h2>
        <p>
          A live-looking homepage preview using the current internal dataset. This demonstrates the
          market-intelligence experience and is not an official live JSE feed.
        </p>
      </div>

      <div className="snapshot-grid">
        <div className="snapshot-card">
          <span>Market mode</span>
          <strong>Demo / internal</strong>
          <p>Latest available prepared dataset.</p>
        </div>
        <div className="snapshot-card">
          <span>Latest market date</span>
          <strong>{status.latest_market_date || 'Not available'}</strong>
          <p>{status.dataset_source}</p>
        </div>
        <div className="snapshot-card">
          <span>Rows loaded</span>
          <strong>{status.row_count.toLocaleString()}</strong>
          <p>Used for demo analysis and routing.</p>
        </div>
        <div className="snapshot-card">
          <span>Sample capital plan</span>
          <strong>{formatJmd(plan.summary.total_allocated)}</strong>
          <p>{formatJmd(plan.reserve_cash)} held as reserve.</p>
        </div>
      </div>

      <div className="snapshot-strip">
        <div>
          <span className="snapshot-label">Top funded demo setups</span>
          <div className="snapshot-tickers">
            {funded.map((trade) => (
              <Link key={trade.ticker} href={'/ticker/' + encodeURIComponent(trade.ticker)}>
                {trade.ticker} · {trade.holding_window} · {formatPercent(trade.allocation_pct)}
              </Link>
            ))}
          </div>
        </div>
        <div>
          <span className="snapshot-label">Watch areas</span>
          <p>
            {unfundedCount} setups held back by rules. Review liquidity, cost assumptions, and data
            status before interpreting outputs.
          </p>
        </div>
      </div>
    </section>
  );
}
