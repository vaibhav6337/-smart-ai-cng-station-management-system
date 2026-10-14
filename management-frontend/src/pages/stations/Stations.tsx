import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import {
  ExternalLink,
  Fuel,
  Pencil,
  RefreshCw,
  Search,
  Trash2,
  X,
} from "lucide-react";
import toast from "react-hot-toast";
import {
  deleteStation,
  getStations,
  refreshOSMStations,
  updateStation,
} from "../../services/stationService";
import { getStoredUser } from "../../services/authService";
import type { Station } from "../../types/station";
interface StationEditForm {
  name: string;
  address: string;
  city: string;
  state: string;
  latitude: string;
  longitude: string;
  total_dispensers: string;
  active_dispensers: string;
  cng_price: string;
  is_active: boolean;
}
const Stations = () => {
  const user = useMemo(() => getStoredUser(), []);
  const isAdmin = user?.role === "ADMIN";
  const canEditStations = isAdmin || user?.role === "MANAGER";
  const [stations, setStations] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
const [refreshing, setRefreshing] = useState(false);
const [refreshingOSM, setRefreshingOSM] = useState(false);
  const [search, setSearch] = useState("");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [selectedStation, setSelectedStation] =
    useState<Station | null>(null);
  const [isEditingStation, setIsEditingStation] = useState(false);
  const [savingStation, setSavingStation] = useState(false);
  const [editForm, setEditForm] = useState<StationEditForm | null>(null);
  const loadStations = async (showLoader = true) => {
    try {
      if (showLoader) {
        setLoading(true);
      } else {
        setRefreshing(true);
      }
      const data = await getStations();
      setStations(data);
    } catch (error: any) {
      const message =
        error?.response?.data?.detail ||
        "Unable to load stations.";
      toast.error(message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  useEffect(() => {
    loadStations();
  }, []);
  const accessibleStations = useMemo(() => {
    if (isAdmin) {
      return stations;
    }
    if (user?.role !== "MANAGER") {
      return [];
    }
    const assignedStationIds = new Set(user.station_ids ?? []);
    return stations.filter((station) =>
      assignedStationIds.has(station.id)
    );
  }, [stations, isAdmin, user]);
  const filteredStations = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();
    return accessibleStations.filter((station) => {
      const matchesSearch =
        !normalizedSearch ||
        station.name.toLowerCase().includes(normalizedSearch) ||
        station.address.toLowerCase().includes(normalizedSearch) ||
        station.city.toLowerCase().includes(normalizedSearch) ||
        station.state.toLowerCase().includes(normalizedSearch);
      const matchesSource =
        sourceFilter === "all" ||
        station.source.toLowerCase() ===
          sourceFilter.toLowerCase();
      const matchesStatus =
        statusFilter === "all" ||
        (statusFilter === "active" && station.is_active) ||
        (statusFilter === "inactive" && !station.is_active);
      return (
        matchesSearch &&
        matchesSource &&
        matchesStatus
      );
    });
  }, [
    accessibleStations,
    search,
    sourceFilter,
    statusFilter,
  ]);
  const openStationDetails = (station: Station) => {
    setSelectedStation(station);
    setIsEditingStation(false);
    setEditForm(null);
  };
  const startEditingStation = (station: Station) => {
    if (!canEditStations) {
      toast.error("You do not have permission to edit stations.");
      return;
    }
    setSelectedStation(station);
    setIsEditingStation(true);
    setEditForm({
      name: station.name ?? "",
      address: station.address ?? "",
      city: station.city ?? "",
      state: station.state ?? "",
      latitude: String(station.latitude ?? ""),
      longitude: String(station.longitude ?? ""),
      total_dispensers: String(station.total_dispensers ?? ""),
      active_dispensers: String(station.active_dispensers ?? ""),
      cng_price: station.cng_price == null ? "" : String(station.cng_price),
      is_active: Boolean(station.is_active),
    });
  };
  const closeStationModal = () => {
    setSelectedStation(null);
    setIsEditingStation(false);
    setEditForm(null);
  };
  const handleSaveStation = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!user || !selectedStation || !editForm || !canEditStations) {
      toast.error("You do not have permission to update this station.");
      return;
    }
    const totalDispensers = isAdmin
      ? Number(editForm.total_dispensers)
      : selectedStation.total_dispensers;
    const activeDispensers = Number(editForm.active_dispensers);
    const cngPrice = editForm.cng_price.trim() === ""
      ? null
      : Number(editForm.cng_price);
    if (!Number.isInteger(totalDispensers) || totalDispensers < 1) {
      toast.error("Total dispensers must be a whole number greater than zero.");
      return;
    }
    if (!Number.isInteger(activeDispensers) || activeDispensers < 0) {
      toast.error("Active dispensers must be a whole number of zero or more.");
      return;
    }
    if (activeDispensers > totalDispensers) {
      toast.error("Active dispensers cannot exceed total dispensers.");
      return;
    }
    if (cngPrice !== null && (!Number.isFinite(cngPrice) || cngPrice < 0)) {
      toast.error("CNG price must be a valid non-negative number.");
      return;
    }
    const payload = isAdmin
      ? {
          name: editForm.name.trim(),
          address: editForm.address.trim(),
          city: editForm.city.trim(),
          state: editForm.state.trim(),
          latitude: Number(editForm.latitude),
          longitude: Number(editForm.longitude),
          total_dispensers: totalDispensers,
          active_dispensers: activeDispensers,
          cng_price: cngPrice,
          is_active: editForm.is_active,
        }
      : {
          active_dispensers: activeDispensers,
          cng_price: cngPrice,
          is_active: editForm.is_active,
        };
    if (isAdmin) {
      if (!payload.name || !payload.address || !payload.city || !payload.state) {
        toast.error("Name, address, city, and state are required.");
        return;
      }
      if (
        !Number.isFinite(payload.latitude) ||
        payload.latitude < -90 ||
        payload.latitude > 90 ||
        !Number.isFinite(payload.longitude) ||
        payload.longitude < -180 ||
        payload.longitude > 180
      ) {
        toast.error("Enter valid latitude and longitude values.");
        return;
      }
    }
    try {
      setSavingStation(true);
      await updateStation(selectedStation.id, payload);
      toast.success("Station updated successfully.");
      closeStationModal();
      await loadStations(false);
    } catch (error: any) {
      const message =
        error?.response?.data?.detail ||
        "Unable to update station.";
      toast.error(message);
    } finally {
      setSavingStation(false);
    }
  };
  const handleRefreshOSM = async () => {
  if (!isAdmin) {
    toast.error("Administrator access is required.");
    return;
  }
  try {
    setRefreshingOSM(true);
    const result = await refreshOSMStations();
    toast.success(
      `OSM refresh completed: ${result.added} added, ${result.updated} updated, ${result.unchanged} unchanged.`
    );
    await loadStations(false);
  } catch (error: any) {
    const message =
      error?.response?.data?.detail ||
      "Unable to refresh OSM stations.";
    toast.error(message);
  } finally {
    setRefreshingOSM(false);
  }
};
  const handleDelete = async (station: Station) => {
    if (!user || user.role !== "ADMIN") {
      toast.error("Administrator access is required.");
      return;
    }
    const confirmed = window.confirm(
      `Are you sure you want to delete "${station.name}"?`
    );
    if (!confirmed) {
      return;
    }
    try {
      await deleteStation(station.id, user.role);
      toast.success(
        "Station deleted successfully."
      );
      setSelectedStation(null);
      await loadStations(false);
    } catch (error: any) {
      const message =
        error?.response?.data?.detail ||
        "Unable to delete station.";
      toast.error(message);
    }
  };
  const activeCount = accessibleStations.filter(
    (station) => station.is_active
  ).length;
  const inactiveCount =
    accessibleStations.length - activeCount;
  const osmCount = accessibleStations.filter(
    (station) =>
      station.source.toLowerCase() === "osm"
  ).length;
  return (
    <div>
      <div className="page-header">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: "16px",
          }}
        >
          <div>
            <h1 className="page-title">
              Stations
            </h1>
            <p className="page-description">
              View and manage CNG stations available to
              your account.
            </p>
          </div>
          <div
  style={{
    display: "flex",
    alignItems: "center",
    gap: "8px",
    flexWrap: "wrap",
  }}
>
  <button
    type="button"
    className="logout-button"
    onClick={() => loadStations(false)}
    disabled={refreshing || refreshingOSM}
  >
    <RefreshCw
      size={17}
      className={
        refreshing ? "spin-icon" : ""
      }
    />
    {refreshing
      ? "Refreshing..."
      : "Refresh"}
  </button>
  {user?.role === "ADMIN" && (
    <button
      type="button"
      className="primary-action-button"
      onClick={handleRefreshOSM}
      disabled={refreshingOSM || refreshing}
    >
      <RefreshCw
        size={17}
        className={
          refreshingOSM ? "spin-icon" : ""
        }
      />
      {refreshingOSM
        ? "Refreshing OSM..."
        : "Refresh OSM"}
    </button>
  )}
</div>
        </div>
      </div>
      {/* Summary */}
      <div className="station-summary-grid">
        <div className="station-summary-card">
          <span>Total Stations</span>
          <strong>{accessibleStations.length}</strong>
        </div>
        <div className="station-summary-card">
          <span>Active</span>
          <strong>{activeCount}</strong>
        </div>
        <div className="station-summary-card">
          <span>Inactive</span>
          <strong>{inactiveCount}</strong>
        </div>
        <div className="station-summary-card">
          <span>OSM / External</span>
          <strong>{osmCount}</strong>
        </div>
      </div>
      {/* Filters */}
      <div className="station-toolbar">
        <div className="station-search">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search station, city or address..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch("")}
            >
              <X size={16} />
            </button>
          )}
        </div>
        <select
  value={sourceFilter}
  onChange={(event) =>
    setSourceFilter(event.target.value)
  }
>
  <option value="all">
    All Sources
  </option>
  <option value="managed">
    Managed
  </option>
  <option value="osm">
    External / OSM
  </option>
</select>
        <select
          value={statusFilter}
          onChange={(event) =>
            setStatusFilter(event.target.value)
          }
        >
          <option value="all">
            All Status
          </option>
          <option value="active">
            Active
          </option>
          <option value="inactive">
            Inactive
          </option>
        </select>
      </div>
      {/* Content */}
      {loading ? (
        <div className="station-state">
          Loading stations...
        </div>
      ) : filteredStations.length === 0 ? (
        <div className="station-state">
          <Fuel size={30} />
          <strong>
            No stations found
          </strong>
          <span>
            Try changing your search or filters.
          </span>
        </div>
      ) : (
        <div className="station-table-wrapper">
          <table className="station-table">
            <thead>
              <tr>
                <th>Station</th>
                <th>Source</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Dispensers</th>
                <th>Queue</th>
                <th>CNG Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredStations.map((station) => (
                <tr key={station.id}>
                  <td>
                    <button
                      type="button"
                      className="station-name-button"
                      onClick={() => openStationDetails(station)}
                    >
                      <strong>
                        {station.name}
                      </strong>
                      <span>
                        {station.city},{" "}
                        {station.state}
                      </span>
                    </button>
                  </td>
                  <td>
                    <span
                      className={`station-source ${
                        station.source.toLowerCase() ===
                        "osm"
                          ? "external"
                          : "managed"
                      }`}
                    >
                      {station.source.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    {station.owner_username ||
                      (station.owner_id == null ? "Unassigned" : "—")}
                  </td>
                  <td>
                    <span
                      className={`station-status ${
                        station.is_active
                          ? "active"
                          : "inactive"
                      }`}
                    >
                      {station.is_active
                        ? "Active"
                        : "Inactive"}
                    </span>
                  </td>
                  <td>
                    {station.active_dispensers}/
                    {station.total_dispensers}
                  </td>
                  <td>
                    {station.queue_length}
                  </td>
                  <td>
                    {station.cng_price !== null
                      ? `₹${station.cng_price}`
                      : "—"}
                  </td>
                  <td>
                    <div
                      style={{
                        display: "flex",
                        gap: "6px",
                      }}
                    >
                      <button
                        type="button"
                        className="table-action-button"
                        onClick={() => openStationDetails(station)}
                        title="View details"
                      >
                        <ExternalLink
                          size={16}
                        />
                      </button>
                      {canEditStations && (
                        <button
                          type="button"
                          className="table-action-button"
                          onClick={() => startEditingStation(station)}
                          title="Edit station"
                        >
                          <Pencil size={16} />
                        </button>
                      )}
                      {isAdmin && (
                        <button
                          type="button"
                          className="table-action-button danger"
                          onClick={() =>
                            handleDelete(station)
                          }
                          title="Delete station"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {/* Details */}
      {selectedStation && (
        <div
          className="station-modal-overlay"
          onClick={closeStationModal}
        >
          <div
            className="station-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="station-modal-header">
              <div>
                <h2>
                  {isEditingStation ? "Edit Station" : selectedStation.name}
                </h2>
                <p>
                  Station ID: #
                  {selectedStation.id}
                </p>
              </div>
              <button
                type="button"
                onClick={closeStationModal}
              >
                <X size={20} />
              </button>
            </div>
            {isEditingStation && editForm ? (
              <form onSubmit={handleSaveStation}>
                {isAdmin && (
                  <div className="request-form-grid">
                    <div className="form-field">
                      <label htmlFor="station-name">Station Name</label>
                      <input id="station-name" required value={editForm.name} onChange={(event) => setEditForm({ ...editForm, name: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-address">Address</label>
                      <input id="station-address" required value={editForm.address} onChange={(event) => setEditForm({ ...editForm, address: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-city">City</label>
                      <input id="station-city" required value={editForm.city} onChange={(event) => setEditForm({ ...editForm, city: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-state">State</label>
                      <input id="station-state" required value={editForm.state} onChange={(event) => setEditForm({ ...editForm, state: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-latitude">Latitude</label>
                      <input id="station-latitude" type="number" step="any" required value={editForm.latitude} onChange={(event) => setEditForm({ ...editForm, latitude: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-longitude">Longitude</label>
                      <input id="station-longitude" type="number" step="any" required value={editForm.longitude} onChange={(event) => setEditForm({ ...editForm, longitude: event.target.value })} />
                    </div>
                    <div className="form-field">
                      <label htmlFor="station-total-dispensers">Total Dispensers</label>
                      <input id="station-total-dispensers" type="number" min="1" step="1" required value={editForm.total_dispensers} onChange={(event) => setEditForm({ ...editForm, total_dispensers: event.target.value })} />
                    </div>
                  </div>
                )}
                <div className="request-form-grid" style={{ marginTop: isAdmin ? 18 : 0 }}>
                  <div className="form-field">
                    <label htmlFor="station-active-dispensers">Active Dispensers</label>
                    <input id="station-active-dispensers" type="number" min="0" max={isAdmin ? (editForm.total_dispensers || undefined) : selectedStation.total_dispensers} step="1" required value={editForm.active_dispensers} onChange={(event) => setEditForm({ ...editForm, active_dispensers: event.target.value })} />
                  </div>
                  <div className="form-field">
                    <label htmlFor="station-cng-price">CNG Price (₹/kg)</label>
                    <input id="station-cng-price" type="number" min="0" step="0.01" value={editForm.cng_price} onChange={(event) => setEditForm({ ...editForm, cng_price: event.target.value })} placeholder="Not available" />
                  </div>
                  <div className="form-field">
                    <label htmlFor="station-is-active">Station Status</label>
                    <select id="station-is-active" value={editForm.is_active ? "active" : "inactive"} onChange={(event) => setEditForm({ ...editForm, is_active: event.target.value === "active" })}>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>
                {!isAdmin && (
                  <p className="page-description" style={{ marginTop: 14 }}>
                    Managers can update operational details only. Station name, address, coordinates, and total dispensers are read-only.
                  </p>
                )}
                <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 24 }}>
                  <button type="button" className="logout-button" onClick={closeStationModal} disabled={savingStation}>Cancel</button>
                  <button type="submit" className="primary-action-button" disabled={savingStation}>
                    {savingStation ? "Saving..." : "Save Changes"}
                  </button>
                </div>
              </form>
            ) : (
              <>
            <div className="station-detail-grid">
              <div>
                <span>Address</span>
                <strong>
                  {selectedStation.address}
                </strong>
              </div>
              <div>
                <span>Location</span>
                <strong>
                  {selectedStation.city},{" "}
                  {selectedStation.state}
                </strong>
              </div>
              <div>
                <span>Coordinates</span>
                <strong>
                  {selectedStation.latitude},{" "}
                  {selectedStation.longitude}
                </strong>
              </div>
              <div>
                <span>Source</span>
                <strong>
                  {selectedStation.source}
                </strong>
              </div>
              <div>
                <span>Dispensers</span>
                <strong>
                  {selectedStation.active_dispensers}/
                  {
                    selectedStation.total_dispensers
                  }
                </strong>
              </div>
              <div>
                <span>Queue Length</span>
                <strong>
                  {selectedStation.queue_length}
                </strong>
              </div>
              <div>
                <span>Estimated Wait</span>
                <strong>
                  {
                    selectedStation.estimated_waiting_time
                  }{" "}
                  min
                </strong>
              </div>
              <div>
                <span>Average Fueling</span>
                <strong>
                  {
                    selectedStation.average_fueling_time
                  }{" "}
                  min
                </strong>
              </div>
              <div>
                <span>CNG Price</span>
                <strong>
                  {selectedStation.cng_price !== null
                    ? `₹${selectedStation.cng_price}`
                    : "Not available"}
                </strong>
              </div>
              <div>
                <span>Status</span>
                <strong>
                  {selectedStation.is_active
                    ? "Active"
                    : "Inactive"}
                </strong>
              </div>
              <div>
                <span>Last Updated</span>
                <strong>
                  {new Date(
                    selectedStation.last_updated
                  ).toLocaleString()}
                </strong>
              </div>
            </div>
            {canEditStations && (
              <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 24 }}>
                <button type="button" className="primary-action-button" onClick={() => startEditingStation(selectedStation)}>
                  <Pencil size={16} />
                  Edit Station
                </button>
                {isAdmin && (
                  <button type="button" className="delete-station-button" onClick={() => handleDelete(selectedStation)}>
                    <Trash2 size={16} />
                    Delete Station
                  </button>
                )}
              </div>
            )}
              </>
            )}
          </div>
        </div>
      )}

    </div>
  );
};
export default Stations;
