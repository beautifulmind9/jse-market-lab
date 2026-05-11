import Link from 'next/link';
import { InfoCard } from '@/components/shared/InfoCard';

const tools = [
  {
    title: 'Portfolio Plan',
    label: 'Working tool',
    body: 'Review funded setups, unfunded setups, cash reserve, and cost assumptions using the decision engine.',
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
    body: 'Understand why the plan looks the way it does and which rules shaped the output.',
    href: '/review',
  },
  {
    title: 'Setup Tester',
    label: 'Future simulation',
    body: 'A future workflow for testing a setup using historical data before acting in the real market.',
    href: '/platform-preview',
  },
  {
    title: 'Paper Portfolio',
    label: 'Future simulation',
    body: 'A future practice portfolio for tracking simulated positions, outcomes, and lessons learned.',
    href: '/platform-preview',
  },
  {
    title: 'AI Helper',
    label: 'Future assistant',
    body: 'A future guided assistant for navigation and explanation, not stock picking or trade instructions.',
    href: '/platform-preview',
  },
];

export default function ToolsPage() {
  return (
    <div className="page-shell">
      <section className="hero">
        <span className="eyebrow">Tools</span>
        <h1>Plan, review, and eventually test setups with structure.</h1>
        <p>
          Tools are where market information becomes a decision-support workflow. The current tools are
          live; future simulation tools remain preview-only until the data, profile, and compliance layers
          are ready.
        </p>
      </section>

      <section className="grid">
        {tools.map((tool) => (
          <InfoCard key={tool.title} title={tool.title} label={tool.label}>
            <p>{tool.body}</p>
            <Link href={tool.href}>Open</Link>
          </InfoCard>
        ))}
      </section>
    </div>
  );
}
