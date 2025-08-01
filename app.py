import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Sustainable Electricity Prototype", layout="wide")

st.title("♻️ Sustainable Electricity System Prototype")
st.markdown("This is a **virtual prototype** simulating electricity generation using geothermal and wasted energy sources, AI pipe monitoring, and two-level TEG recovery.")

# --- Sidebar Controls ---
st.sidebar.header("Simulation Controls")
geothermal_temp = st.sidebar.slider("Geothermal Heat (°C)", 300, 900, 600)
wasted_energy_input = st.sidebar.slider("Wasted Energy Input (kWh)", 10, 200, 80)
teg_device_level = st.sidebar.slider("TEG Device Recovery (%)", 0, 50, 15)
teg_system_level = st.sidebar.slider("TEG System Recovery (%)", 0, 50, 20)
pipe_health = st.sidebar.slider("Pipe Health (%)", 0, 100, 100)
storage_capacity = st.sidebar.slider("Battery Storage Capacity (kWh)", 100, 1000, 500)

# --- Energy Generation Functions ---
def geothermal_energy(temp):
    return 0.5 * temp  # Simplified: higher temp, more output

def wasted_energy_recovery(wasted):
    return 0.7 * wasted  # 70% usable from wasted energy

def calculate_teg_recovery(usage, device_pct, system_pct):
    return usage * (device_pct + system_pct) / 100

def monitor_pipe(health):
    if health < 40:
        return "⚠️ Warning: Pipe needs replacement!", 0.6
    elif health < 70:
        return "🔶 Pipe condition moderate. Monitoring closely.", 0.8
    else:
        return "✅ Pipe health optimal.", 1.0

# --- Simulated Energy Outputs ---
geo_output = geothermal_energy(geothermal_temp)
waste_output = wasted_energy_recovery(wasted_energy_input)
teg_recovery = calculate_teg_recovery(waste_output + geo_output, teg_device_level, teg_system_level)
pipe_status_msg, pipe_efficiency = monitor_pipe(pipe_health)

# Final energy output (before storage)
total_output = (geo_output + waste_output + teg_recovery) * pipe_efficiency

# --- Simulate Energy Storage ---
charge = min(total_output, storage_capacity)
discharge = charge * 0.75  # 75% usable later due to battery loss

# --- Tabs UI ---
tab1, tab2, tab3 = st.tabs(["🔋 Output Summary", "📊 Graph", "🤖 AI & TEG"])

with tab1:
    st.subheader("📦 Energy Summary")
    st.metric("Geothermal Output (kWh)", f"{geo_output:.2f}")
    st.metric("Wasted Energy Recovery (kWh)", f"{waste_output:.2f}")
    st.metric("TEG Recovery (kWh)", f"{teg_recovery:.2f}")
    st.metric("Pipe Efficiency Factor", f"{pipe_efficiency:.2f}")
    st.metric("Total Generated (kWh)", f"{total_output:.2f}")
    st.metric("Stored Energy (kWh)", f"{charge:.2f}")
    st.metric("Future Discharge (kWh)", f"{discharge:.2f}")
    st.success(pipe_status_msg)

with tab2:
    st.subheader("📈 Power Output Over Time")
    hours = np.arange(0, 24, 1)
    generation = total_output * np.sin(np.pi * hours / 24)**2
    fig, ax = plt.subplots()
    ax.plot(hours, generation, label="Energy Output (kWh)", color="green")
    ax.set_xlabel("Time (Hours)")
    ax.set_ylabel("Energy")
    ax.legend()
    st.pyplot(fig)

with tab3:
    st.subheader("🤖 AI Monitoring + TEG Placement")
    st.markdown("""
    - AI continuously monitors **pipe health**, triggering alerts and replacements automatically.
    - TEGs installed:
        - **Device-Level**: Captures heat from electronics (fans, lights, TVs).
        - **System-Level**: Captures residual heat in transmission systems.
    - Two **separate steam generators** process heat from geothermal and wasted energy sources.
    - System automatically redirects inputs and logs data for smart grid optimization.
    """)

# Footer
st.markdown("---")
st.caption("Prototype by [Retina Majumder], Age 16 — Sustainable Electricity Innovator 🌍")
