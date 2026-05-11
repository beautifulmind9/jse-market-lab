import type { DataStatus, DecisionAudit, PortfolioPlan, TickerAnalysis, ViewMode } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(API_BASE_URL + path, {
    ...init,
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  });

  if (!response.ok) {
    throw new Error('API request failed with status ' + response.status);
  }

  return response.json() as Promise<T>;
}

export function getDataStatus(): Promise<DataStatus> {
  return apiFetch<DataStatus>('/api/data/status');
}

export function getPortfolioPlan(
  capital: number,
  mode: ViewMode = 'guided',
  costProfile = 'conservative_estimate',
): Promise<PortfolioPlan> {
  return apiFetch<PortfolioPlan>('/api/portfolio/plan', {
    method: 'POST',
    body: JSON.stringify({ capital, mode, cost_profile: costProfile }),
  });
}

export function getTickerAnalysis(ticker: string, mode: ViewMode = 'guided'): Promise<TickerAnalysis> {
  const path = '/api/ticker/' + encodeURIComponent(ticker) + '/analysis?mode=' + encodeURIComponent(mode);
  return apiFetch<TickerAnalysis>(path);
}

export function getDecisionAudit(capital: number, mode: ViewMode = 'guided'): Promise<DecisionAudit> {
  const path = '/api/review/decision-audit?capital=' + encodeURIComponent(String(capital)) + '&mode=' + encodeURIComponent(mode);
  return apiFetch<DecisionAudit>(path);
}
