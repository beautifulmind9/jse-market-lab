export type ViewMode = 'guided' | 'advanced';

export type Trade = {
  ticker: string;
  company_name: string;
  tier: string;
  holding_window: string;
  allocation_amount: number;
  allocation_pct: number;
  liquidity_status: string;
  risk_flags: string[];
  reason: string;
  net_pl_context: string;
  selection_rank?: number | null;
  funded_rank?: number | null;
};

export type PortfolioPlan = {
  capital: number;
  mode: ViewMode;
  funded_trades: Trade[];
  unfunded_trades: Trade[];
  reserve_cash: number;
  summary: {
    funded_count: number;
    unfunded_count: number;
    total_allocated: number;
    cash_reserve: number;
  };
  disclaimer: string;
};

export type DataStatus = {
  dataset_source: string;
  row_count: number;
  latest_market_date: string | null;
  warnings: string[];
  errors: string[];
  message: string;
};

export type TickerAnalysis = {
  ticker: string;
  mode: ViewMode;
  quick_take: string[];
  best_holding_window: string;
  holding_windows: Array<{
    holding_window: string;
    count: number;
    win_rate: number;
    median_return: number;
    average_return: number;
  }>;
  risk_profile: string[];
  what_to_watch: string[];
  execution_behavior: string[];
  disclaimer: string;
};

export type DecisionAudit = {
  mode: ViewMode;
  summary: string[];
  funded_rationale: string[];
  unfunded_rationale: string[];
  rules_applied: string[];
  cash_reserve_explanation: string;
  disclaimer: string;
};
