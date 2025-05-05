import React from "react";
import { MapContainer, TileLayer, Rectangle } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapViewer = ({ result }) => {
  const bboxes = result.detections.map((d, i) => ({
    id: i,
    bounds: [
      [d.bbox[1], d.bbox[0]],
      [d.bbox[3], d.bbox[2]],
    ],
  }));

  return (
    <div className="h-[400px] mb-4">
      <MapContainer center={[0, 0]} zoom={2} className="h-full w-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {bboxes.map((b) => (
          <Rectangle
            key={b.id}
            bounds={b.bounds}
            pathOptions={{ color: "red" }}
          />
        ))}
      </MapContainer>
    </div>
  );
};

export default MapViewer;
