'use client';

import { useEffect, useState } from 'react';
import { getDataStatus } from '@/lib/api';
import type { DataStatus } from '@/lib/types';
import { InfoCard } from './InfoCard';

export function ApiStatusCard() {
  const [status, setStatus] = useState<DataStatus | null>(null);
  const [message, setMessage] = useState('The frontend is ready. Add the backend URL when the API is hosted.');

  useEffect(() => {
    if (!process.env.NEXT_PUBLIC_API_BASE_URL) {
      return;
    }

    getDataStatus()
      .then((payload) => setStatus(payload))
      .catch(() => setMessage('The backend URL is configured, but the API is not reachable yet.'));
  }, []);

  if (status) {
    return (
      <InfoCard title="Data connection" label="API ready">
        <p>Source: {status.dataset_source}</p>
        <p>Rows loaded: {status.row_count}</p>
        <p>Latest market date: {status.latest_market_date || 'Not available'}</p>
      </InfoCard>
    );
  }

  return (
    <InfoCard title="Data connection" label="Frontend ready">
      <p>{message}</p>
    </InfoCard>
  );
}
