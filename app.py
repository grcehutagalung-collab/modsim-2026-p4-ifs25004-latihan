import numpy as np
from scipy.integrate import solve_ivp
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# =========================
# KONFIGURASI PARAMETER
# =========================

class CookingConfig:

    def __init__(self,
                 rice_mass=10,
                 water_mass=15,
                 burner_power=3000,
                 initial_temp=25,
                 target_temp=100,
                 ambient_temp=25,
                 simulation_time=60):

        self.rice_mass = rice_mass
        self.water_mass = water_mass
        self.burner_power = burner_power
        self.initial_temp = initial_temp
        self.target_temp = target_temp
        self.ambient_temp = ambient_temp
        self.simulation_time = simulation_time

        self.Cp_water = 4186
        self.Cp_rice = 2000
        self.pan_mass = 5
        self.Cp_pan = 500
        self.heating_efficiency = 0.7

        self.total_mass = self.rice_mass + self.water_mass

# =========================
# MODEL FISIKA
# =========================

class PhysicsModel:

    def __init__(self, config):
        self.config = config

    def heat_input(self, T):

        if T < self.config.target_temp:
            return self.config.burner_power * self.config.heating_efficiency

        return 0

    def heat_loss(self, T):

        return (T - self.config.ambient_temp) * 10

    def heat_capacity(self):

        Cp_mix = (self.config.water_mass * self.config.Cp_water +
                  self.config.rice_mass * self.config.Cp_rice)

        Cp_total = Cp_mix + self.config.pan_mass * self.config.Cp_pan

        return Cp_total

# =========================
# SISTEM PERSAMAAN
# =========================

class DifferentialEquations:

    def __init__(self, physics):

        self.physics = physics
        self.config = physics.config

    def equations(self, t, y):

        T, water = y

        Q_in = self.physics.heat_input(T)
        Q_loss = self.physics.heat_loss(T)

        Cp = self.physics.heat_capacity()

        dTdt = (Q_in - Q_loss) / Cp

        evap = 0

        if T >= 100:
            evap = 0.0001
        dWdt = -evap

        return [dTdt, dWdt]

# =========================
# SIMULATOR
# =========================

class RiceCookingSimulator:

    def __init__(self, config):

        self.config = config
        self.physics = PhysicsModel(config)
        self.eq = DifferentialEquations(self.physics)

    def run(self):

        t_span = (0, self.config.simulation_time * 60)

        t_eval = np.linspace(0,
                             self.config.simulation_time * 60,
                             500)

        y0 = [self.config.initial_temp,
              self.config.water_mass]

        sol = solve_ivp(self.eq.equations,
                        t_span,
                        y0,
                        t_eval=t_eval)

        time = sol.t / 60
        temp = sol.y[0]
        water = sol.y[1]

        return time, temp, water

# =========================
# STREAMLIT APP
# =========================

def main():

    st.title("🍚 Simulasi Proses Memasak Nasi")

    st.sidebar.header("Parameter")

    rice_mass = st.sidebar.slider("Massa Beras (kg)",1.0,20.0,10.0)

    water_mass = st.sidebar.slider("Massa Air (kg)",5.0,30.0,15.0)

    burner_power = st.sidebar.slider("Daya Kompor (W)",1000,5000,3000)

    simulation_time = st.sidebar.slider("Waktu Simulasi (menit)",10,120,60)

    config = CookingConfig(
        rice_mass=rice_mass,
        water_mass=water_mass,
        burner_power=burner_power,
        simulation_time=simulation_time
    )

    simulator = RiceCookingSimulator(config)

    time, temp, water = simulator.run()

    st.subheader("Grafik Suhu")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time,
        y=temp,
        mode="lines",
        name="Suhu"
    ))

    fig.add_hline(y=100,line_dash="dash")

    fig.update_layout(
        xaxis_title="Waktu (menit)",
        yaxis_title="Suhu (°C)"
    )

    st.plotly_chart(fig)

    st.subheader("Grafik Kandungan Air")

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=time,
        y=water,
        mode="lines",
        name="Air"
    ))

    fig2.update_layout(
        xaxis_title="Waktu (menit)",
        yaxis_title="Massa Air (kg)"
    )

    st.plotly_chart(fig2)

    df = pd.DataFrame({
        "Waktu (menit)": time,
        "Suhu": temp,
        "Air": water
    })

    st.subheader("Data Simulasi")

    st.dataframe(df)

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Data",
        csv,
        "hasil_simulasi.csv"
    )

if __name__ == "__main__":
    main()