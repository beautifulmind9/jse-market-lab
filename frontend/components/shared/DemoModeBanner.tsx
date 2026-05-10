import Link from 'next/link';
import { DEMO_MODE_MESSAGE, isDemoMode } from '@/lib/demoMode';

export function DemoModeBanner() {
  if (!isDemoMode()) {
    return null;
  }

  return (
    <div className="demo-banner" role="note">
      <div className="demo-banner-inner">
        <span>{DEMO_MODE_MESSAGE}</span>
        <Link href="/demo">What this means</Link>
      </div>
    </div>
  );
}
