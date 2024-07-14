from typing import Dict, Any, List
from datetime import datetime
import asyncio
from src.utils.event_bus import EventBus

class CrisisDetectionModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('symptom_logged', self.assess_crisis)
        self.crisis_keywords = [
            'suicidal', 'suicide', 'kill myself', 'end my life',
            'hopeless', 'cannot go on', 'self-harm', 'hurt myself'
        ]
        self.high_severity_threshold = 8
        self.crisis_protocols = self.load_crisis_protocols()

    def load_crisis_protocols(self) -> Dict[str, List[str]]:
        return {
            'Suicide Risk': [
                "Immediately alert on-call clinician",
                "Assess immediate danger and consider emergency services",
                "Provide crisis hotline number",
                "Schedule urgent follow-up within 24 hours"
            ],
            'Self-Harm Risk': [
                "Alert treating clinician",
                "Provide resources for coping strategies",
                "Schedule follow-up within 48 hours",
                "Consider safety planning"
            ],
            'Severe Depression': [
                "Alert treating clinician",
                "Assess for suicidal ideation",
                "Provide resources for immediate support",
                "Schedule follow-up within 72 hours"
            ],
            'Psychosis': [
                "Immediately alert on-call clinician",
                "Assess for safety risks",
                "Consider emergency psychiatric evaluation",
                "Provide support resources to patient and family"
            ]
        }

    async def assess_crisis(self, symptom_data: Dict[str, Any]):
        patient_id = symptom_data['patient_id']
        log_entry = symptom_data['log_entry']
        message = log_entry['message']
        severity = log_entry['severity']

        is_crisis = self.detect_crisis_keywords(message) or severity >= self.high_severity_threshold
        crisis_type = 'Suicide Risk' if self.detect_crisis_keywords(message) else 'Severe Symptoms'

        if is_crisis:
            await self.trigger_crisis_protocol(patient_id, crisis_type, log_entry)

        return {
            'is_crisis': is_crisis,
            'severity': 'high' if is_crisis else 'low',
            'crisis_type': crisis_type if is_crisis else None
        }

    def detect_crisis_keywords(self, text: str) -> bool:
        return any(keyword in text.lower() for keyword in self.crisis_keywords)

    async def trigger_crisis_protocol(self, patient_id: str, crisis_type: str, symptom: Dict[str, Any]):
        protocol = self.crisis_protocols.get(crisis_type, [])
    
        alert = {
            'patient_id': patient_id,
            'crisis_type': crisis_type,
            'symptom': symptom['message'],
            'severity': symptom['severity'],
            'timestamp': symptom.get('timestamp', datetime.now().isoformat()),  # Add a default timestamp
            'protocol': protocol
        }
    
        print(f"CRISIS ALERT for patient {patient_id}:")
        print(f"Crisis Type: {crisis_type}")
        print(f"Symptom: {symptom['message']}")
        print(f"Severity: {symptom['severity']}")
        print("Initiating Crisis Protocol:")
        for step in protocol:
            print(f"- {step}")
    
        await self.event_bus.publish('crisis_alert', alert)
    
        # Simulate execution of crisis protocol
        for step in protocol:
            await asyncio.sleep(0.5)  # Simulate time taken for each step
            print(f"Executed: {step}")
        
        print(f"Crisis protocol for {crisis_type} completed for patient {patient_id}")

    async def handle_clinician_response(self, response_data: Dict[str, Any]):
        patient_id = response_data['patient_id']
        clinician_action = response_data['action']
        
        print(f"Clinician response for patient {patient_id}: {clinician_action}")
        
        # Here you would implement logic to handle the clinician's response
        # This could include updating the patient's record, adjusting the treatment plan, etc.
        
        await self.event_bus.publish('clinician_crisis_response', response_data)