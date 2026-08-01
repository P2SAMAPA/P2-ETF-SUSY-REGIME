# P2-SUSY-REGIME

**SUSY-Enhanced Regime Detection — Supersymmetric Quantum Mechanics for Market Regime Shifts**

Part of the **P2Quant Engine Suite** · P2SAMAPA

---

## What This Engine Does

This engine applies **Supersymmetric Quantum Mechanics (SUSY-QM)** to the Fokker-Planck equation of a time-series model with regime switches. The energy gap in the SUSY partner Hamiltonian becomes an early warning indicator for regime shifts, more sensitive than traditional methods based on variance or autocorrelation.

### Theory

**Supersymmetric Quantum Mechanics:**
- Constructs partner Hamiltonians H+ and H- from a superpotential W(x)
- H± = -∂²/∂x² + V±(x), where V± = W² ± W'
- Energy spectra of H+ and H- are related (SUSY partners)

**Fokker-Planck Equation:**
- Describes the evolution of probability density
- Can be mapped to a Schrödinger-like equation
- Regime switches appear as changes in the potential

**Energy Gap as Early Warning:**
- Ground state energy near zero = stable regime
- Energy gap closing = approaching regime shift
- SUSY breaking signal = market transition detection

---

## Key Metrics

| Metric | What it tells you |
|--------|-------------------|
| **z-score** | Cross-sectional ranking of regime stability |
| **Energy Gap** | Gap between ground and first excited state |
| **Regime Type** | IMMINENT / POSSIBLE / STABLE |
| **SUSY Breaking** | Near-zero ground state indicator |

---

## Windows

| Window | Purpose |
|--------|---------|
| 63d | Short-term regime detection |
| 252d | Core signal (primary) |
| 504d | Medium-term regime structure |
| 1008d | Structural regime detection |
| 2016d+ | Secular regime analysis |

---

## Setup

```bash
git clone https://github.com/P2SAMAPA/P2-SUSY-REGIME
cd P2-SUSY-REGIME
pip install -r requirements.txt

export HF_TOKEN=hf_...
python trainer.py

streamlit run streamlit_app.py
