import Link from 'next/link';
import { getDataStatus, getPortfolioPlan } from '@/lib/api';
import { formatJmd, formatPercent } from '@/lib/formatters';

const SNAPSHOT_CAPITAL = 100000;

const demoFallback = {
  latestMarketDate: 'Latest available demo date',
  datasetSource: 'Demo/internal market dataset',
  rowsLoaded: '57,656+',
  allocated: '$70,000',
  reserve: '$30,000',
  tickers: [
    { ticker: 'JPS9.5', label: '5D · 30%' },
    { ticker: 'WIPT', label: '30D · 30%' },
    { ticker: 'TJH8.0', label: '5D · 10%' },
  ],
};

function DemoFallbackSnapshot() {
  return (
    <section className="market-snapshot">
      <div className="snapshot-lead">
        <span className="eyebrow">Demo Market Snapshot</span>
        <h2>Latest available market view</h2>
        <p>
          A live-looking homepage preview using demo/internal market data. This keeps the walkthrough
          useful even when the API is waking up or temporarily unreachable.
        </p>
      </div>

      <div className="snapshot-grid">
        <div className="snapshot-card">
          <span>Market mode</span>
          <strong>Demo / internal</strong>
          <p>Not an official live JSE feed.</p>
        </div>
        <div className="snapshot-card">
          <span>Latest market date</span>
          <strong>{demoFallback.latestMarketDate}</strong>
          <p>{demoFallback.datasetSource}</p>
        </div>
        <div className="snapshot-card">
          <span>Rows loaded</span>
          <strong>{demoFallback.rowsLoaded}</strong>
          <p>Sample dataset for product demonstration.</p>
        </div>
        <div className="snapshot-card">
          <span>Sample capital plan</span>
          <strong>{demoFallback.allocated}</strong>
          <p>{demoFallback.reserve} held as reserve.</p>
        </div>
      </div>

      <div className="snapshot-strip">
        <div>
          <span className="snapshot-label">Demo setup examples</span>
          <div className="snapshot-tickers">
            {demoFallback.tickers.map((item) => (
              <Link key={item.ticker} href={'/ticker/' + encodeURIComponent(item.ticker)}>
                {item.ticker} · {item.label}
              </Link>
            ))}
          </div>
        </div>
        <div>
          <span className="snapshot-label">Watch areas</span>
          <p>
            Review liquidity, cost assumptions, data status, and holding-window behavior before
            interpreting any output.
          </p>
        </div>
      </div>
    </section>
  );
}

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
    return <DemoFallbackSnapshot />;
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
