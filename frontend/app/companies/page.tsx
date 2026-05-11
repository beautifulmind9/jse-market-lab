import Link from 'next/link';

const sampleCompanies = [
  {
    ticker: 'JMMBGL',
    name: 'JMMB Group Limited',
    focus: 'Financial services',
    status: 'Working ticker analysis',
    context: 'Use this sample to review quick take, holding windows, risk context, and what to watch.',
  },
  {
    ticker: 'WIPT',
    name: 'Wigton Windfarm Limited',
    focus: 'Energy / utilities',
    status: 'Demo company card',
    context: 'Useful for showing how company pages can connect market movement, signals, and research context.',
  },
  {
    ticker: 'CAR',
    name: 'Carreras Limited',
    focus: 'Consumer / income context',
    status: 'Demo company card',
    context: 'Useful for future dividend and income-context workflows once source data is validated.',
  },
  {
    ticker: 'TJH8.0',
    name: 'TransJamaican Highway preference',
    focus: 'Preference / income context',
    status: 'Demo company card',
    context: 'Useful for showing income, holding-window, and tradability considerations in a company view.',
  },
];

const companyModules = [
  {
    title: 'Ticker Analysis',
    label: 'Working surface',
    body: 'Review quick take, historical holding-window behavior, risk context, and what to watch for a single ticker.',
  },
  {
    title: 'Company Profile',
    label: 'Future anchor',
    body: 'A future company page will combine business context, market data, signals, dividend notes, and research links.',
  },
  {
    title: 'Dividend Context',
    label: 'Future income layer',
    body: 'Future income tools will show distribution timing, history, and risk notes without treating dividends as guaranteed.',
  },
  {
    title: 'Earnings Scorecard',
    label: 'Future research layer',
    body: 'A future scorecard will connect earnings events to company behavior, source notes, and market reaction context.',
  },
  {
    title: 'Float / Tradability',
    label: 'Future market reality layer',
    body: 'A future layer will help users understand liquidity, float, spread risk, and entry/exit difficulty.',
  },
  {
    title: 'Research Links',
    label: 'Compliance-gated',
    body: 'Research hosting and redistribution must remain gated until source rights and compliance rules are validated.',
  },
];

const researchSteps = [
  'Start with broad Market Pulse context.',
  'Open a company or ticker page for focused review.',
  'Check holding windows, liquidity, costs, and risk notes.',
  'Use Tools only after reviewing context and assumptions.',
];

export default function CompaniesPage() {
  return (
    <div className="page-shell market-home-shell">
      <section className="market-front">
        <div className="market-tape" aria-label="Demo company research status tape">
          <div className="tape-item">
            <span>Company mode</span>
            <strong>Demo / internal</strong>
          </div>
          <div className="tape-item">
            <span>Available view</span>
            <strong>Ticker Analysis</strong>
          </div>
          <div className="tape-item">
            <span>Future modules</span>
            <strong>Company Pages</strong>
          </div>
          <div className="tape-item warn">
            <span>Status</span>
            <strong>Not advice</strong>
          </div>
        </div>

        <div className="market-front-grid">
          <div className="market-lede-panel">
            <span className="eyebrow">Demo Company Research</span>
            <h2>Start with a ticker, then build the company picture.</h2>
            <p>
              Companies will become the research anchor for ticker analysis, dividend context, earnings
              notes, tradability, and source links. Current examples are for product walkthroughs only.
            </p>
            <div className="market-lede-actions">
              <Link href="/market">Market Pulse</Link>
              <Link href="/tools">Tools</Link>
              <Link href="/research">Research</Link>
            </div>
          </div>

          <div className="quote-panel">
            <div className="quote-panel-header">
              <span>Research Board</span>
              <strong>DEMO</strong>
            </div>
            <div className="quote-metrics">
              <div>
                <span>Working surface</span>
                <strong>Ticker Analysis</strong>
              </div>
              <div>
                <span>Next layer</span>
                <strong>Company Pages</strong>
              </div>
              <div>
                <span>Data status</span>
                <strong>Internal/demo</strong>
              </div>
            </div>
          </div>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Sample company cards</h3>
              <Link href="/market">Back to Market</Link>
            </div>
            <div className="company-card-grid">
              {sampleCompanies.map((company) => (
                <Link className="company-research-card" key={company.ticker} href={'/ticker/' + encodeURIComponent(company.ticker)}>
                  <span>{company.status}</span>
                  <strong>{company.ticker}</strong>
                  <h4>{company.name}</h4>
                  <p>{company.focus}</p>
                  <small>{company.context}</small>
                </Link>
              ))}
            </div>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Research flow</h3>
              <Link href="/learn">Learn</Link>
            </div>
            <ul className="market-news-list">
              {researchSteps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul>
          </section>
        </div>

        <div className="market-content-grid">
          <section className="market-module wide">
            <div className="module-heading">
              <h3>Company page modules</h3>
              <Link href="/platform-preview">Preview roadmap</Link>
            </div>
            <div className="company-module-grid">
              {companyModules.map((module) => (
                <div className="company-module-card" key={module.title}>
                  <span>{module.label}</span>
                  <strong>{module.title}</strong>
                  <p>{module.body}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="market-module">
            <div className="module-heading">
              <h3>Next step</h3>
              <Link href="/tools">Open tools</Link>
            </div>
            <ul className="market-news-list">
              <li>Open a ticker analysis page for a focused view.</li>
              <li>Review market context before treating a setup as useful.</li>
              <li>Use portfolio tools only after checking liquidity, risk, and assumptions.</li>
            </ul>
          </section>
        </div>
      </section>

      <div className="notice warning">
        <p>
          Company research examples use sample or internally prepared data for product demonstration.
          They are not investment advice, recommendations, official research coverage, or live JSE data.
        </p>
      </div>
    </div>
  );
}
