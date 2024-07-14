# src/modules/continuous_learning_module.py

from typing import Dict, Any, List
from src.utils.event_bus import EventBus
import json
import os
from datetime import datetime

class ContinuousLearningModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('treatment_outcome', self.process_outcome)
        self.event_bus.subscribe('clinician_feedback', self.process_feedback)
        self.data_dir = 'learning_data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.outcomes_file = os.path.join(self.data_dir, 'treatment_outcomes.json')
        self.feedback_file = os.path.join(self.data_dir, 'clinician_feedback.json')
        self.load_data()

    def load_data(self):
        if os.path.exists(self.outcomes_file):
            with open(self.outcomes_file, 'r') as f:
                self.outcomes = json.load(f)
        else:
            self.outcomes = []

        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback = json.load(f)
        else:
            self.feedback = []

    def save_data(self):
        with open(self.outcomes_file, 'w') as f:
            json.dump(self.outcomes, f, indent=2)
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback, f, indent=2)

    async def process_outcome(self, data: Dict[str, Any]):
        self.outcomes.append({
            'timestamp': datetime.now().isoformat(),
            'patient_id': data['patient_id'],
            'treatment': data['treatment'],
            'outcome': data['outcome'],
            'duration': data['duration']
        })
        self.save_data()
        await self.update_models()

    async def process_feedback(self, data: Dict[str, Any]):
        self.feedback.append({
            'timestamp': datetime.now().isoformat(),
            'clinician_id': data['clinician_id'],
            'patient_id': data['patient_id'],
            'module': data['module'],
            'feedback_type': data['feedback_type'],
            'details': data.get('details', '')
        })
        self.save_data()
        await self.update_models()

    async def update_models(self):
        print("\nUpdating models based on new data:")
        self.analyze_outcomes()
        self.analyze_feedback()
        # Any other model updating logic would go here

    def analyze_outcomes(self):
        if not self.outcomes:
            print("No treatment outcomes recorded yet.")
            return

        total_outcomes = len(self.outcomes)
        successful_outcomes = sum(1 for outcome in self.outcomes if outcome['outcome'] == 'successful')
        success_rate = (successful_outcomes / total_outcomes) * 100

        print(f"Treatment Success Rate: {success_rate:.2f}%")
        print(f"Total Outcomes Recorded: {total_outcomes}")

        # You could add more sophisticated analysis here, such as:
        # - Success rates by treatment type
        # - Average treatment duration
        # - Correlation between treatment duration and success rate

    def analyze_feedback(self):
        if not self.feedback:
            print("No clinician feedback recorded yet.")
            return

        feedback_count = len(self.feedback)
        module_feedback = {}

        for item in self.feedback:
            module = item['module']
            if module not in module_feedback:
                module_feedback[module] = {'positive': 0, 'negative': 0}
            
            if item['feedback_type'] == 'positive':
                module_feedback[module]['positive'] += 1
            else:
                module_feedback[module]['negative'] += 1

        print(f"Total Feedback Entries: {feedback_count}")
        for module, counts in module_feedback.items():
            total = counts['positive'] + counts['negative']
            positive_rate = (counts['positive'] / total) * 100
            print(f"Module '{module}' Positive Feedback Rate: {positive_rate:.2f}%")

    def get_learning_summary(self) -> Dict[str, Any]:
        return {
            'total_outcomes': len(self.outcomes),
            'total_feedback': len(self.feedback),
            'last_update': datetime.now().isoformat()
        }