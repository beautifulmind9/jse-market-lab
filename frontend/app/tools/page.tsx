import Link from 'next/link';

const workingTools = [
  {
    title: 'Portfolio Plan',
    label: 'Working tool',
    body: 'Review funded setups, unfunded setups, reserve cash, allocation rules, and cost assumptions using the decision engine.',
    href: '/portfolio',
  },
  {
    title: 'Ticker Analysis',
    label: 'Working tool',
    body: 'Review one ticker at a time with quick take, holding-window behavior, risk context, and what to watch.',
    href: '/ticker/JMMBGL',
  },
  {
    title: 'Decision Audit',
    label: 'Working tool',
    body: 'Understand why the plan looks the way it does and which ranking, quality, liquidity, and allocation rules shaped the output.',
    href: '/review',
  },
];

const futureTools = [
  {
    title: 'Setup Tester',
    label: 'Future simulation',
    body: 'Practice testing a setup using historical data before acting in the real market. This will be simulation-only.',
    href: '/platform-preview',
  },
  {
    title: 'Paper Portfolio',
    label: 'Future simulation',
    body: 'Track simulated positions, outcomes, lessons learned, and review discipline without executing trades.',
    href: '/platform-preview',
  },
  {
    title: 'AI Helper',
    label: 'Future assistant',
    body: 'Guide users through the platform, explain terms, and help interpret outputs without stock picking or trade instructions.',
    href: '/platform-preview',
  },
];

const checklist = [
  'Start with Market Pulse to understand broad context.',
  'Research the company before interpreting a setup.',
  'Review liquidity, spread risk, and volume confirmation.',
  'Compare holding windows instead of treating every setup the same.',
  'Check estimated costs before looking at possible net outcomes.',
];

const costNotes = [
  { label: 'Cost mode', value: 'Conservative estimate' },
  { label: 'Broker fees', value: 'Range / profile based' },
  { label: 'CESS', value: 'Included where configured' },
  { label: 'Status', value: 'Confirm with broker' },
];

export default function ToolsPage() {
  return (
    <div className="page-shell market-home-shell">
      <section className="market-front">
        <div className="market-tape" aria-label="Decision-support tools status tape">
          <div className="tape-item">
            <span>Tools mode</span>
            <strong>Decision support</strong>
          </div>
          <div className="tape-item">
            <span>Working tools</span>
            <strong>3 live</strong>
          </div>
          <div className="tape-item">
            <span>Future tools</span>
            <strong>Simulation</strong>
          </div>
          <div className="tape-item warn">
            <span>Status</span>
            <strong>Not advice</strong>
          </div>
        </div>

        <div className="market-front-grid">
          <div className="market-lede-panel">
            <span className="eyebrow">Decision-Support Hub</span>
            <h2>Move from market context to structured review.</h2>
            <p>
              Tools help users plan, compare, and audit setups after reviewing market and company
              context. They support discipline, not blind action.
            </p>
            <div className="market-lede-actions">
              <Link href="/portfolio">Portfolio Plan</Link>
              <Link href="/ticker/JMMBGL">Ticker Analysis</Link>
              <Link href="/review">Decision Audit</Link>
            </div>
          </div>

          <div className="quote-panel">
            <div className="quote-panel-header">
              <span>Tool Board</span>
              <strong>GUIDED</strong>
            </div>
            <div className="quote-metrics">
              <div>
                <span>Planning</span>
                <strong>Portfolio</strong>
              </div>
              <div>
                <span>Research input</span>
                <strong>Ticker</strong>
              </div>
              <div>
                <span>Review layer</span>
                <strong>Audit</strong>
              </div>
            </div>
          </div>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Working tools</h3>
              <Link href="/market">Start with market</Link>
            </div>
            <div className="company-card-grid">
              {workingTools.map((tool) => (
                <Link className="company-research-card" key={tool.title} href={tool.href}>
                  <span>{tool.label}</span>
                  <strong>{tool.title}</strong>
                  <p>{tool.body}</p>
                  <small>Open tool</small>
                </Link>
              ))}
            </div>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Before using tools</h3>
              <Link href="/companies">Companies</Link>
            </div>
            <ul className="market-news-list">
              {checklist.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Future simulation tools</h3>
              <Link href="/platform-preview">Preview roadmap</Link>
            </div>
            <div className="company-module-grid">
              {futureTools.map((tool) => (
                <Link className="company-module-card" key={tool.title} href={tool.href}>
                  <span>{tool.label}</span>
                  <strong>{tool.title}</strong>
                  <p>{tool.body}</p>
                </Link>
              ))}
            </div>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Cost assumptions</h3>
              <Link href="/learn">Learn costs</Link>
            </div>
            <div className="quote-metrics">
              {costNotes.map((note) => (
                <div key={note.label}>
                  <span>{note.label}</span>
                  <strong>{note.value}</strong>
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>

      <div className="notice warning">
        <p>
          Tools are for decision support, education, and simulation planning. They do not provide
          personal investment advice, guarantee outcomes, execute trades, recommend a broker, or hold
          client funds.
        </p>
      </div>
    </div>
  );
}
