from typing import Dict, Any, List
from datetime import datetime

class StakeholderModule:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.patients = {}
        self.professionals = {}
        self.administrators = {}
        self.thhs_reports = []

    async def register_patient(self, patient_data: Dict[str, Any]):
        patient_id = patient_data['id']
        self.patients[patient_id] = patient_data
        await self.event_bus.publish('patient_registered', {'patient_id': patient_id})

    async def update_patient_data(self, patient_id: str, updated_data: Dict[str, Any]):
        if patient_id in self.patients:
            self.patients[patient_id].update(updated_data)
            await self.event_bus.publish('patient_data_updated', {'patient_id': patient_id})
        else:
            raise ValueError(f"Patient with ID {patient_id} not found")

    async def register_professional(self, professional_data: Dict[str, Any]):
        professional_id = professional_data['id']
        self.professionals[professional_id] = professional_data
        await self.event_bus.publish('professional_registered', {'professional_id': professional_id})

    async def assign_patient_to_professional(self, patient_id: str, professional_id: str):
        if patient_id in self.patients and professional_id in self.professionals:
            self.patients[patient_id]['assigned_professional'] = professional_id
            await self.event_bus.publish('patient_assigned', {'patient_id': patient_id, 'professional_id': professional_id})
        else:
            raise ValueError("Invalid patient or professional ID")

    async def register_administrator(self, admin_data: Dict[str, Any]):
        admin_id = admin_data['id']
        self.administrators[admin_id] = admin_data
        await self.event_bus.publish('administrator_registered', {'admin_id': admin_id})

    async def generate_clinic_report(self, admin_id: str) -> Dict[str, Any]:
        if admin_id not in self.administrators:
            raise ValueError(f"Administrator with ID {admin_id} not found")
        
        report = {
            'total_patients': len(self.patients),
            'total_professionals': len(self.professionals),
            'patient_professional_ratio': len(self.patients) / len(self.professionals) if len(self.professionals) > 0 else 0,
            'generated_at': datetime.now().isoformat()
        }
        await self.event_bus.publish('clinic_report_generated', {'admin_id': admin_id})
        return report

    async def submit_thhs_report(self, report_data: Dict[str, Any]):
        self.thhs_reports.append(report_data)
        await self.event_bus.publish('thhs_report_submitted', {'report_id': len(self.thhs_reports) - 1})

    async def get_thhs_reports(self) -> List[Dict[str, Any]]:
        return self.thhs_reports

    # Patient interface methods
    async def get_patient_data(self, patient_id: str) -> Dict[str, Any]:
        if patient_id in self.patients:
            return self.patients[patient_id]
        else:
            raise ValueError(f"Patient with ID {patient_id} not found")

    async def get_patient_appointments(self, patient_id: str) -> List[Dict[str, Any]]:
        # This would typically interact with a scheduler module
        # For now, we'll return a placeholder
        return [{'date': '2023-07-20', 'time': '14:00', 'professional': 'Dr. Smith'}]

    # Professional interface methods
    async def get_professional_patients(self, professional_id: str) -> List[Dict[str, Any]]:
        if professional_id in self.professionals:
            return [patient for patient in self.patients.values() if patient.get('assigned_professional') == professional_id]
        else:
            raise ValueError(f"Professional with ID {professional_id} not found")

    async def update_patient_treatment_plan(self, professional_id: str, patient_id: str, treatment_plan: Dict[str, Any]):
        if professional_id in self.professionals and patient_id in self.patients:
            self.patients[patient_id]['treatment_plan'] = treatment_plan
            await self.event_bus.publish('treatment_plan_updated', {'patient_id': patient_id, 'professional_id': professional_id})
        else:
            raise ValueError("Invalid professional or patient ID")

    # Administrator interface methods
    async def get_clinic_statistics(self, admin_id: str) -> Dict[str, Any]:
        if admin_id in self.administrators:
            return {
                'total_patients': len(self.patients),
                'total_professionals': len(self.professionals),
                'total_administrators': len(self.administrators),
                'recent_thhs_reports': len(self.thhs_reports)
            }
        else:
            raise ValueError(f"Administrator with ID {admin_id} not found")

# Example usage
async def main():
    from utils.event_bus import EventBus
    event_bus = EventBus()
    stakeholder_module = StakeholderModule(event_bus)

    # Register a patient
    await stakeholder_module.register_patient({'id': 'P001', 'name': 'John Doe', 'age': 30})

    # Register a professional
    await stakeholder_module.register_professional({'id': 'PR001', 'name': 'Dr. Smith', 'specialization': 'Psychiatrist'})

    # Assign patient to professional
    await stakeholder_module.assign_patient_to_professional('P001', 'PR001')

    # Register an administrator
    await stakeholder_module.register_administrator({'id': 'A001', 'name': 'Admin User'})

    # Generate clinic report
    report = await stakeholder_module.generate_clinic_report('A001')
    print("Clinic Report:", report)

    # Submit THHS report
    await stakeholder_module.submit_thhs_report({'date': '2023-07-15', 'content': 'Monthly clinic performance report'})

    # Get professional's patients
    patients = await stakeholder_module.get_professional_patients('PR001')
    print("Dr. Smith's patients:", patients)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())