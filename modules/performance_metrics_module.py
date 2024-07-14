from typing import Dict, Any, List
from datetime import datetime, timedelta
import numpy as np

class PerformanceMetricsModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.screenings = []
        self.patient_satisfaction = {}
        self.treatment_outcomes = {}
        self.clinician_time = {}
        self.crisis_events = []
        
        # Subscribe to relevant events
        self.event_bus.subscribe('screening_completed', self.record_screening)
        self.event_bus.subscribe('patient_satisfaction_recorded', self.record_satisfaction)
        self.event_bus.subscribe('treatment_outcome_recorded', self.record_treatment_outcome)
        self.event_bus.subscribe('clinician_time_recorded', self.record_clinician_time)
        self.event_bus.subscribe('crisis_event_recorded', self.record_crisis_event)

    async def record_screening(self, data: Dict[str, Any]):
        self.screenings.append(data)

    async def record_satisfaction(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        satisfaction = data['satisfaction']
        self.patient_satisfaction[patient_id] = satisfaction

    async def record_treatment_outcome(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        outcome = data['outcome']
        self.treatment_outcomes[patient_id] = outcome

    async def record_clinician_time(self, data: Dict[str, Any]):
        clinician_id = data['clinician_id']
        time_spent = data['time_spent']
        if clinician_id not in self.clinician_time:
            self.clinician_time[clinician_id] = []
        self.clinician_time[clinician_id].append(time_spent)

    async def record_crisis_event(self, data: Dict[str, Any]):
        self.crisis_events.append(data)

    def calculate_screening_accuracy(self) -> float:
        if not self.screenings:
            return 0.0
        accurate_screenings = sum(1 for screening in self.screenings if screening['accurate'])
        return accurate_screenings / len(self.screenings)

    def calculate_patient_satisfaction(self) -> float:
        if not self.patient_satisfaction:
            return 0.0
        return sum(self.patient_satisfaction.values()) / len(self.patient_satisfaction)

    def calculate_treatment_improvement(self) -> float:
        if not self.treatment_outcomes:
            return 0.0
        improved_outcomes = sum(1 for outcome in self.treatment_outcomes.values() if outcome == 'improved')
        return improved_outcomes / len(self.treatment_outcomes)

    def calculate_clinician_time_saved(self) -> float:
        if not self.clinician_time:
            return 0.0
        baseline_time = 60  # Assume 60 minutes as baseline time per patient
        actual_time = np.mean([np.mean(times) for times in self.clinician_time.values()])
        return (baseline_time - actual_time) / baseline_time * 100

    def calculate_crisis_prevention_rate(self) -> float:
        total_patients = len(set(self.patient_satisfaction.keys()) | set(self.treatment_outcomes.keys()))
        if total_patients == 0:
            return 0.0
        prevented_crises = total_patients - len(self.crisis_events)
        return prevented_crises / total_patients

    def generate_performance_report(self) -> Dict[str, Any]:
        return {
            'screening_accuracy': self.calculate_screening_accuracy(),
            'patient_satisfaction': self.calculate_patient_satisfaction(),
            'treatment_improvement': self.calculate_treatment_improvement(),
            'clinician_time_saved': self.calculate_clinician_time_saved(),
            'crisis_prevention_rate': self.calculate_crisis_prevention_rate(),
            'report_generated_at': datetime.now().isoformat()
        }

# Example usage
async def main():
    from utils.event_bus import EventBus
    event_bus = EventBus()
    metrics_module = PerformanceMetricsModule(event_bus)

    # Simulate some events
    await event_bus.publish('screening_completed', {'patient_id': 'P001', 'accurate': True})
    await event_bus.publish('patient_satisfaction_recorded', {'patient_id': 'P001', 'satisfaction': 4.5})
    await event_bus.publish('treatment_outcome_recorded', {'patient_id': 'P001', 'outcome': 'improved'})
    await event_bus.publish('clinician_time_recorded', {'clinician_id': 'C001', 'time_spent': 45})
    await event_bus.publish('crisis_event_recorded', {'patient_id': 'P002', 'severity': 'high'})

    # Generate and print the performance report
    report = metrics_module.generate_performance_report()
    print("Performance Report:", report)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())