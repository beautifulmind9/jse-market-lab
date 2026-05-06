import { InfoCard } from '@/components/shared/InfoCard';

const sampleTrades = [
  { ticker: 'JMMBGL', tier: 'A', window: '20D', status: 'Funded for review' },
  { ticker: 'GK', tier: 'B', window: '10D', status: 'Funded for review' },
  { ticker: 'XYZ', tier: 'C', window: '5D', status: 'Watch only' },
];

export default function PortfolioPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Portfolio Plan</span>
        <h1>Your capital plan will live here.</h1>
        <p>
          This page will call the FastAPI portfolio endpoint and render funded trades, unfunded trades,
          reserve cash, and rule-based explanations.
        </p>
      </section>

      <section className="grid">
        {sampleTrades.map((trade) => (
          <InfoCard key={trade.ticker} title={trade.ticker} label={trade.status}>
            <p>Tier: {trade.tier}</p>
            <p>Holding window: {trade.window}</p>
            <p>
              This placeholder keeps the frontend structure ready while API integration is added in the
              next slice.
            </p>
          </InfoCard>
        ))}
      </section>
    </div>
  );
}
