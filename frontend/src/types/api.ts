// API Response Types

export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface TelegramChannel {
  id: number;
  user_id: number;
  channel_name: string;
  channel_id: string | null;
  is_active: boolean;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface TelegramChannelCreate {
  channel_name: string;
  channel_id?: string;
  description?: string;
  is_active?: boolean;
}

export interface TelegramChannelUpdate {
  channel_name?: string;
  description?: string;
  is_active?: boolean;
}

export type BrokerType = 'angel_one' | 'zerodha' | 'dhan' | 'upstox';

export interface Broker {
  id: number;
  user_id: number;
  broker_type: BrokerType;
  broker_name: string;
  is_active: boolean;
  has_api_key: boolean;
  has_api_secret: boolean;
  has_client_id: boolean;
  created_at: string;
  updated_at: string;
}

export interface BrokerCreate {
  broker_type: BrokerType;
  broker_name: string;
  api_key?: string;
  api_secret?: string;
  client_id?: string;
  access_token?: string;
  config?: Record<string, any>;
  is_active?: boolean;
}

export interface BrokerUpdate {
  broker_name?: string;
  api_key?: string;
  api_secret?: string;
  client_id?: string;
  access_token?: string;
  config?: Record<string, any>;
  is_active?: boolean;
}

export type SignalStatus = 'received' | 'parsed' | 'executing' | 'executed' | 'failed' | 'ignored';
export type OrderType = 'buy' | 'sell';
export type OrderAction = 'entry' | 'exit' | 'stoploss' | 'target';

export interface Signal {
  id: number;
  telegram_channel_id: number;
  raw_message: string;
  message_id: string | null;
  symbol: string | null;
  order_type: OrderType | null;
  action: OrderAction | null;
  quantity: number | null;
  entry_price: number | null;
  target_price: number | null;
  stoploss_price: number | null;
  parsed_data: Record<string, any> | null;
  status: SignalStatus;
  error_message: string | null;
  signal_time: string | null;
  received_at: string;
  parsed_at: string | null;
}

export interface SignalExecution {
  id: number;
  signal_id: number;
  broker_id: number;
  order_id: string | null;
  status: string;
  executed_price: number | null;
  executed_quantity: number | null;
  broker_response: Record<string, any> | null;
  error_message: string | null;
  executed_at: string | null;
  created_at: string;
}

export interface SignalWithExecutions extends Signal {
  executions: SignalExecution[];
}

export interface ChannelBrokerMapping {
  id: number;
  telegram_channel_id: number;
  broker_id: number;
  is_active: boolean;
  created_at: string;
}

export interface ChannelBrokerMappingCreate {
  telegram_channel_id: number;
  broker_id: number;
  is_active?: boolean;
}

export interface SignalStats {
  period_days: number;
  start_date: string;
  total_signals: number;
  parsed_signals: number;
  executed_signals: number;
  failed_signals: number;
  success_rate: number;
  execution_rate: number;
  top_symbols: [string, number][];
  signals_by_channel: Record<number, number>;
}

export interface ApiError {
  detail: string;
}
