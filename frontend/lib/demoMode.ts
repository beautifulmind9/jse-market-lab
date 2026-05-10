export function isDemoMode(): boolean {
  return process.env.NEXT_PUBLIC_DEMO_MODE === 'true';
}

export const DEMO_MODE_MESSAGE =
  'Demo Mode — This view uses sample or transformed historical data to demonstrate the product experience. It is not an official live JSE feed and is not financial advice.';

export const DEMO_MODE_SHORT_LABEL = 'Demo mode';
