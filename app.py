import streamlit as st
import subprocess
import os

# User interface
st.set_page_config(page_title="UFSI Road Safety", layout="wide")
st.title("UFSI: Road Safety Scenario Interface")
st.markdown("### UK Road Safety & Infrastructure Validation")

# --- SIDEBAR: WORLD MANAGEMENT ---
st.sidebar.header("CARLA Management")

if st.sidebar.button("Initialize World (Town05)"):
    try:
        import carla
        import config 
        client = carla.Client(config.HOST, config.PORT)
        client.set_timeout(15.0)
        world = client.get_world()
        if "Town05" not in world.get_map().name:
            st.sidebar.warning("Switching to Town05...")
            client.load_world('Town05')
            st.sidebar.success("Town05 Loaded!")
        else:
            st.sidebar.info("Town05 is already active.")
    except Exception as e:
        st.sidebar.error(f"Connection Failed: {e}")

if st.sidebar.button("Clear All Actors"):
    subprocess.run(["py", "-3.12", "cleanup.py"])
    st.sidebar.warning("All vehicles and sensors removed.")

# --- MAIN PANEL ---
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    target_speed = st.slider("Cruising Speed (mph)", min_value=20, max_value=70, value=30, step=10)
with col2:
    prt_map = {"Robot (0.0s)": 0.0, "Alert (0.7s)": 0.7, "Surprise (1.5s)": 1.5, "Design Standard (2.5s)": 2.5}
    prt_label = st.selectbox("Driver Reaction Time (PRT)", list(prt_map.keys()))

selected_prt = prt_map[prt_label]

scenario = st.selectbox("Select Validation Scenario", [
    "Straight Line Stop Test", 
    "Hazard Following Test", 
    "Kinetic Energy Calculation",
])

# --- SCENARIO DESCRIPTIONS ---
descriptions = {
    "Straight Line Stop Test": """
    ### About: Emergency Braking Distance (SSD Validation)
    **What it tests:** This scenario validates the total distance required for a vehicle to come to a complete stop from a steady speed. It compares the simulation's results against the **Highway Code** and **Stopping Sight Distance (SSD)** benchmarks used in UK road design.
    
    **Mathematical Framework:**
    * **Thinking Distance:** The distance covered during the Perception-Reaction Time.
    $$d_{t} = v \cdot t_{prt}$$
    * **Braking Distance:** The physical distance required to dissipate kinetic energy via friction.
    $$d_{b} = \\frac{v^2}{2 \cdot \\mu \cdot g}$$
    
    **Infrastructure Context:** This validates whether the "visibility splay" at a junction or the "sightline" on a curve provides enough distance for a driver to see an object and stop before impact.
    """,
    "Hazard Following Test": """
    ### About: Lead Vehicle Braking (The 'Safety Gap' Analysis)
    **What it tests:** This simulates a high-risk "convoy" event. A lead vehicle performs an emergency stop, and the Ego vehicle must react. It tests if the legal 'Safe Gap' (e.g., the 2-second rule) is sufficient when accounting for human PRT.
    
    **Mathematical Framework:**
    * **Total Stopping Distance ($d_{total}$):**
    $$d_{total} = (v \cdot t_{prt}) + \\frac{v^2}{2 \cdot \\mu \cdot g}$$
    * **Safety Margin Result:** $$Margin = Gap_{initial} - (d_{thinking\_ego} + d_{braking\_ego} - d_{braking\_lead})$$
    
    **Infrastructure Context:** This proves that 'Safe Gaps' are not static. It highlights how distraction or fatigue (high PRT) can cause a collision even if the vehicles are technically following at the 'legal' distance.
    """,
    "Kinetic Energy Calculation": """
    ### About: Kinetic Energy & Passive Safety (BS EN 12767)
    **What it tests:** This scenario focuses on the physics of the crash itself. It calculates the energy an object (like a signpost or barrier) must absorb to protect occupants during a high-speed collision.
    
    **Mathematical Framework:**
    * **Kinetic Energy ($E_{k}$):**
    $$E_{k} = \\frac{1}{2} m v^2$$
    * **Fall Height Equivalency ($h$):** Visualizes the impact energy as a vertical fall from a building.
    $$h = \\frac{E_{k}}{m \cdot g}$$
    
    **Infrastructure Context:** This ties directly into **BS EN 12767**, the standard for the passive safety of support structures. It demonstrates why "soft" or "forgiving" infrastructure is required at higher speed limits.
    """
}

st.markdown(descriptions.get(scenario, "Select a scenario to see details."))

# --- EXECUTION ---
col_run, col_batch = st.columns(2)

with col_run:
    if st.button("Run Stop Test", use_container_width=True):
        st.info(f"Launching {scenario}...")
        
        file_map = {
            "Straight Line Stop Test": "test_straight_line.py",
            "Hazard Following Test": "test_following_distance.py",
            "Kinetic Energy Calculation": "test_motorway.py",
        }
        
        script_to_run = file_map.get(scenario)
        selected_prt = prt_map[prt_label]

        try:
            # Execute the simulation script
            result = subprocess.run(["py", "-3.12", script_to_run, str(target_speed), str(selected_prt)], capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success(f"Test Complete: {scenario}")
                st.code(result.stdout)
                
                # 1. DEFINE STATUS
                if "FAIL" in result.stdout or "DANGEROUS" in result.stdout:
                    status = "FAIL (DANGEROUS)"
                else:
                    status = "PASS (SAFE)"

                # 2. REFINED DATA SCRAPING (Isolating Sim Result from Benchmark)
                extracted_val = "N/A"
                for line in result.stdout.split('\n'):
                    # Search for keywords used across all three test console outputs
                    if any(x in line for x in ["Total Stop Dist:", "Final Bumper Gap:", "Energy:"]):
                        # Splitting by '|' ensures we take only the actual simulation result 
                        parts = line.split('|')
                        extracted_val = parts[0].split(':')[-1].strip()

                # 3. BESPOKE REPORT ROUTING (Standardized Styling)
                if scenario == "Straight Line Stop Test":
                    import report_stop
                    report_file = report_stop.generate_pdf(scenario, target_speed, selected_prt, status, extracted_val)
                    
                elif scenario == "Hazard Following Test":
                    import report_hazard
                    report_file = report_hazard.generate(target_speed, selected_prt, status, extracted_val)
                    
                elif scenario == "Kinetic Energy Calculation":
                    import report_energy
                    report_file = report_energy.generate(target_speed, selected_prt, extracted_val)

                # 4. DOWNLOAD BUTTON
                with open(report_file, "rb") as f:
                    st.download_button(f"📄 Download Forensic {scenario} Report", f, file_name=report_file, use_container_width=True)
                    
        except Exception as e:
            st.error(f"UI Error: {e}")

with col_batch:
    if st.button("Run Batch Validation (20-70 MPH)", use_container_width=True):
        st.warning("Executing Batch Mode. Results will be logged to results_data/.")
        progress_bar = st.progress(0)
        speeds = [20, 30, 40, 50, 60, 70]
        # Using straight line as the primary benchmark script [cite: 247, 322]
        for i, s in enumerate(speeds):
            subprocess.run(["py", "-3.12", "test_straight_line.py", str(s), str(selected_prt)])
            progress_bar.progress((i + 1) / len(speeds))
        st.success("Batch Complete! You can now analyze the CSV files in your project folder.")