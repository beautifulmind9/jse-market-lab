import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const researchAreas = [
  {
    title: 'Research Hub',
    label: 'Future surface',
    body: 'A future place to organize company notes, market notes, event context, and source links once hosting and data-rights rules are clear.',
  },
  {
    title: 'Company notes',
    label: 'Future surface',
    body: 'A future index of company-focused research notes connected to Company Pages and Ticker Analysis.',
  },
  {
    title: 'Analyst Call Tracker',
    label: 'Future surface',
    body: 'A future tracker for analyst calls, company presentations, and event-based research context where available.',
  },
];

export default function ResearchPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Research</span>
        <h1>Organize company and market intelligence carefully.</h1>
        <p>
          Research surfaces are part of the platform vision, but public hosting, redistribution, and
          monetization must stay gated until data-rights and compliance questions are resolved.
        </p>
      </section>

      <section className="grid">
        {researchAreas.map((area) => (
          <InfoCard key={area.title} title={area.title} label={area.label}>
            <p>{area.body}</p>
          </InfoCard>
        ))}
      </section>

      <div className="notice warning">
        <p>
          Research content should not be presented as official, licensed, or sponsored until sources,
          rights, and disclosures are validated.
        </p>
      </div>

      <div className="button-row">
        <Link className="button" href="/companies">
          Start with companies
        </Link>
        <Link className="button secondary" href="/platform-preview">
          View research roadmap
        </Link>
      </div>
    </div>
  );
}
