import { InfoCard } from '@/components/shared/InfoCard';
import { TextStack } from '@/components/shared/TextStack';
import { getDecisionAudit } from '@/lib/api';
import { formatJmd } from '@/lib/formatters';

const DEFAULT_CAPITAL = 100000;

function TextCard({ title, label, lines }: { title: string; label: string; lines: string[] }) {
  return (
    <InfoCard title={title} label={label}>
      <TextStack lines={lines} />
    </InfoCard>
  );
}

export default async function ReviewPage() {
  let audit;
  let error: string | null = null;

  try {
    audit = await getDecisionAudit(DEFAULT_CAPITAL, 'guided');
  } catch {
    error = 'Decision audit data is not available right now. Please try again after the API is reachable.';
  }

  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Decision Audit</span>
        <h1>Review why the plan looks the way it does.</h1>
        <p>
          This page uses the hosted FastAPI backend to explain funded rationale, unfunded rationale,
          rules applied, and cash reserve logic for a sample {formatJmd(DEFAULT_CAPITAL)} guided plan.
        </p>
      </section>

      {error || !audit ? (
        <section className="grid">
          <InfoCard title="Decision audit unavailable" label="API status">
            <p>{error}</p>
          </InfoCard>
        </section>
      ) : (
        <>
          <div className="notice">
            <p>{audit.disclaimer}</p>
          </div>

          <section className="grid">
            <TextCard title="Summary" label={audit.mode} lines={audit.summary} />
            <TextCard title="Why trades were funded" label="Rationale" lines={audit.funded_rationale} />
            <TextCard title="Why trades were not funded" label="Discipline" lines={audit.unfunded_rationale} />
          </section>

          <section className="grid two">
            <TextCard title="Rules applied" label="Method" lines={audit.rules_applied} />
            <InfoCard title="Cash reserve" label="Risk control">
              <p>{audit.cash_reserve_explanation}</p>
            </InfoCard>
          </section>
        </>
      )}
    </div>
  );
}
