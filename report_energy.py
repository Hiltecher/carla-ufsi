from fpdf import FPDF
from datetime import datetime

class EnergyReport(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59) # Standardized Slate Blue
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 20, 'UFSI: KINETIC ENERGY & IMPACT REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 0, 'Passive Safety Validation (BS EN 12767)', 0, 1, 'C')
        self.ln(20)

def generate(speed, prt, energy_val="N/A"):
    pdf = EnergyReport()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 1. IMPACT CONFIGURATION", 1, 1, 'L', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 10, f" Velocity at Hazard Event: {speed} MPH", 1, 1)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 2. FORENSIC PHYSICS BREAKDOWN", 1, 1, 'L', 1)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(95, 10, " Total Kinetic Energy:", 1, 0)
    pdf.cell(95, 10, f" {energy_val}", 1, 1)
    
    try:
        val = float(str(energy_val).replace('kJ', '').strip())
        height = val / (1800 * 9.81 / 1000)
        pdf.set_font("Arial", '', 10)
        pdf.cell(190, 10, f" Fall Height Equivalency: Like falling from a {height:.1f}m building", 1, 1)
    except: pass
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 3. INFRASTRUCTURE REQUIREMENTS (BS EN 12767)", 1, 1, 'L', 1)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 8, "Roadside structures must be designed to absorb this energy level. "
                          "High energy values require HE (High Energy Absorbing) supports.")

    filename = f"Energy_Report_{speed}mph.pdf"
    pdf.output(filename)
    return filename