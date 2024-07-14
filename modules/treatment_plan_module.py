# src/modules/treatment_plan_module.py

from typing import Dict, Any, List
from src.utils.event_bus import EventBus

class TreatmentPlanModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('intake_completed', self.generate_treatment_plan)
        self.treatment_guidelines = self.load_treatment_guidelines()

    def load_treatment_guidelines(self) -> Dict[str, List[str]]:
        # In a real-world scenario, this would load from a database or external source
        return {
            'depression': [
                'Cognitive Behavioral Therapy (CBT)',
                'Antidepressant medication (e.g., SSRIs)',
                'Regular exercise regimen',
                'Mindfulness and meditation practices'
            ],
            'anxiety': [
                'Cognitive Behavioral Therapy (CBT)',
                'Exposure therapy',
                'Anti-anxiety medication (e.g., SSRIs, benzodiazepines)',
                'Relaxation techniques'
            ],
            'bipolar': [
                'Mood stabilizers (e.g., lithium, valproic acid)',
                'Psychoeducation',
                'Cognitive Behavioral Therapy (CBT)',
                'Regular sleep schedule'
            ],
            'ocd': [
                'Exposure and Response Prevention (ERP) therapy',
                'Cognitive Behavioral Therapy (CBT)',
                'SSRI medication',
                'Mindfulness practices'
            ],
            'unspecified': [
                'Comprehensive psychological evaluation',
                'Supportive counseling',
                'Stress management techniques',
                'Healthy lifestyle changes'
            ]
        }

    async def generate_treatment_plan(self, intake_result: Dict[str, Any]):
        patient_id = intake_result.get('patient_id', 'Unknown')
        screening_result = intake_result.get('screening_result', {})
        condition = screening_result.get('category', 'unspecified')
        risk_level = intake_result.get('risk_level', 'low')

        treatment_plan = self.create_treatment_plan(condition, risk_level)
        
        print(f"Generated Treatment Plan for patient {patient_id}:")
        print(treatment_plan)
        
        await self.event_bus.publish('treatment_plan_generated', {
            'patient_id': patient_id,
            'treatment_plan': treatment_plan
        })

    def create_treatment_plan(self, condition: str, risk_level: str) -> Dict[str, Any]:
        base_treatments = self.treatment_guidelines.get(condition, self.treatment_guidelines['unspecified'])
        
        treatment_plan = {
            'primary_treatment': base_treatments[0] if base_treatments else "Consult with a specialist",
            'additional_treatments': base_treatments[1:3] if len(base_treatments) > 1 else [],
            'lifestyle_recommendations': ['Regular exercise', 'Healthy diet', 'Adequate sleep'],
            'follow_up': 'Schedule follow-up in 2 weeks'
        }

        if risk_level == 'high':
            treatment_plan['urgent_actions'] = ['Immediate psychiatric evaluation', 'Consider inpatient treatment']
        elif risk_level == 'medium':
            treatment_plan['urgent_actions'] = ['Expedited outpatient treatment', 'Weekly check-ins']

        return treatment_plan