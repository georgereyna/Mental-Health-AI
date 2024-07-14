# src/modules/intake_module.py

from typing import Dict, Any
from src.utils.event_bus import EventBus

class IntakeModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('intake_started', self.process)

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simplified intake process
        result = {
            'patient_id': data['patient_id'],
            'risk_level': self.assess_risk(data),
            'screening_result': self.screen_patient(data),
            'recommended_action': 'Schedule appointment within 1 week'
        }
        await self.event_bus.publish('intake_completed', result)
        return result

    def assess_risk(self, data: Dict[str, Any]) -> str:
        # Simplified risk assessment
        if 'suicidal thoughts' in data.get('symptoms', []):
            return 'high'
        elif len(data.get('symptoms', [])) > 2:
            return 'medium'
        else:
            return 'low'

    def screen_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simplified screening
        symptoms = data.get('symptoms', [])
        if 'feeling sad' in symptoms or 'lack of interest' in symptoms:
            category = 'depression'
        elif 'anxiety' in symptoms or 'excessive worry' in symptoms:
            category = 'anxiety'
        else:
            category = 'unspecified'
        
        return {
            'category': category,
            'confidence': 0.8  # Placeholder confidence value
        }