
import streamlit as st
import math
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Q-Secure | Quantum Security Lab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .brand {
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #8b95a5;
        font-size: 0.95rem;
        margin-top: -12px;
    }

    div[data-testid="stSegmentedControl"] {
        margin-top: 8px;
        margin-bottom: 22px;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.07);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    .section-label {
        color: #8b95a5;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .info-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        '<div class="brand">🔐 Q-SECURE</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Quantum Computing & Cybersecurity Lab</div>',
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        "<div style='text-align:right;padding-top:12px;'>"
        "● Simulation Environment</div>",
        unsafe_allow_html=True
    )

st.divider()

# ---------- NAVIGATION ----------
page = st.segmented_control(
    "Main navigation",
    options=[
        "⌂  Dashboard",
        "⚛  Quantum Circuit",
        "◈  About"
    ],
    default="⌂  Dashboard",
    selection_mode="single",
    label_visibility="collapsed",
    key="main_navigation"
)

if page is None:
    page = "⌂  Dashboard"

st.write("")

# ---------- DASHBOARD ----------
if page == "⌂  Dashboard":

    st.title("Quantum Security Dashboard")
    st.write(
        "Explore how quantum search compares with "
        "classical search in an unstructured search problem."
    )

    n = st.slider(
        "Number of possible states",
        min_value=4,
        max_value=256,
        value=16,
        step=4
    )

    classical = n
    grover_estimate = math.ceil(
        (math.pi / 4) * math.sqrt(n)
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Search Space",
        f"{n:,}",
        help="Number of possible candidate states."
    )

    col2.metric(
        "Classical Worst Case",
        f"{classical:,}",
        help="Maximum checks for a simple linear search."
    )

    col3.metric(
        "Grover Query Estimate",
        f"{grover_estimate:,}",
        help="Approximate query count for an idealized search."
    )

    st.divider()

    st.subheader("Search Complexity Comparison")

    fig, ax = plt.subplots(figsize=(9, 4))

    bars = ax.bar(
        ["Classical worst case", "Grover query estimate"],
        [classical, grover_estimate],
        width=0.5
    )

    ax.set_ylabel("Illustrative query count")
    ax.set_title("Theoretical Search Comparison")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.bar_label(bars, padding=4)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "Grover's algorithm offers a quadratic query "
        "speedup for unstructured search under idealized "
        "conditions. Query counts are not execution times."
    )

    st.subheader("Why It Matters")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            '<div class="info-card">'
            '<h4>⚛ Quantum Search</h4>'
            '<p>Uses superposition, an oracle and amplitude '
            'amplification to increase the chance of finding '
            'a target state.</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="info-card">'
            '<h4>🔐 Cybersecurity</h4>'
            '<p>Large-scale quantum computers could affect '
            'some existing cryptographic systems, making '
            'quantum-resistant cryptography important.</p>'
            '</div>',
            unsafe_allow_html=True
        )

# ---------- QUANTUM CIRCUIT ----------
elif page == "⚛  Quantum Circuit":

    st.title("Quantum Circuit Explorer")
    st.write(
        "Run a two-qubit Grover search for the target state |11>."
    )

    st.markdown(
        '<div class="section-label">CIRCUIT CONFIGURATION</div>',
        unsafe_allow_html=True
    )

    shots = st.select_slider(
        "Number of measurement shots",
        options=[256, 512, 1024, 2048, 4096],
        value=1024
    )

    # Prepare the quantum circuit.
    qc = QuantumCircuit(2)

    # Create equal superposition.
    qc.h([0, 1])

    # Oracle marks the target state |11>.
    qc.cz(0, 1)

    # Grover diffusion operator.
    qc.h([0, 1])
    qc.x([0, 1])
    qc.h(1)
    qc.cx(0, 1)
    qc.h(1)
    qc.x([0, 1])
    qc.h([0, 1])

    # Measure both qubits.
    qc.measure_all()

    st.subheader("Circuit Diagram")
    st.code(str(qc.draw(output="text")))

    if st.button("▶ Run Quantum Simulation", type="primary"):

        with st.spinner("Simulating quantum circuit..."):
            simulator = AerSimulator()
            compiled = transpile(qc, simulator)

            result = simulator.run(
                compiled,
                shots=shots
            ).result()

            counts = result.get_counts()

        st.success("Simulation completed.")

        st.subheader("Measurement Results")

        col1, col2 = st.columns(2)

        target_count = counts.get("11", 0)
        probability = target_count / shots * 100

        col1.metric(
            "Target State: 11",
            f"{target_count} / {shots}"
        )

        col2.metric(
            "Target Measurement Rate",
            f"{probability:.1f}%"
        )

        st.bar_chart(counts)

        st.caption(
            "Counts vary with measurement sampling. "
            "This small circuit is an educational demonstration."
        )

    st.divider()

    st.subheader("How the Circuit Works")

    with st.expander("1. Hadamard gates"):
        st.write(
            "Hadamard gates create an equal superposition "
            "of the four computational basis states."
        )

    with st.expander("2. Oracle"):
        st.write(
            "The controlled-Z gate changes the phase of "
            "the target state |11>."
        )

    with st.expander("3. Diffusion operator"):
        st.write(
            "The diffusion operation amplifies the target "
            "state's probability through amplitude amplification."
        )

    with st.expander("4. Measurement"):
        st.write(
            "Measurement converts the quantum state into "
            "classical bit outcomes. For this four-state example, "
            "the target is expected with high probability."
        )

# ---------- ABOUT ----------
elif page == "◈  About":

    st.title("About Q-Secure")

    st.write(
        "Q-Secure is an educational project that explores "
        "quantum search and its potential implications for "
        "password security and cryptography."
    )

    st.subheader("Project Objectives")

    st.markdown("""
    - Understand Grover's quantum search algorithm.
    - Compare classical and quantum query complexity.
    - Simulate a quantum circuit using Qiskit.
    - Explore why post-quantum cryptography matters.
    """)

    st.subheader("Technology Stack")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown("**Python**")
    c2.markdown("**Streamlit**")
    c3.markdown("**Qiskit**")
    c4.markdown("**Matplotlib**")

    st.subheader("Limitations")

    st.warning(
        "This project is a small-scale educational simulation. "
        "It does not crack real passwords or demonstrate an attack "
        "against real encryption. The search comparison is theoretical, "
        "and a simulated quantum circuit does not establish a "
        "real-world speed advantage."
    )

    st.subheader("Future Scope")

    st.markdown("""
    - Add more Grover search examples.
    - Visualize quantum circuit operations.
    - Explore post-quantum cryptographic algorithms.
    - Compare ideal query complexity with practical circuit costs.
    """)

    st.divider()

    st.caption(
        "Q-SECURE | Built as a learning project in quantum computing."
    )

# ---------- FOOTER ----------
st.divider()

st.caption(
    "Q-SECURE  ·  Quantum Security Lab  ·  Educational use only"
)
