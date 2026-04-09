from fpdf import FPDF
from datetime import datetime
import math

class SafetyReport(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 20, 'UFSI: ROAD SAFETY VALIDATION REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 0, 'Scenario stress-testing against UK Department for Transport standards', 0, 1, 'C')
        self.ln(20)

def generate_pdf(scenario, speed, prt, status, sim_dist="N/A"):
    pdf = SafetyReport()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # 1. TEST SUMMARY
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Report ID: UFSI-{datetime.now().strftime('%Y%H%M')}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d %B %Y')}", ln=True)
    pdf.ln(5)

    # 2. INPUT CONFIGURATION (MEETING FR2)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 1. SYSTEM CONFIGURATION & PARAMETERS", 1, 1, 'L', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(95, 10, f" Target Velocity: {speed} MPH", 1, 0)
    pdf.cell(95, 10, f" Perception-Reaction Time (PRT): {prt}s", 1, 1)
    pdf.cell(190, 10, f" Test Environment: CARLA Digital Twin (Town05 - Motorway)", 1, 1)
    pdf.ln(5)

    # 3. TECHNICAL PHYSICS ANALYSIS (NFR3)
    v_ms = speed * 0.44704
    ke_kj = 0.5 * 1800 * (v_ms**2) / 1000 
    thinking_dist = v_ms * prt
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 2. FORENSIC PHYSICS BREAKDOWN", 1, 1, 'L', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 10, f" Critical Thinking Distance: {thinking_dist:.2f} meters", 1, 1)
    pdf.cell(190, 10, f" Kinetic Energy at Hazard Trigger: {ke_kj:.2f} kJ", 1, 1)
    pdf.cell(190, 10, f" Fall Height Equivalency: Like falling from a {ke_kj/17.65:.1f}m building", 1, 1)
    pdf.ln(5)

    # 4. SIMULATION PERFORMANCE DATA
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 3. SIMULATION DATA ACQUISITION", 1, 1, 'L', 1)
    pdf.set_font("Arial", '', 10)
    
    hc_benchmarks = {20: 12, 30: 23, 40: 36, 50: 53, 60: 73, 70: 96, 90: 151}
    bench = hc_benchmarks.get(int(speed), 0)
    
    pdf.cell(95, 10, f" UK Statutory Requirement (SSD):", 1, 0)
    pdf.cell(95, 10, f" {bench} meters", 1, 1)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, f" Actual Simulated Stopping Distance:", 1, 0)
    pdf.cell(95, 10, f" {sim_dist}", 1, 1) 
    
    # Calculate Safety Margin
    try:
        actual_val = float(str(sim_dist).replace('m', '').strip())
        diff = bench - actual_val
        margin_text = f"Safety Margin: {diff:.2f}m" if diff > 0 else f"Safety Deficit: {abs(diff):.2f}m"
        pdf.cell(190, 10, f" {margin_text}", 1, 1)
    except:
        pdf.cell(190, 10, " Margin Calculation: Data Unavailable", 1, 1)
    
    pdf.ln(5)

    # 5. FINAL SAFETY VERDICT
    pdf.set_font("Arial", 'B', 12)
    color = (200, 0, 0) if "FAIL" in status else (0, 128, 0)
    pdf.set_text_color(*color)
    pdf.cell(0, 10, f"SAFETY VERDICT: {status}", 1, 1, 'C')
    
    # 6. INFRASTRUCTURE RECOMMENDATION
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 10)
    pdf.ln(5)
    recommendation = "Maintain current signage." if "PASS" in status else "ACTION REQUIRED: Recommend reduction in speed limit or extension of visibility splay."
    pdf.multi_cell(0, 8, f"Recommendation: {recommendation}")

    filename = f"Detailed_Safety_Report_{speed}mph.pdf"
    pdf.output(filename)
    return filename