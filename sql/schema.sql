-- Optimus Telemetry Table suitable for high-frequency sensor data
CREATE TABLE IF NOT EXISTS optimus_test_telemetry (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    unit_id INT,              -- Representing an Optimus Bot ID
    cycle_time INT,           -- Cycle count
    op_setting_1 FLOAT,       -- Ambient temp
    sensor_11_temp FLOAT,     -- Motor/Joint Temp
    sensor_12_pressure FLOAT, -- Hydraulic/Actuator Pressure
    status VARCHAR(20) DEFAULT 'OPERATIONAL'
);

-- Indexing for high-speed retrieval (Tesla JD requirement)
-- Optimizes queries filtering by unit and sorting by recent cycles
CREATE INDEX IF NOT EXISTS idx_unit_cycle ON optimus_test_telemetry(unit_id, cycle_time DESC);
