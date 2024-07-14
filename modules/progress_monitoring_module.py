# src/modules/progress_monitoring_module.py

from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.utils.event_bus import EventBus

class ProgressMonitoringModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('symptom_logged', self.update_progress)
        self.event_bus.subscribe('treatment_plan_generated', self.initialize_progress)
        self.patient_progress = {}

    async def initialize_progress(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        self.patient_progress[patient_id] = {
            'start_date': datetime.now(),
            'initial_symptoms': [],
            'symptom_history': [],
            'treatment_plan': data['treatment_plan'],
            'goals': self.set_initial_goals(data['treatment_plan'])
        }

    def set_initial_goals(self, treatment_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {'description': 'Reduce overall symptom severity', 'target': 'Decrease by 50%', 'status': 'In Progress'},
            {'description': 'Adhere to primary treatment', 'target': treatment_plan['primary_treatment'], 'status': 'Not Started'},
            {'description': 'Implement lifestyle changes', 'target': ', '.join(treatment_plan['lifestyle_recommendations']), 'status': 'Not Started'}
        ]

    async def update_progress(self, symptom_data: Dict[str, Any]):
        patient_id = symptom_data['patient_id']
        if patient_id not in self.patient_progress:
            return  # Patient progress not initialized yet

        progress = self.patient_progress[patient_id]
        progress['symptom_history'].append(symptom_data['log_entry'])

        if len(progress['symptom_history']) % 5 == 0:  # Generate report every 5 symptoms logged
            report = self.generate_progress_report(patient_id)
            print(f"\nProgress Report for patient {patient_id}:")
            print(report)
            await self.event_bus.publish('progress_report_generated', {'patient_id': patient_id, 'report': report})

    def generate_progress_report(self, patient_id: str) -> Dict[str, Any]:
        progress = self.patient_progress[patient_id]
        current_symptoms = progress['symptom_history'][-5:]  # Last 5 symptoms
        initial_symptoms = progress['symptom_history'][:5]  # First 5 symptoms

        avg_current_severity = sum(s['severity'] for s in current_symptoms) / len(current_symptoms)
        avg_initial_severity = sum(s['severity'] for s in initial_symptoms) / len(initial_symptoms)

        severity_change = ((avg_current_severity - avg_initial_severity) / avg_initial_severity) * 100

        report = {
            'duration': (datetime.now() - progress['start_date']).days,
            'avg_initial_severity': avg_initial_severity,
            'avg_current_severity': avg_current_severity,
            'severity_change': severity_change,
            'goals': progress['goals'],
        }

        # Update goal status
        if severity_change <= -50:
            report['goals'][0]['status'] = 'Achieved'
        elif severity_change < 0:
            report['goals'][0]['status'] = 'Improving'

        return report

    def get_patient_progress(self, patient_id: str) -> Dict[str, Any]:
        return self.patient_progress.get(patient_id, {})