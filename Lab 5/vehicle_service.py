
"""Manage vehicle service records, costs, and job cards."""

import hashlib
import json
from datetime import date
from pathlib import Path
import shutil

SERVICE_RATES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "General": 2500,
    "Brake Check": 1200,
}
service_records = {}


def add_service(vehicle_no, service_type="General", history=None):
    """Add a service record and return the updated vehicle history."""
    if history is None:
        history = []

    cost = SERVICE_RATES.get(service_type, 0)
    entry = {
        "type": service_type,
        "cost": cost,
        "date": str(date.today()),
    }
    service_records.setdefault(vehicle_no, []).append(entry)
    history.append(vehicle_no)
    return history


def cancel_service(vehicle_no, service_type):
    """Remove matching service jobs for a vehicle."""
    try:
        jobs = service_records[vehicle_no]
    except KeyError:
        print("No records for", vehicle_no)
        return False

    remaining = [job for job in jobs if job["type"] != service_type]
    service_records[vehicle_no] = remaining
    return len(remaining) < len(jobs)


def get_total_cost(vehicle_no):
    """Return the total service cost for a vehicle."""
    total_cost = 0
    for job in service_records.get(vehicle_no, []):
        total_cost += job["cost"]
    return total_cost


def job_card_id(vehicle_no):
    """Return a short, deterministic job-card identifier."""
    return hashlib.sha256(vehicle_no.encode("utf-8")).hexdigest()[:8]


def busiest_vehicle():
    """Return the vehicle with the most service records, if any."""
    best = None
    for vehicle, jobs in service_records.items():
        if best is None or len(jobs) > len(service_records[best]):
            best = vehicle
    return best


def save_records(file_name="services.json"):
    """Save service records to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(service_records, file, indent=2)


def load_records(file_name="services.json"):
    """Load service records from a JSON file."""
    with open(file_name, encoding="utf-8") as file:
        return json.load(file)


def backup_records(folder):
    """Copy the service records file into the specified folder."""
    destination = Path(folder)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2("services.json", destination / "services.json")


def main():
    """Run the vehicle-service demonstration."""
    add_service("KA01AB1234", "Oil Change")
    add_service("KA01AB1234", "Wheel Alignment")
    add_service("KA05XY9876")
    add_service("KA03MN4455", "Brake Check")
    cancel_service("KA05XY9876", "Brake Check")
    cancel_service("KA09ZZ0001", "General")
    cancel_service("KA03MN4455", "Brake Check")
    print("Total for KA01AB1234:", get_total_cost("KA01AB1234"))
    print("Total for KA05XY9876:", get_total_cost("KA05XY9876"))
    print("Job card for KA01AB1234:", job_card_id("KA01AB1234"))
    save_records()
    loaded = load_records()
    print(
        "Vehicles on file:",
        len(loaded),
        "| busiest vehicle:",
        busiest_vehicle(),
    )


if __name__ == "__main__":
    main()
