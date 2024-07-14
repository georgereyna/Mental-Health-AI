# run, start new terminal, cd frontend, npm start

import sys
import os
import asyncio
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from typing import Dict, Any

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the event bus and modules
from utils.event_bus import EventBus
from modules.intake_module import IntakeModule
from modules.scheduler_module import SchedulerModule
from modules.documentation_module import DocumentationModule
from modules.nlp_module import NLPModule
from modules.ml_module import MLModule
from modules.cultural_sensitivity_module import CulturalSensitivityModule
from modules.progress_monitoring_module import ProgressMonitoringModule
from modules.crisis_detection_module import CrisisDetectionModule
from modules.treatment_plan_module import TreatmentPlanModule
from modules.continuous_learning_module import ContinuousLearningModule
from modules.api_integration import APIIntegrationModule
from modules.hipaa_compliance_module import HIPAAComplianceModule
from modules.ethics_module import EthicsModule
from modules.secure_database import SecureDatabase
from modules.symptom_tracking_module import SymptomTrackingModule
from modules.ehr_integration_module import EHRIntegrationModule
from modules.user_interface import UserInterfaceModule
from modules.data_sources_module import DataSourcesModule
from modules.stakeholder_module import StakeholderModule
from modules.compliance_module import ComplianceModule
from modules.performance_metrics_module import PerformanceMetricsModule
from modules.challenges_module import ChallengesModule

app = Flask(__name__)
event_bus = EventBus()

async def setup_modules(event_bus):
    secure_db = SecureDatabase()
    intake_module = IntakeModule(event_bus)
    scheduler_module = SchedulerModule(event_bus)
    documentation_module = DocumentationModule(event_bus)
    nlp_module = NLPModule()
    ml_module = MLModule()
    cultural_sensitivity_module = CulturalSensitivityModule(event_bus)
    progress_monitoring_module = ProgressMonitoringModule(event_bus)
    crisis_detection_module = CrisisDetectionModule(event_bus)
    treatment_plan_module = TreatmentPlanModule(event_bus)
    continuous_learning_module = ContinuousLearningModule(event_bus)
    api_integration_module = APIIntegrationModule(event_bus)
    hipaa_compliance_module = HIPAAComplianceModule(event_bus)
    ethics_module = EthicsModule(event_bus)
    symptom_tracking_module = SymptomTrackingModule(event_bus)
    ehr_integration_module = EHRIntegrationModule(event_bus)
    user_interface = UserInterfaceModule(event_bus)
    data_sources_module = DataSourcesModule()
    stakeholder_module = StakeholderModule(event_bus)
    compliance_module = ComplianceModule(event_bus)
    performance_metrics_module = PerformanceMetricsModule(event_bus)
    challenges_module = ChallengesModule(event_bus)
    
    return {
        'user_interface': user_interface,
        'nlp_module': nlp_module,
        'ml_module': ml_module,
        'secure_database': secure_db,
        'api_integration': api_integration_module,
        'intake_module': intake_module,
        'scheduler_module': scheduler_module,
        'treatment_plan_module': treatment_plan_module,
        'symptom_tracking_module': symptom_tracking_module,
        'progress_monitoring_module': progress_monitoring_module,
        'crisis_detection_module': crisis_detection_module,
        'performance_metrics_module': performance_metrics_module
    }

modules = asyncio.run(setup_modules(event_bus))

@app.route('/api/patient/<id>')
def patient_interface(id):
    data = asyncio.run(modules['user_interface'].get_patient_interface(id))
    return jsonify(data)

@app.route('/api/clinician/<id>')
def clinician_interface(id):
    data = asyncio.run(modules['user_interface'].get_clinician_interface(id))
    return jsonify(data)

@app.route('/api/admin/<id>')
def admin_interface(id):
    data = asyncio.run(modules['user_interface'].get_admin_interface(id))
    return jsonify(data)

@app.route('/api/symptom_tracking', methods=['POST'])
def track_symptom():
    data = request.json
    result = asyncio.run(modules['symptom_tracking_module'].log_symptom(data['patient_id'], data['symptom_data']))
    return jsonify(result)

@app.route('/api/schedule_appointment', methods=['POST'])
def schedule_appointment():
    data = request.json
    result = asyncio.run(modules['scheduler_module'].schedule_appointment(data))
    return jsonify(result)

@app.route('/api/generate_treatment_plan', methods=['POST'])
def generate_treatment_plan():
    data = request.json
    result = asyncio.run(modules['treatment_plan_module'].generate_treatment_plan(data))
    return jsonify(result)

@app.route('/api/detect_crisis', methods=['POST'])
def detect_crisis():
    data = request.json
    result = asyncio.run(modules['crisis_detection_module'].assess_crisis(data))
    return jsonify(result)

@app.route('/api/performance_metrics')
def get_performance_metrics():
    result = asyncio.run(modules['performance_metrics_module'].generate_performance_report())
    return jsonify(result)

async def demonstrate_modules(modules):
    print("\nDemonstrating Symptom Tracking:")
    symptom_data = {
        'patient_id': '12345',
        'symptom': 'Feeling sad',
        'severity': 8,
        'notes': 'Patient has been feeling sad for several weeks.'
    }
    await modules['symptom_tracking_module'].log_symptom('12345', symptom_data)

    print("\nDemonstrating Treatment Plan Handling:")
    treatment_plan_data = {
        'patient_id': '12345',
        'plan': 'Start CBT and schedule weekly sessions.'
    }
    await modules['treatment_plan_module'].generate_treatment_plan(treatment_plan_data)

    print("\nDemonstrating Appointment Scheduling:")
    appointment_data = {
        'patient_id': '12345',
        'date': '2023-07-14',
        'time': '10:00'
    }
    await modules['scheduler_module'].schedule_appointment(appointment_data)

    print("\nDemonstrating Progress Monitoring:")
    progress_data = {
        'patient_id': '12345',
        'progress_notes': 'Patient shows improvement after 3 sessions.'
    }
    await modules['progress_monitoring_module'].update_progress(progress_data)

    print("\nDemonstrating HIPAA Compliance Check:")
    await event_bus.publish('hipaa_compliance_check', {})

    print("\nDemonstrating EHR Integration:")
    ehr_request_data = {
        'patient_id': '12345',
        'request_type': 'retrieve'
    }
    await event_bus.publish('ehr_request', ehr_request_data)

    print("\nDemonstrating NLP Module:")
    nlp_data = {
        'text': 'I have been feeling very anxious and cannot sleep.'
    }
    nlp_result = modules['nlp_module'].process_text(nlp_data)
    print(f"NLP Result: {nlp_result}")

    print("\nDemonstrating ML Module:")
    ml_data = {
        'features': [5.1, 3.5, 1.4, 0.2]
    }
    ml_result = await modules['ml_module'].predict(ml_data)
    print(f"ML Result: {ml_result}")

    print("\nDemonstrating Secure Database:")
    patient_data = {
        'name': 'John Doe',
        'age': 30,
        'diagnosis': 'Anxiety disorder',
        'treatment': 'CBT'
    }
    modules['secure_database'].insert_patient('12345', patient_data)
    print("Patient data inserted.")
    retrieved_data = modules['secure_database'].get_patient('12345')
    print(f"Retrieved patient data: {retrieved_data}")

    print("\nDemonstrating API Integration:")
    api_integration_status = modules['api_integration'].get_integration_status()
    print(f"API Integration Status: {api_integration_status}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        asyncio.run(demonstrate_modules(modules))
    else:
        print("Starting Flask server...")
        app.run(debug=True)