import Link from 'next/link';

const marketTape = [
  { label: 'Market mode', value: 'Demo / internal' },
  { label: 'Latest data', value: '2026-04-24' },
  { label: 'Rows loaded', value: '57,656+' },
  { label: 'Feed status', value: 'Not live JSE', tone: 'warn' },
];

const movers = [
  { ticker: 'JPS9.5', window: '5D', tier: 'A', note: 'Funded in demo plan' },
  { ticker: 'WIPT', window: '30D', tier: 'A', note: 'Longer holding window' },
  { ticker: 'TJH8.0', window: '5D', tier: 'A', note: 'Smaller allocation' },
  { ticker: 'CAR', window: '30D', tier: 'B', note: 'Held back by rules' },
];

const liquidityWatch = [
  'Thin trading can affect entry and exit timing.',
  'Spread widening should be reviewed before interpreting short holding windows.',
  'Volume confirmation is a stronger signal-quality input than price movement alone.',
];

const signalClusters = [
  { label: 'Tier A setups', value: '3 demo funded' },
  { label: 'Tier B/C watch', value: 'Rule-dependent' },
  { label: 'Holding windows', value: '5D / 10D / 20D / 30D' },
  { label: 'Cost profile', value: 'Conservative estimate' },
];

const marketNotes = [
  'This page uses demo/internal data to show the intended Market Pulse experience.',
  'Official live market feed access requires JSE/data-rights validation.',
  'Market context should lead users into company research, tools, and review workflows.',
];

export default function MarketPage() {
  return (
    <div className="page-shell market-home-shell">
      <section className="market-front">
        <div className="market-tape" aria-label="Demo Market Pulse status tape">
          {marketTape.map((item) => (
            <div key={item.label} className={'tape-item ' + (item.tone || 'neutral')}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>

        <div className="market-front-grid">
          <div className="market-lede-panel">
            <span className="eyebrow">Demo Market Pulse</span>
            <h2>JSE market context, before the ticker deep dive.</h2>
            <p>
              A demo-safe market intelligence view for broad conditions, setup clusters, liquidity
              context, and data status. This is not an official live JSE feed.
            </p>
            <div className="market-lede-actions">
              <Link href="/companies">Companies</Link>
              <Link href="/tools">Tools</Link>
              <Link href="/demo">Demo</Link>
            </div>
          </div>

          <div className="quote-panel">
            <div className="quote-panel-header">
              <span>Pulse Board</span>
              <strong>DEMO</strong>
            </div>
            <div className="quote-metrics">
              {signalClusters.map((cluster) => (
                <div key={cluster.label}>
                  <span>{cluster.label}</span>
                  <strong>{cluster.value}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Market movers mockup</h3>
              <Link href="/companies">Research companies</Link>
            </div>
            <div className="market-table">
              <div className="market-table-head">
                <span>Ticker</span>
                <span>Tier</span>
                <span>Window</span>
                <span>Context</span>
              </div>
              {movers.map((row) => (
                <Link className="market-table-row" key={row.ticker} href={'/ticker/' + encodeURIComponent(row.ticker)}>
                  <strong>{row.ticker}</strong>
                  <span>{row.tier}</span>
                  <span>{row.window}</span>
                  <span>{row.note}</span>
                </Link>
              ))}
            </div>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Liquidity watch</h3>
              <Link href="/learn">Learn why</Link>
            </div>
            <ul className="market-news-list">
              {liquidityWatch.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </section>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Latest market notes</h3>
              <Link href="/demo">Demo mode</Link>
            </div>
            <ul className="market-news-list">
              {marketNotes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Next step</h3>
              <Link href="/tools">Open tools</Link>
            </div>
            <ul className="market-news-list">
              <li>Use Market Pulse to get context first.</li>
              <li>Open Companies to research a specific ticker.</li>
              <li>Use Tools for portfolio planning and decision review.</li>
            </ul>
          </section>
        </div>
      </section>

      <div className="notice warning">
        <p>
          Demo Market Pulse is a product mockup using sample or internally prepared data. It is for
          education and decision-support demonstration only, not investment advice or an official
          real-time exchange feed.
        </p>
      </div>
    </div>
  );
}
