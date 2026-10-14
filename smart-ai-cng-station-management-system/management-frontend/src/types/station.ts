export interface Station {
  id: number;
  owner_id?: number | null;
  owner_username?: string | null;
  name: string;
  source: string;
  address: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  total_dispensers: number;
  cng_price: number | null;
  is_active: boolean;

  active_dispensers: number;
  average_fueling_time: number;

  queue_length: number;
  estimated_waiting_time: number;

  last_updated: string;
  created_at: string;
  updated_at: string;
}