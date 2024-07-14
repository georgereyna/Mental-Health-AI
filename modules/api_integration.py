# src/modules/api_integration.py

import asyncio
import json
from typing import Dict, Any

class MockExternalAPI:
    def __init__(self):
        self.ehr_data = {}
        self.schedule = {}

    async def get_patient_ehr(self, patient_id: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)  # Simulate network delay
        return self.ehr_data.get(patient_id, {"error": "Patient not found"})

    async def update_patient_ehr(self, patient_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.5)  # Simulate network delay
        self.ehr_data[patient_id] = data
        return {"status": "success", "message": "EHR updated"}

    async def get_available_slots(self, date: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)  # Simulate network delay
        return self.schedule.get(date, {"error": "No slots available"})

    async def book_appointment(self, date: str, time: str, patient_id: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)  # Simulate network delay
        if date not in self.schedule:
            self.schedule[date] = {}
        if time in self.schedule[date]:
            return {"error": "Slot already booked"}
        self.schedule[date][time] = patient_id
        return {"status": "success", "message": "Appointment booked"}

class APIIntegrationModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.external_api = MockExternalAPI()
        self.event_bus.subscribe('ehr_request', self.handle_ehr_request)
        self.event_bus.subscribe('ehr_update', self.handle_ehr_update)
        self.event_bus.subscribe('schedule_request', self.handle_schedule_request)
        self.event_bus.subscribe('appointment_booking', self.handle_appointment_booking)

    async def handle_ehr_request(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        ehr_data = await self.external_api.get_patient_ehr(patient_id)
        await self.event_bus.publish('ehr_data', {'patient_id': patient_id, 'data': ehr_data})

    async def handle_ehr_update(self, data: Dict[str, Any]):
        patient_id = data['patient_id']
        update_data = data['update_data']
        result = await self.external_api.update_patient_ehr(patient_id, update_data)
        await self.event_bus.publish('ehr_update_result', {'patient_id': patient_id, 'result': result})

    async def handle_schedule_request(self, data: Dict[str, Any]):
        date = data['date']
        available_slots = await self.external_api.get_available_slots(date)
        await self.event_bus.publish('available_slots', {'date': date, 'slots': available_slots})

    async def handle_appointment_booking(self, data: Dict[str, Any]):
        date = data['date']
        time = data['time']
        patient_id = data['patient_id']
        booking_result = await self.external_api.book_appointment(date, time, patient_id)
        await self.event_bus.publish('booking_result', {'patient_id': patient_id, 'result': booking_result})

    def get_integration_status(self) -> Dict[str, Any]:
        return {
            "ehr_connection": "active",
            "scheduling_connection": "active",
            "last_sync": "2023-07-13T10:30:00Z"
        }