import Link from 'next/link';

const links = [
  { href: '/', label: 'Start Here' },
  { href: '/portfolio', label: 'Portfolio Plan' },
  { href: '/ticker/JMMBGL', label: 'Ticker Analysis' },
  { href: '/review', label: 'Review' },
];

export function Navigation() {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link href="/" className="brand">
          JSE Market Lab
        </Link>
        <nav className="nav-links" aria-label="Main navigation">
          {links.map((link) => (
            <Link key={link.href} href={link.href}>
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
