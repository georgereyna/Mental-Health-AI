import sys
import os
import asyncio
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
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
CORS(app)
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

@app.route('/api/test')
def test_route():
    return jsonify({"message": "Test route is working"})

@app.route('/api/patient/<id>')
def patient_interface(id):
    print(f"Received request for patient {id}")
    try:
        # This is a mock response. Replace this with actual data retrieval logic.
        data = {
            "props": {
                "patientId": id,
                "appointments": [
                    {"date": "2023-07-20", "time": "10:00 AM"},
                    {"date": "2023-07-27", "time": "2:00 PM"}
                ],
                "symptoms": [
                    {"name": "Headache", "severity": 3},
                    {"name": "Fatigue", "severity": 2}
                ],
                "treatmentPlan": {
                    "description": "Rest and hydration"
                }
            }
        }
        print(f"Returning data for patient {id}: {data}")
        return jsonify(data)
    except Exception as e:
        print(f"Error processing request for patient {id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/clinician/<id>')
def clinician_interface(id):
    print(f"Received request for clinician {id}")
    try:
        data = asyncio.run(modules['user_interface'].get_clinician_interface(id))
        print(f"Returning data for clinician {id}: {data}")
        return jsonify(data)
    except Exception as e:
        print(f"Error processing request for clinician {id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/<id>')
def admin_interface(id):
    print(f"Received request for admin {id}")
    try:
        data = asyncio.run(modules['user_interface'].get_admin_interface(id))
        print(f"Returning data for admin {id}: {data}")
        return jsonify(data)
    except Exception as e:
        print(f"Error processing request for admin {id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

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

async def run_interactive_menu():
    while True:
        print("\n--- Mental Health Clinic AI System ---")
        print("1. Patient Interface")
        print("2. Clinician Interface")
        print("3. Administrator Interface")
        print("4. Exit")
        
        choice = input("Select an interface (1-4): ")
        
        if choice == '1':
            patient_id = input("Enter patient ID: ")
            data = await modules['user_interface'].get_patient_interface(patient_id)
            print(f"Patient Interface Data: {data}")
        elif choice == '2':
            clinician_id = input("Enter clinician ID: ")
            data = await modules['user_interface'].get_clinician_interface(clinician_id)
            print(f"Clinician Interface Data: {data}")
        elif choice == '3':
            admin_id = input("Enter admin ID: ")
            data = await modules['user_interface'].get_admin_interface(admin_id)
            print(f"Admin Interface Data: {data}")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        # Simulate some processing time
        await asyncio.sleep(1)

if __name__ == "__main__":
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")

    try:
        import cryptography
        print(f"Cryptography version: {cryptography.__version__}")
        print(f"Cryptography location: {cryptography.__file__}")
    except ImportError:
        print("Failed to import cryptography")
        print("Install cryptography using 'pip install cryptography'")

    print("1. Start Flask server")
    print("2. Run interactive menu")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=8000)
    elif choice == '2':
        print("Starting interactive menu...")
        asyncio.run(run_interactive_menu())
    else:
        print("Invalid choice. Exiting...")