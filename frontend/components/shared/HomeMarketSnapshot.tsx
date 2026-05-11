import Link from 'next/link';
import { getDataStatus, getPortfolioPlan, hasConfiguredApiBaseUrl } from '@/lib/api';
import { formatJmd, formatPercent } from '@/lib/formatters';
import type { PortfolioPlan, Trade } from '@/lib/types';

const SNAPSHOT_CAPITAL = 100000;

const demoFallback = {
  latestMarketDate: '2026-04-24',
  datasetSource: 'Demo/internal market dataset',
  rowsLoaded: '57,656+',
  allocated: '$70,000',
  reserve: '$30,000',
  unfundedCount: 6,
  tickers: [
    { ticker: 'JPS9.5', window: '5D', tier: 'A', allocation: '30%' },
    { ticker: 'WIPT', window: '30D', tier: 'A', allocation: '30%' },
    { ticker: 'TJH8.0', window: '5D', tier: 'A', allocation: '10%' },
  ],
};

function MarketTape({ rowsLoaded, latestDate }: { rowsLoaded: string; latestDate: string }) {
  const tape = [
    { label: 'JSE LAB MODE', value: 'DEMO', tone: 'neutral' },
    { label: 'LATEST DATA', value: latestDate, tone: 'neutral' },
    { label: 'ROWS', value: rowsLoaded, tone: 'neutral' },
    { label: 'FEED', value: 'INTERNAL', tone: 'neutral' },
    { label: 'STATUS', value: 'NOT LIVE JSE', tone: 'warn' },
  ];

  return (
    <div className="market-tape" aria-label="Demo market status tape">
      {tape.map((item) => (
        <div key={item.label} className={'tape-item ' + item.tone}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
        </div>
      ))}
    </div>
  );
}

function SetupRows({ trades }: { trades: Array<Pick<Trade, 'ticker' | 'holding_window' | 'tier' | 'allocation_pct'>> }) {
  return (
    <div className="market-table">
      <div className="market-table-head">
        <span>Ticker</span>
        <span>Tier</span>
        <span>Window</span>
        <span>Allocation</span>
      </div>
      {trades.map((trade) => (
        <Link className="market-table-row" key={trade.ticker} href={'/ticker/' + encodeURIComponent(trade.ticker)}>
          <strong>{trade.ticker}</strong>
          <span>{trade.tier || '—'}</span>
          <span>{trade.holding_window || '—'}</span>
          <span>{formatPercent(trade.allocation_pct)}</span>
        </Link>
      ))}
    </div>
  );
}

function DemoSetupRows() {
  return (
    <div className="market-table">
      <div className="market-table-head">
        <span>Ticker</span>
        <span>Tier</span>
        <span>Window</span>
        <span>Allocation</span>
      </div>
      {demoFallback.tickers.map((trade) => (
        <Link className="market-table-row" key={trade.ticker} href={'/ticker/' + encodeURIComponent(trade.ticker)}>
          <strong>{trade.ticker}</strong>
          <span>{trade.tier}</span>
          <span>{trade.window}</span>
          <span>{trade.allocation}</span>
        </Link>
      ))}
    </div>
  );
}

function MarketFrontPage({
  latestDate,
  datasetSource,
  rowsLoaded,
  allocated,
  reserve,
  unfundedCount,
  plan,
}: {
  latestDate: string;
  datasetSource: string;
  rowsLoaded: string;
  allocated: string;
  reserve: string;
  unfundedCount: number;
  plan?: PortfolioPlan;
}) {
  const funded = plan?.funded_trades.slice(0, 3) ?? [];

  return (
    <section className="market-front">
      <MarketTape rowsLoaded={rowsLoaded} latestDate={latestDate} />

      <div className="market-front-grid">
        <div className="market-lede-panel">
          <span className="eyebrow">Demo Market Snapshot</span>
          <h2>Latest available JSE market view</h2>
          <p>
            Demo/internal data shaped into a market-front page experience. This is not an official live
            JSE feed.
          </p>
          <div className="market-lede-actions">
            <Link href="/market">Market</Link>
            <Link href="/companies">Companies</Link>
            <Link href="/tools">Tools</Link>
          </div>
        </div>

        <div className="quote-panel">
          <div className="quote-panel-header">
            <span>Snapshot Board</span>
            <strong>DEMO</strong>
          </div>
          <div className="quote-metrics">
            <div>
              <span>Sample allocated</span>
              <strong>{allocated}</strong>
            </div>
            <div>
              <span>Reserve cash</span>
              <strong>{reserve}</strong>
            </div>
            <div>
              <span>Held back</span>
              <strong>{unfundedCount}</strong>
            </div>
          </div>
        </div>
      </div>

      <div className="market-content-grid">
        <div className="market-module wide">
          <div className="module-heading">
            <h3>Top demo setups</h3>
            <Link href="/portfolio">View portfolio plan</Link>
          </div>
          {funded.length > 0 ? <SetupRows trades={funded} /> : <DemoSetupRows />}
        </div>

        <div className="market-module">
          <div className="module-heading">
            <h3>Market notes</h3>
            <Link href="/demo">Demo mode</Link>
          </div>
          <ul className="market-news-list">
            <li>Latest available dataset: {latestDate}</li>
            <li>Source: {datasetSource}</li>
            <li>Cost assumptions and liquidity checks are active.</li>
            <li>Official live feed requires JSE/data-rights validation.</li>
          </ul>
        </div>
      </div>
    </section>
  );
}

function renderDemoFallback() {
  return (
    <MarketFrontPage
      latestDate={demoFallback.latestMarketDate}
      datasetSource={demoFallback.datasetSource}
      rowsLoaded={demoFallback.rowsLoaded}
      allocated={demoFallback.allocated}
      reserve={demoFallback.reserve}
      unfundedCount={demoFallback.unfundedCount}
    />
  );
}

export async function HomeMarketSnapshot() {
  if (!hasConfiguredApiBaseUrl()) {
    return renderDemoFallback();
  }

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
    return renderDemoFallback();
  }

  return (
    <MarketFrontPage
      latestDate={status.latest_market_date || 'Not available'}
      datasetSource={status.dataset_source}
      rowsLoaded={status.row_count.toLocaleString()}
      allocated={formatJmd(plan.summary.total_allocated)}
      reserve={formatJmd(plan.reserve_cash)}
      unfundedCount={plan.summary.unfunded_count}
      plan={plan}
    />
  );
}
