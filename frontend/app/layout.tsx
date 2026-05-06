import './globals.css';
import type { Metadata } from 'next';
import { Navigation } from '@/components/layout/Navigation';

export const metadata: Metadata = {
  title: 'JSE Market Lab',
  description: 'Decision-support dashboard for Jamaican Stock Exchange investors.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navigation />
        <main>{children}</main>
      </body>
    </html>
  );
}
