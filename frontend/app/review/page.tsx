import { InfoCard } from '@/components/shared/InfoCard';

export default function ReviewPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Decision Audit</span>
        <h1>Review why the plan looks the way it does.</h1>
        <p>
          This page will explain funded rationale, unfunded rationale, rules applied, and cash reserve
          logic in simple decision-support language.
        </p>
      </section>

      <section className="grid">
        <InfoCard title="Why trades were funded" label="Rationale">
          <p>
            Shows which quality, confidence, and portfolio rules supported funding for review.
          </p>
        </InfoCard>
        <InfoCard title="Why trades were not funded" label="Discipline">
          <p>
            Explains liquidity failures, Tier C handling, allocation limits, and other constraints without
            forcing weak setups into the plan.
          </p>
        </InfoCard>
        <InfoCard title="Cash reserve" label="Risk control">
          <p>
            Keeps unallocated capital visible so the user understands reserve cash is part of the plan,
            not a mistake.
          </p>
        </InfoCard>
      </section>
    </div>
  );
}
