import { InfoCard } from '@/components/shared/InfoCard';

type TickerPageProps = {
  params: {
    ticker: string;
  };
};

export default function TickerPage({ params }: TickerPageProps) {
  const ticker = params.ticker.toUpperCase();

  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Ticker Analysis</span>
        <h1>{ticker}</h1>
        <p>
          This page will show quick take, best holding window, risk profile, execution behavior, and
          what to watch for a single ticker.
        </p>
      </section>

      <section className="grid">
        <InfoCard title="Quick take" label="Guided">
          <p>
            The API-backed summary will explain whether the ticker has enough completed signal
            history for a clean read.
          </p>
        </InfoCard>
        <InfoCard title="Holding windows" label="5D / 10D / 20D / 30D">
          <p>
            This section will compare typical behavior across available holding windows using median
            return first, with average return as supporting context.
          </p>
        </InfoCard>
        <InfoCard title="What to watch" label="Risk context">
          <p>
            The dashboard will highlight liquidity, volume support, volatility, and any incomplete data
            before the user makes their own decision.
          </p>
        </InfoCard>
      </section>
    </div>
  );
}
