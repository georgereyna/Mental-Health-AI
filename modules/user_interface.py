from typing import Dict, Any, List
from src.utils.event_bus import EventBus
import asyncio

class UserInterfaceModule:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def get_patient_interface(self, patient_id: str) -> Dict[str, Any]:
        appointments = await self.get_patient_appointments(patient_id)
        symptoms = await self.get_patient_symptoms(patient_id)
        treatment_plan = await self.get_patient_treatment_plan(patient_id)
        
        return {
            "component": "PatientDashboard",
            "props": {
                "patientId": patient_id,
                "appointments": appointments,
                "symptoms": symptoms,
                "treatmentPlan": treatment_plan
            }
        }

    async def get_clinician_interface(self, clinician_id: str) -> Dict[str, Any]:
        patients = await self.get_clinician_patients(clinician_id)
        appointments = await self.get_clinician_appointments(clinician_id)
        alerts = await self.get_clinician_alerts(clinician_id)
        
        return {
            "component": "ClinicianDashboard",
            "props": {
                "clinicianId": clinician_id,
                "patients": patients,
                "appointments": appointments,
                "alerts": alerts
            }
        }

    async def get_admin_interface(self, admin_id: str) -> Dict[str, Any]:
        clinic_stats = await self.get_clinic_stats()
        compliance_reports = await self.get_compliance_reports()
        staff_performance = await self.get_staff_performance()
        
        return {
            "component": "AdminDashboard",
            "props": {
                "adminId": admin_id,
                "clinicStats": clinic_stats,
                "complianceReports": compliance_reports,
                "staffPerformance": staff_performance
            }
        }

    async def get_patient_appointments(self, patient_id: str) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_patient_appointments', {'patient_id': patient_id})
        return response.get('appointments', []) if response else []

    async def get_patient_symptoms(self, patient_id: str) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_patient_symptoms', {'patient_id': patient_id})
        return response.get('symptoms', []) if response else []

    async def get_patient_treatment_plan(self, patient_id: str) -> Dict[str, Any]:
        response = await self.event_bus.publish('get_treatment_plan', {'patient_id': patient_id})
        return response.get('treatment_plan', {}) if response else {}

    async def get_clinician_patients(self, clinician_id: str) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_clinician_patients', {'clinician_id': clinician_id})
        return response.get('patients', []) if response else []

    async def get_clinician_appointments(self, clinician_id: str) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_clinician_appointments', {'clinician_id': clinician_id})
        return response.get('appointments', []) if response else []

    async def get_clinician_alerts(self, clinician_id: str) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_clinician_alerts', {'clinician_id': clinician_id})
        return response.get('alerts', []) if response else []

    async def get_clinic_stats(self) -> Dict[str, Any]:
        response = await self.event_bus.publish('get_clinic_stats', {})
        return response.get('stats', {}) if response else {}

    async def get_compliance_reports(self) -> List[Dict[str, Any]]:
        response = await self.event_bus.publish('get_compliance_reports', {})
        return response.get('reports', []) if response else []

    async def get_staff_performance(self) -> Dict[str, Any]:
        response = await self.event_bus.publish('get_staff_performance', {})
        return response.get('performance', {}) if response else {}

    async def log_patient_symptom(self, patient_id: str, symptom_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.event_bus.publish('log_patient_symptom', {
            'patient_id': patient_id,
            'symptom_data': symptom_data
        })
        return response if response else {}

    async def update_treatment_plan(self, patient_id: str, treatment_plan: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.event_bus.publish('update_treatment_plan', {
            'patient_id': patient_id,
            'treatment_plan': treatment_plan
        })
        return response if response else {}

    async def schedule_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.event_bus.publish('schedule_appointment', appointment_data)
        return response if response else {}

    async def generate_compliance_report(self, report_type: str) -> Dict[str, Any]:
        response = await self.event_bus.publish('generate_compliance_report', {'report_type': report_type})
        return response if response else {}

    async def handle_crisis_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.event_bus.publish('handle_crisis_alert', alert_data)
        return response if response else {}

    async def run_interface(self):
        while True:
            print("\n--- Mental Health Clinic AI System ---")
            print("1. Patient Interface")
            print("2. Clinician Interface")
            print("3. Administrator Interface")
            print("4. Exit")
            
            choice = input("Select an interface (1-4): ")
            
            if choice == '1':
                patient_id = input("Enter patient ID: ")
                interface_data = await self.get_patient_interface(patient_id)
                print(f"Patient Interface Data: {interface_data}")
            elif choice == '2':
                clinician_id = input("Enter clinician ID: ")
                interface_data = await self.get_clinician_interface(clinician_id)
                print(f"Clinician Interface Data: {interface_data}")
            elif choice == '3':
                admin_id = input("Enter admin ID: ")
                interface_data = await self.get_admin_interface(admin_id)
                print(f"Admin Interface Data: {interface_data}")
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

            # Simulate some processing time
            await asyncio.sleep(1)

    async def display_patient_dashboard(self, patient_id: str):
        interface_data = await self.get_patient_interface(patient_id)
        print("\n--- Patient Dashboard ---")
        print(f"Patient ID: {patient_id}")
        print("Appointments:")
        for apt in interface_data['props']['appointments']:
            print(f"  - Date: {apt['date']}, Time: {apt['time']}, With: {apt['doctor']}")
        print("Recent Symptoms:")
        for symptom in interface_data['props']['symptoms']:
            print(f"  - {symptom['name']}: Severity {symptom['severity']}, Recorded on {symptom['date']}")
        print("Treatment Plan:")
        plan = interface_data['props']['treatmentPlan']
        print(f"  Description: {plan['description']}")
        print("  Steps:")
        for step in plan['steps']:
            print(f"    - {step}")

    async def display_clinician_dashboard(self, clinician_id: str):
        interface_data = await self.get_clinician_interface(clinician_id)
        print("\n--- Clinician Dashboard ---")
        print(f"Clinician ID: {clinician_id}")
        print("Today's Appointments:")
        for apt in interface_data['props']['appointments']:
            print(f"  - Time: {apt['time']}, Patient: {apt['patientName']}, Reason: {apt['reason']}")
        print("Patient Alerts:")
        for alert in interface_data['props']['alerts']:
            print(f"  - Patient: {alert['patientName']}, Alert: {alert['message']}")
        print("My Patients:")
        for patient in interface_data['props']['patients']:
            print(f"  - Name: {patient['name']}, Last Visit: {patient['lastVisit']}")

    async def display_admin_dashboard(self, admin_id: str):
        interface_data = await self.get_admin_interface(admin_id)
        print("\n--- Admin Dashboard ---")
        print(f"Admin ID: {admin_id}")
        print("Clinic Statistics:")
        for stat, value in interface_data['props']['clinicStats'].items():
            print(f"  - {stat}: {value}")
        print("Compliance Reports:")
        for report in interface_data['props']['complianceReports']:
            print(f"  - Title: {report['title']}, Date: {report['date']}, Status: {report['status']}")
        print("Staff Performance:")
        for staff, perf in interface_data['props']['staffPerformance'].items():
            print(f"  - {staff}: Patients: {perf['patients']}, Satisfaction: {perf['satisfaction']}")

# Example usage
if __name__ == "__main__":
    event_bus = EventBus()
    ui_module = UserInterfaceModule(event_bus)
    asyncio.run(ui_module.run_interface())