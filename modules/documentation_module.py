from typing import Dict, Any
from src.utils.event_bus import EventBus

class DocumentationModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe('intake_completed', self.create_initial_record)
        self.event_bus.subscribe('appointment_scheduled', self.update_record)

    async def create_initial_record(self, intake_result: Dict[str, Any]):
        # Create initial documentation
        print(f"Created initial record for patient {intake_result['patient_id']}")

    async def update_record(self, appointment: Dict[str, Any]):
        # Update documentation with appointment info
        print(f"Updated record for patient {appointment['patient_id']} with appointment details")