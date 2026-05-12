import './globals.css';
import type { Metadata } from 'next';
import { Navigation } from '@/components/layout/Navigation';
import { AIHelperShell } from '@/components/shared/AIHelperShell';
import { DemoModeBanner } from '@/components/shared/DemoModeBanner';

export const metadata: Metadata = {
  title: 'JSE Market Lab',
  description: 'Decision-support dashboard for Jamaican Stock Exchange investors.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <DemoModeBanner />
        <Navigation />
        <main>{children}</main>
        <AIHelperShell />
      </body>
    </html>
  );
}
