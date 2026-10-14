import api from "../api/axios";
import type { Station } from "../types/station";

export const getStations = async (): Promise<Station[]> => {
  const response = await api.get<Station[]>("/stations/");
  return response.data;
};

// Used by StationRequests.tsx when a Manager requests ownership of an existing station.
// Reuses the existing stations endpoint; no new backend endpoint is required.
export const getStationsForOwnershipRequest = async (): Promise<Station[]> => {
  return getStations();
};

export type StationUpdatePayload = Partial<
  Pick<
    Station,
    | "name"
    | "address"
    | "city"
    | "state"
    | "latitude"
    | "longitude"
    | "total_dispensers"
    | "active_dispensers"
    | "cng_price"
    | "is_active"
  >
>;

export const updateStation = async (
  stationId: number,
  data: StationUpdatePayload
): Promise<Station> => {
  const response = await api.put<Station>(`/stations/${stationId}`, data);
  return response.data;
};

export const deleteStation = async (
  stationId: number,
  role: "ADMIN" | "MANAGER"
) => {
  const endpoint =
    role === "ADMIN"
      ? `/stations/admin/${stationId}`
      : `/stations/${stationId}`;

  const response = await api.delete(endpoint);

  return response.data;
};

export interface OSMRefreshResponse {
  message: string;
  added: number;
  updated: number;
  unchanged: number;
}

export const refreshOSMStations =
  async (): Promise<OSMRefreshResponse> => {
    const response =
      await api.post<OSMRefreshResponse>(
        "/admin/refresh-cng-stations"
      );

    return response.data;
  };
