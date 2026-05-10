import { InfoCard } from '@/components/shared/InfoCard';
import { MetricRow } from '@/components/shared/MetricRow';
import { TextStack } from '@/components/shared/TextStack';
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
              <TextStack lines={analysis.quick_take} />
            </InfoCard>
            <InfoCard title="Best holding window" label="Current sample">
              <MetricRow label="Best window" value={analysis.best_holding_window || 'Not enough data yet'} />
              <p>Use this as context, not a prediction.</p>
            </InfoCard>
            <InfoCard title="What to watch" label="Risk context">
              <TextStack lines={analysis.what_to_watch} />
            </InfoCard>
          </section>

          <div className="notice">
            <p>{analysis.disclaimer}</p>
          </div>

          <section className="hero compact">
            <span className="eyebrow">Holding windows</span>
            <h2>Historical signal behavior</h2>
          </section>
          <section className="grid">
            {analysis.holding_windows.map((window) => (
              <InfoCard key={window.holding_window} title={window.holding_window} label="Window">
                <MetricRow label="Signals" value={window.count} />
                <MetricRow label="Win rate" value={formatPercent(window.win_rate)} />
                <MetricRow label="Median return" value={formatPercent(window.median_return)} />
                <MetricRow label="Average return" value={formatPercent(window.average_return)} />
              </InfoCard>
            ))}
          </section>

          <section className="grid two">
            <InfoCard title="Risk profile" label="Review">
              <TextStack lines={analysis.risk_profile} />
            </InfoCard>
            <InfoCard title="Execution behavior" label="Market reality">
              <TextStack lines={analysis.execution_behavior} />
            </InfoCard>
          </section>
        </>
      )}
    </div>
  );
}
