export function formatJmd(value: number): string {
  return new Intl.NumberFormat('en-JM', {
    style: 'currency',
    currency: 'JMD',
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatPercent(value: number): string {
  return new Intl.NumberFormat('en-JM', {
    style: 'percent',
    maximumFractionDigits: 1,
  }).format(value);
}
