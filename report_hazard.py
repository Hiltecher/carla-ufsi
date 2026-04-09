from fpdf import FPDF
from datetime import datetime

class HazardReport(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59) # Standardized Slate Blue
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 20, 'UFSI: HAZARD FOLLOWING ANALYSIS', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 0, 'Stress-testing UK Safety Gaps & Human Reaction Factors', 0, 1, 'C')
        self.ln(20)

def generate(speed, prt, status, bumper_gap="N/A"):
    pdf = HazardReport()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # 1. SYSTEM CONFIGURATION
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 1. SYSTEM CONFIGURATION & PARAMETERS", 1, 1, 'L', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(95, 10, f" Closing Speed: {speed} MPH", 1, 0)
    pdf.cell(95, 10, f" Driver PRT Profile: {prt}s", 1, 1)
    pdf.ln(5)

    # 2. DATA ACQUISITION
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 2. SIMULATION DATA ACQUISITION", 1, 1, 'L', 1)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, " Final Bumper-to-Bumper Gap:", 1, 0)
    pdf.cell(95, 10, f" {bumper_gap}", 1, 1)
    pdf.ln(5)

    # 3. VERDICT
    pdf.set_font("Arial", 'B', 12)
    color = (200, 0, 0) if "FAIL" in status else (0, 128, 0)
    pdf.set_text_color(*color)
    pdf.cell(0, 15, f"SAFETY VERDICT: {status}", 1, 1, 'C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 10)
    pdf.ln(5)
    rec = "Gap sufficient for driver profile." if "PASS" in status else "ACTION: Recommend '2-second rule' enforcement."
    pdf.multi_cell(0, 8, f"Recommendation: {rec}")

    filename = f"Hazard_Report_{speed}mph.pdf"
    pdf.output(filename)
    return filename