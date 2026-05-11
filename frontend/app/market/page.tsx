import Link from 'next/link';

const marketTape = [
  { label: 'Market mode', value: 'Demo / internal' },
  { label: 'Latest data', value: '2026-04-24' },
  { label: 'Rows loaded', value: '57,656+' },
  { label: 'Feed status', value: 'Not live JSE', tone: 'warn' },
];

const movers = [
  { ticker: 'JPS9.5', name: 'JPS Preference', window: '5D', tier: 'A', note: 'Funded in demo plan' },
  { ticker: 'WIPT', name: 'Wigton Windfarm', window: '30D', tier: 'A', note: 'Longer holding window' },
  { ticker: 'TJH8.0', name: 'TransJamaican Highway', window: '5D', tier: 'A', note: 'Smaller allocation' },
  { ticker: 'CAR', name: 'Carreras', window: '30D', tier: 'B', note: 'Held back by rules' },
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
      <section className="market-pulse-page">
        <div className="market-pulse-header">
          <span className="eyebrow">Demo Market Pulse</span>
          <h1>JSE market context, before the ticker deep dive.</h1>
          <p>
            A demo-safe market intelligence view for broad conditions, setup clusters, liquidity
            context, and data status. This is not an official live JSE feed.
          </p>
        </div>

        <div className="market-tape pulse-tape" aria-label="Demo Market Pulse status tape">
          {marketTape.map((item) => (
            <div key={item.label} className={'tape-item ' + (item.tone || 'neutral')}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </div>
          ))}
        </div>

        <div className="pulse-grid">
          <section className="pulse-module pulse-main">
            <div className="module-heading">
              <h2>Market movers mockup</h2>
              <Link href="/companies">Research companies</Link>
            </div>
            <div className="pulse-table">
              <div className="pulse-table-head">
                <span>Ticker</span>
                <span>Window</span>
                <span>Tier</span>
                <span>Context</span>
              </div>
              {movers.map((row) => (
                <Link className="pulse-table-row" key={row.ticker} href={'/ticker/' + encodeURIComponent(row.ticker)}>
                  <strong>{row.ticker}</strong>
                  <span>{row.window}</span>
                  <span>{row.tier}</span>
                  <span>{row.note}</span>
                </Link>
              ))}
            </div>
          </section>

          <section className="pulse-module">
            <div className="module-heading">
              <h2>Signal clusters</h2>
              <Link href="/tools">Open tools</Link>
            </div>
            <div className="cluster-list">
              {signalClusters.map((cluster) => (
                <div key={cluster.label}>
                  <span>{cluster.label}</span>
                  <strong>{cluster.value}</strong>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="pulse-grid lower">
          <section className="pulse-module">
            <div className="module-heading">
              <h2>Liquidity watch</h2>
              <Link href="/learn">Learn why it matters</Link>
            </div>
            <ul className="market-news-list">
              {liquidityWatch.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </section>

          <section className="pulse-module pulse-main">
            <div className="module-heading">
              <h2>Latest market notes</h2>
              <Link href="/demo">Demo mode</Link>
            </div>
            <ul className="market-news-list">
              {marketNotes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </section>
        </div>

        <div className="notice warning">
          <p>
            Demo Market Pulse is a product mockup using sample or internally prepared data. It is for
            education and decision-support demonstration only, not investment advice or an official
            real-time exchange feed.
          </p>
        </div>
      </section>
    </div>
  );
}
