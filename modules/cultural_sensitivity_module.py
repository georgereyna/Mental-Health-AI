# src/modules/cultural_sensitivity_module.py

from typing import Dict, Any
from src.utils.event_bus import EventBus

class CulturalSensitivityModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('intake_completed', self.adapt_approach)
        self.event_bus.subscribe('treatment_plan_generated', self.customize_treatment_plan)
        self.cultural_adaptations = self.load_cultural_adaptations()

    def load_cultural_adaptations(self) -> Dict[str, Dict[str, Any]]:
        # In a real system, this would load from a database or external source
        return {
            'latino': {
                'language': 'Spanish',
                'family_involvement': 'High',
                'spirituality': 'Important',
                'stigma_reduction': 'Emphasize physical symptoms',
            },
            'asian': {
                'language': 'Varies',
                'family_involvement': 'High',
                'stigma_reduction': 'Frame as stress management',
                'communication_style': 'Less direct',
            },
            'african_american': {
                'spirituality': 'Often important',
                'discrimination_awareness': 'High',
                'community_involvement': 'Beneficial',
            },
            # Add more cultural adaptations as needed
        }

    async def adapt_approach(self, intake_data: Dict[str, Any]):
        patient_id = intake_data['patient_id']
        cultural_background = intake_data.get('cultural_background', 'default')
        
        adaptations = self.cultural_adaptations.get(cultural_background, {})
        
        if adaptations:
            print(f"Adapting approach for patient {patient_id} based on {cultural_background} background:")
            for key, value in adaptations.items():
                print(f"- {key}: {value}")
        else:
            print(f"No specific cultural adaptations for {cultural_background}. Using default approach.")

        # Publish adapted approach for other modules to use
        await self.event_bus.publish('cultural_adaptations', {
            'patient_id': patient_id,
            'adaptations': adaptations
        })

    async def customize_treatment_plan(self, plan_data: Dict[str, Any]):
        patient_id = plan_data['patient_id']
        treatment_plan = plan_data['treatment_plan']
        cultural_background = plan_data.get('cultural_background', 'default')
        
        adaptations = self.cultural_adaptations.get(cultural_background, {})
        
        if adaptations:
            print(f"Customizing treatment plan for patient {patient_id} based on {cultural_background} background:")
            
            if 'language' in adaptations:
                treatment_plan['language'] = adaptations['language']
                print(f"- Providing resources in {adaptations['language']}")
            
            if 'family_involvement' in adaptations and adaptations['family_involvement'] == 'High':
                treatment_plan['family_sessions'] = 'Recommended'
                print("- Recommending family involvement in treatment")
            
            if 'spirituality' in adaptations and adaptations['spirituality'] == 'Important':
                treatment_plan['consider_spirituality'] = True
                print("- Considering spirituality in treatment approach")
            
            if 'stigma_reduction' in adaptations:
                treatment_plan['framing'] = adaptations['stigma_reduction']
                print(f"- Framing treatment to reduce stigma: {adaptations['stigma_reduction']}")

        # Publish customized treatment plan
        await self.event_bus.publish('treatment_plan_customized', {
            'patient_id': patient_id,
            'treatment_plan': treatment_plan
        })

    def get_cultural_adaptation(self, cultural_background: str) -> Dict[str, Any]:
        return self.cultural_adaptations.get(cultural_background, {})