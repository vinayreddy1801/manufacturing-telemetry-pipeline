import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def check_production_health():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return

    print("🔍 Sentinel: Scanning for Anomalies...")

    # SQL to find units where sensor_11 (Temp) is spiking
    # Threshold > 500 is arbitrary for testing, adjust based on data
    query = """
    SELECT unit_id, cycle_time, sensor_11_temp 
    FROM optimus_test_telemetry 
    WHERE sensor_11_temp > 500 
    ORDER BY timestamp DESC LIMIT 10;
    """
    
    try:
        cur.execute(query)
        rows = cur.fetchall()
        
        if rows:
            print(f"⚠️  ALERT: {len(rows)} High-Temp Anomalies Detected!")
            for row in rows:
                print(f"   -> Unit {row[0]} | Cycle {row[1]} | Temp {row[2]:.2f} - CHECK REQUIRED")
            
            # Here you would integrate with PagerDuty, Slack, or insert into an alerts table
        else:
            print("✅ All Systems Normal. No anomalies detected.")
            
    except Exception as e:
        print(f"❌ Error querying anomalies: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    check_production_health()
