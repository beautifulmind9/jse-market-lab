import Link from 'next/link';

const links = [
  { href: '/', label: 'Start Here' },
  { href: '/learn', label: 'Learn' },
  { href: '/market', label: 'Market' },
  { href: '/companies', label: 'Companies' },
  { href: '/tools', label: 'Tools' },
  { href: '/research', label: 'Research' },
  { href: '/demo', label: 'Demo' },
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
