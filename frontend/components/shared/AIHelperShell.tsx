'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

type HelperContent = {
  pageLabel: string;
  title: string;
  summary: string;
  checks: string[];
  prompts: string[];
  links: Array<{ href: string; label: string }>;
};

const defaultContent: HelperContent = {
  pageLabel: 'JSE Market Lab',
  title: 'I can help you find the right path.',
  summary:
    'Use me to understand this platform, what each page is showing, and what to check next. This shell is rule-based for now and does not make live AI or web-search calls yet.',
  checks: [
    'Confirm whether a page is using demo/internal data.',
    'Review liquidity, costs, holding windows, and risk context before using tools.',
    'Use the platform for decision support, not blind action.',
  ],
  prompts: [
    'What should I do first?',
    'Explain this page.',
    'What should I check next?',
  ],
  links: [
    { href: '/learn', label: 'Learn basics' },
    { href: '/market', label: 'Market Pulse' },
    { href: '/tools', label: 'Open Tools' },
  ],
};

const routeContent: Array<{ match: (path: string) => boolean; content: HelperContent }> = [
  {
    match: (path) => path === '/',
    content: {
      pageLabel: 'Homepage',
      title: 'Start with the market, then choose your path.',
      summary:
        'The homepage gives a demo market snapshot first, then routes you into learning, market context, company research, tools, income context, or the product demo.',
      checks: [
        'Check the market snapshot label so you know whether the data is demo/internal or live-authorized.',
        'Choose a path based on what you are trying to do today.',
        'Use Tools only after you understand the market/company context.',
      ],
      prompts: ['What does Demo Market Snapshot mean?', 'Which path should I choose?', 'How should I use this platform responsibly?'],
      links: [
        { href: '/market', label: 'Market Pulse' },
        { href: '/companies', label: 'Companies' },
        { href: '/tools', label: 'Tools' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/market'),
    content: {
      pageLabel: 'Market Pulse',
      title: 'Use this page for broad market context.',
      summary:
        'Market Pulse helps you see demo/internal market conditions, signal clusters, liquidity notes, and the next step before drilling into one ticker.',
      checks: [
        'Look at the demo/internal data label first.',
        'Use market notes and liquidity watch before researching a specific company.',
        'Do not treat a mover or cluster as a buy/sell instruction.',
      ],
      prompts: ['Explain Market Pulse.', 'What does liquidity watch mean?', 'What should I check before opening a company?'],
      links: [
        { href: '/companies', label: 'Research companies' },
        { href: '/tools', label: 'Open Tools' },
        { href: '/learn', label: 'Learn liquidity' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/companies'),
    content: {
      pageLabel: 'Companies',
      title: 'Start with a company, then build the research picture.',
      summary:
        'Companies is the research entry point. Use sample cards to open ticker analysis and understand future company-page modules such as dividends, earnings, and tradability.',
      checks: [
        'Open a ticker page for a focused view.',
        'Treat company cards as demo walkthrough examples, not recommendations.',
        'Review dividend, earnings, and tradability context once those modules are built.',
      ],
      prompts: ['How should I research a company here?', 'What should I check before using Tools?', 'What is a company page supposed to include?'],
      links: [
        { href: '/ticker/JMMBGL', label: 'Sample ticker' },
        { href: '/market', label: 'Market context' },
        { href: '/research', label: 'Research direction' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/tools') || path.startsWith('/portfolio') || path.startsWith('/review'),
    content: {
      pageLabel: 'Tools',
      title: 'Use Tools for structured decision support.',
      summary:
        'Tools help you review portfolio planning, ticker analysis, and decision audits. They support planning and review, not personal investment advice.',
      checks: [
        'Check liquidity and risk flags before interpreting a setup.',
        'Review cost assumptions because they affect possible net outcomes.',
        'Use Decision Audit to understand why the rules produced a result.',
      ],
      prompts: ['Which tool should I use first?', 'What does Decision Audit show?', 'Why do cost assumptions matter?'],
      links: [
        { href: '/portfolio', label: 'Portfolio Plan' },
        { href: '/ticker/JMMBGL', label: 'Ticker Analysis' },
        { href: '/review', label: 'Decision Audit' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/ticker'),
    content: {
      pageLabel: 'Ticker Analysis',
      title: 'Use this page to understand one ticker at a time.',
      summary:
        'Ticker Analysis explains quick take, holding-window behavior, risk context, execution behavior, and what to watch for a selected ticker.',
      checks: [
        'Compare 5D, 10D, 20D, and 30D behavior where available.',
        'Look at median return alongside average return.',
        'Treat the analysis as context, not a trade instruction.',
      ],
      prompts: ['What does holding window mean?', 'Why compare median and average return?', 'What should I watch before using this ticker in a plan?'],
      links: [
        { href: '/companies', label: 'Companies' },
        { href: '/portfolio', label: 'Portfolio Plan' },
        { href: '/learn', label: 'Learn terms' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/learn'),
    content: {
      pageLabel: 'Learn',
      title: 'Build the foundation before using outputs.',
      summary:
        'Learn explains JSE basics, liquidity, holding windows, costs, dividends, and responsible decision support in beginner-friendly language.',
      checks: [
        'Start with liquidity and costs if you are new to the JSE.',
        'Learn the difference between a signal and an instruction.',
        'Use education pages before interpreting advanced outputs.',
      ],
      prompts: ['Explain holding windows like I am new.', 'Why does volume matter?', 'What does decision support mean?'],
      links: [
        { href: '/market', label: 'Market Pulse' },
        { href: '/companies', label: 'Companies' },
        { href: '/tools', label: 'Tools' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/research'),
    content: {
      pageLabel: 'Research',
      title: 'Research needs source discipline.',
      summary:
        'Research surfaces are future/compliance-gated. Use this area to understand how source links, company notes, and market notes may be organized later.',
      checks: [
        'Separate official sources from commentary or summaries.',
        'Check source dates before relying on public information.',
        'Public-source research mode is planned later with citations.',
      ],
      prompts: ['What counts as an official source?', 'How should I verify research?', 'When will web search be available?'],
      links: [
        { href: '/companies', label: 'Companies' },
        { href: '/demo', label: 'Demo' },
        { href: '/platform-preview', label: 'Preview roadmap' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/income'),
    content: {
      pageLabel: 'Income',
      title: 'Use income context with risk in view.',
      summary:
        'Income views will focus on dividend context, payout timing, company income profiles, and future portfolio income estimates.',
      checks: [
        'Dividend history does not guarantee future dividends.',
        'Review company context and financial reports where available.',
        'Income planning should still include liquidity and risk checks.',
      ],
      prompts: ['What does dividend context mean?', 'Why is dividend history not a guarantee?', 'How will income tools work later?'],
      links: [
        { href: '/companies', label: 'Companies' },
        { href: '/learn', label: 'Learn dividends' },
        { href: '/platform-preview', label: 'Preview roadmap' },
      ],
    },
  },
  {
    match: (path) => path.startsWith('/demo') || path.startsWith('/platform-preview'),
    content: {
      pageLabel: 'Demo',
      title: 'Use this path for product walkthroughs.',
      summary:
        'Demo and Platform Preview explain what is built, what is future, and what depends on data rights, compliance review, or JSE/FSC/legal validation.',
      checks: [
        'Separate working features from roadmap features.',
        'Do not present demo/internal data as official live data.',
        'Use this flow for advisors, partners, grants, or product reviewers.',
      ],
      prompts: ['What is built today?', 'What is future work?', 'What needs compliance validation?'],
      links: [
        { href: '/', label: 'Homepage' },
        { href: '/market', label: 'Market Pulse' },
        { href: '/tools', label: 'Tools' },
      ],
    },
  },
];

function getContent(pathname: string): HelperContent {
  return routeContent.find((entry) => entry.match(pathname))?.content ?? defaultContent;
}

export function AIHelperShell() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const content = useMemo(() => getContent(pathname || '/'), [pathname]);

  return (
    <div className="ai-helper-root">
      {isOpen ? (
        <aside className="ai-helper-panel" aria-label="JSE Lab Helper panel">
          <div className="ai-helper-header">
            <div>
              <span>{content.pageLabel}</span>
              <h2>JSE Lab Helper</h2>
            </div>
            <button type="button" onClick={() => setIsOpen(false)} aria-label="Close JSE Lab Helper">
              ×
            </button>
          </div>

          <div className="ai-helper-body">
            <section>
              <h3>{content.title}</h3>
              <p>{content.summary}</p>
            </section>

            <section>
              <h4>What to check next</h4>
              <ul>
                {content.checks.map((check) => (
                  <li key={check}>{check}</li>
                ))}
              </ul>
            </section>

            <section>
              <h4>Suggested questions</h4>
              <div className="ai-helper-prompts">
                {content.prompts.map((prompt) => (
                  <span key={prompt}>{prompt}</span>
                ))}
              </div>
            </section>

            <section>
              <h4>Helpful links</h4>
              <div className="ai-helper-links">
                {content.links.map((link) => (
                  <Link key={link.href} href={link.href} onClick={() => setIsOpen(false)}>
                    {link.label}
                  </Link>
                ))}
              </div>
            </section>

            <section className="ai-helper-note">
              <h4>Research mode</h4>
              <p>
                Public-source internet research is planned for a later version with citations and
                source checks. This MVP helper does not make live AI, API, or web-search calls.
              </p>
            </section>

            <section className="ai-helper-warning">
              <p>
                JSE Lab Helper provides platform guidance only. It does not give personal investment
                advice, recommend buy/sell actions, guarantee outcomes, recommend brokers, or execute
                trades.
              </p>
            </section>
          </div>
        </aside>
      ) : null}

      <button className="ai-helper-button" type="button" onClick={() => setIsOpen((value) => !value)}>
        <span>Guide Me</span>
      </button>
    </div>
  );
}
