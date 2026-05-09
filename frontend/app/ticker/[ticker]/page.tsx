import { InfoCard } from '@/components/shared/InfoCard';
import { getTickerAnalysis } from '@/lib/api';
import { formatPercent } from '@/lib/formatters';

type TickerPageProps = {
  params: {
    ticker: string;
  };
};

export default async function TickerPage({ params }: TickerPageProps) {
  const ticker = params.ticker.toUpperCase();
  let analysis;
  let error: string | null = null;

  try {
    analysis = await getTickerAnalysis(ticker, 'guided');
  } catch {
    error = 'Ticker analysis is not available right now. Please try again after the API is reachable.';
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Ticker Analysis</span>
        <h1>{ticker}</h1>
        <p>
          Review quick take, holding-window behavior, risk profile, execution behavior, and what to
          watch before making your own decision.
        </p>
      </section>

      {error || !analysis ? (
        <section className="grid">
          <InfoCard title="Ticker data unavailable" label="API status">
            <p>{error}</p>
          </InfoCard>
        </section>
      ) : (
        <>
          <section className="grid">
            <InfoCard title="Quick take" label={analysis.mode}>
              {analysis.quick_take.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </InfoCard>
            <InfoCard title="Best holding window" label="Current sample">
              <p>{analysis.best_holding_window || 'Not enough data yet'}</p>
              <p>Use this as context, not a prediction.</p>
            </InfoCard>
            <InfoCard title="What to watch" label="Risk context">
              {analysis.what_to_watch.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </InfoCard>
          </section>

          <section className="hero">
            <span className="eyebrow">Holding windows</span>
            <h2>Historical signal behavior</h2>
          </section>
          <section className="grid">
            {analysis.holding_windows.map((window) => (
              <InfoCard key={window.holding_window} title={window.holding_window} label="Window">
                <p>Signals: {window.count}</p>
                <p>Win rate: {formatPercent(window.win_rate)}</p>
                <p>Median return: {formatPercent(window.median_return)}</p>
                <p>Average return: {formatPercent(window.average_return)}</p>
              </InfoCard>
            ))}
          </section>

          <section className="grid">
            <InfoCard title="Risk profile" label="Review">
              {analysis.risk_profile.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </InfoCard>
            <InfoCard title="Execution behavior" label="Market reality">
              {analysis.execution_behavior.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </InfoCard>
            <InfoCard title="Decision boundary" label="Reminder">
              <p>{analysis.disclaimer}</p>
            </InfoCard>
          </section>
        </>
      )}
    </div>
  );
}
