from typing import Dict, Any, List
from datetime import datetime
from src.utils.event_bus import EventBus

class SymptomTrackingModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.symptom_logs: Dict[str, List[Dict[str, Any]]] = {}
        self.event_bus.subscribe('symptom_logged', self.process_symptom_log)

    async def log_symptom(self, patient_id: str, symptom_data: Dict[str, Any]):
        if patient_id not in self.symptom_logs:
            self.symptom_logs[patient_id] = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'symptom': symptom_data['symptom'],
            'severity': symptom_data['severity'],
            'duration': symptom_data.get('duration', None),
            'notes': symptom_data.get('notes', None)
        }
        
        self.symptom_logs[patient_id].append(log_entry)
        await self.event_bus.publish('symptom_logged', {'patient_id': patient_id, 'log_entry': log_entry})

    async def process_symptom_log(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        log_entry = data['log_entry']
        analysis = self.analyze_symptoms(patient_id)
        await self.event_bus.publish('symptom_analysis_completed', {'patient_id': patient_id, 'analysis': analysis})

    def analyze_symptoms(self, patient_id: str) -> Dict[str, Any]:
        if patient_id not in self.symptom_logs or not self.symptom_logs[patient_id]:
            return {'status': 'No symptom data available'}

        logs = self.symptom_logs[patient_id]
        symptoms = {}
        for log in logs:
            symptom = log['symptom']
            if symptom not in symptoms:
                symptoms[symptom] = {'count': 0, 'total_severity': 0, 'first_reported': log['timestamp'], 'last_reported': log['timestamp']}
            symptoms[symptom]['count'] += 1
            symptoms[symptom]['total_severity'] += log['severity']
            symptoms[symptom]['last_reported'] = log['timestamp']

        analysis = {
            'total_logs': len(logs),
            'unique_symptoms': len(symptoms),
            'symptom_summary': [
                {
                    'symptom': symptom,
                    'frequency': data['count'],
                    'avg_severity': data['total_severity'] / data['count'],
                    'first_reported': data['first_reported'],
                    'last_reported': data['last_reported']
                }
                for symptom, data in symptoms.items()
            ]
        }

        return analysis

    def get_patient_symptom_logs(self, patient_id: str) -> List[Dict[str, Any]]:
        return self.symptom_logs.get(patient_id, [])