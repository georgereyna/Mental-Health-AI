from typing import Dict, Any
from datetime import datetime, timedelta
import uuid
from src.utils.event_bus import EventBus

class SchedulerModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.appointments = {}
        self.reminders = {}

    async def schedule_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        patient_id = data['patient_id']
        preferred_time = data.get('preferred_time', datetime.now() + timedelta(days=1))
        
        # In a real system, this would check availability and book the appointment
        appointment_id = f"APT-{uuid.uuid4().hex[:8]}"
        appointment_time = datetime.fromisoformat(preferred_time) if isinstance(preferred_time, str) else preferred_time
        
        appointment = {
            'appointment_id': appointment_id,
            'patient_id': patient_id,
            'date': appointment_time.date().isoformat(),
            'time': appointment_time.time().isoformat(),
        }
        
        self.appointments[appointment_id] = appointment
        self.set_reminder(patient_id, appointment_time)
        
        print(f"Appointment scheduled for patient {patient_id} on {appointment['date']} at {appointment['time']}")
        await self.event_bus.publish('appointment_scheduled', appointment)
        
        return appointment

    def set_reminder(self, patient_id: str, appointment_time: datetime):
        reminder_time = appointment_time - timedelta(days=1)
        self.reminders[patient_id] = reminder_time
        print(f"Reminder set for patient {patient_id} on {reminder_time.strftime('%Y-%m-%d %H:%M')}")

    async def check_reminders(self):
        now = datetime.now()
        reminders_to_send = []
        for patient_id, reminder_time in self.reminders.items():
            if now >= reminder_time:
                reminders_to_send.append(patient_id)
        
        for patient_id in reminders_to_send:
            await self.send_reminder(patient_id)
            del self.reminders[patient_id]

    async def send_reminder(self, patient_id: str):
        appointment = next((apt for apt in self.appointments.values() if apt['patient_id'] == patient_id), None)
        if appointment:
            reminder_message = f"Reminder: You have an appointment tomorrow at {appointment['time']}"
            print(f"Sending reminder to patient {patient_id}: {reminder_message}")
            await self.event_bus.publish('reminder_sent', {'patient_id': patient_id, 'message': reminder_message})

    def get_appointment(self, patient_id: str) -> Dict[str, Any]:
        return next((apt for apt in self.appointments.values() if apt['patient_id'] == patient_id), None)