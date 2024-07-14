# src/modules/ehr_integration_module.py

from typing import Dict, Any
from src.utils.event_bus import EventBus
import json
import os

class EHRIntegrationModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('patient_data_saved', self.sync_to_ehr)
        self.event_bus.subscribe('treatment_plan_generated', self.update_ehr_treatment_plan)
        self.ehr_data_dir = 'ehr_data'
        os.makedirs(self.ehr_data_dir, exist_ok=True)

    async def sync_to_ehr(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        patient_data = data.get('data', {})
        
        # In a real system, this would interact with an actual EHR API
        # For this simulation, we'll save to a JSON file
        ehr_file = os.path.join(self.ehr_data_dir, f"{patient_id}_ehr.json")
        
        try:
            with open(ehr_file, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}
        
        # Update only if patient_data is a dictionary
        if isinstance(patient_data, dict):
            existing_data.update(patient_data)
        else:
            # If it's not a dictionary (e.g., encrypted data), store it as is
            existing_data['encrypted_data'] = patient_data
        
        with open(ehr_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        print(f"Patient data for {patient_id} synced to EHR")

    async def update_ehr_treatment_plan(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        treatment_plan = data['treatment_plan']
        
        ehr_file = os.path.join(self.ehr_data_dir, f"{patient_id}_ehr.json")
        
        try:
            with open(ehr_file, 'r') as f:
                ehr_data = json.load(f)
        except FileNotFoundError:
            ehr_data = {}
        
        ehr_data['treatment_plan'] = treatment_plan
        
        with open(ehr_file, 'w') as f:
            json.dump(ehr_data, f, indent=2)
        
        print(f"Treatment plan for patient {patient_id} updated in EHR")

    def retrieve_from_ehr(self, patient_id: str) -> Dict[str, Any]:
        ehr_file = os.path.join(self.ehr_data_dir, f"{patient_id}_ehr.json")
        
        try:
            with open(ehr_file, 'r') as f:
                ehr_data = json.load(f)
            return ehr_data
        except FileNotFoundError:
            print(f"No EHR data found for patient {patient_id}")
            return {}