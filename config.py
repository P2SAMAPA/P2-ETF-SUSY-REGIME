"""
config.py  —  Configuration for SUSY-Regime Engine
===================================================

Defines:
  - UNIVERSES: ETF ticker sets
  - SUSY: Supersymmetric quantum mechanics parameters
  - WINDOWS: Time windows for regime detection
  - REGIME: Thresholds and detection parameters
"""

# ── HuggingFace ──────────────────────────────────────────────────────────────

HF_TOKEN = ""
DATA_REPO = "P2SAMAPA/fi-etf-macro-signal-master-data"
RESULTS_REPO = "P2SAMAPA/p2-susy-regime-results"


# ── ETF Universes ────────────────────────────────────────────────────────────

UNIVERSES = {
    "FI_COMMODITIES": [
        "TLT", "VCIT", "LQD", "HYG", "VNQ", "GLD", "SLV",
    ],
    "EQUITY_SECTORS": [
        "SPY", "QQQ", "XLK", "XLF", "XLE", "XLV", "XLI", "VUG", "VTV", "SPYG", "QUAL", "IWR", "VO", "VB", "VIG", "VEA", "VGT", "VDE", "XLC", "IBB",
        "XLY", "XLP", "XLU", "GDX", "XME", "IWF", "XSD", "SOXX", "SMH", "URA",
        "XBI", "IWM", "IWD", "IWO", "XLB", "XLRE",
    ],
    "COMBINED": [
        "TLT", "VCIT", "LQD", "HYG", "VNQ", "GLD", "SLV",
        "SPY", "QQQ", "XLK", "XLF", "XLE", "XLV", "XLI", "VUG", "VTV", "SPYG", "QUAL", "IWR", "VO", "VB", "VIG", "VEA", "VGT", "VDE", "XLC", "IBB",
        "XLY", "XLP", "XLU", "GDX", "XME", "IWF", "XSD", "SOXX", "SMH", "URA",
        "XBI", "IWM", "IWD", "IWO", "XLB", "XLRE",
    ],
}


# ── Windows ──────────────────────────────────────────────────────────────────

WINDOWS = [63, 252, 504, 1008, 2016, 4032, 4536]
WINDOW_LABELS = {
    63: "63d  (~3 months) — Short-term",
    252: "252d (~1 year) — Core Signal",
    504: "504d (~2 years) — Medium-term",
    1008: "1008d (~4 years) — Structural",
    2016: "2016d (~8 years) — Secular",
    4032: "4032d (~16 years) — Long-term",
    4536: "4536d (~18 years) — Full History",
}
PRIMARY_WINDOW = 252


# ── SUSY Parameters ─────────────────────────────────────────────────────────

SUSY = {
    "n_eigenvalues": 10,        # Number of eigenvalues to compute
    "potential_type": "morse",   # morse, harmonic, double_well
    "superpotential": "tanh",    # tanh, polynomial, custom
    "energy_gap_threshold": 0.1, # Threshold for regime shift detection
    "ground_state_energy": 0.0,  # Near-zero ground state
}


# ── Regime Detection Parameters ─────────────────────────────────────────────

REGIME = {
    "shift_threshold": 0.5,      # Energy gap threshold for regime shift
    "min_regime_length": 10,     # Minimum days in a regime
    "n_regimes": 3,              # Number of regimes to detect
    "smoothing_window": 5,       # Smoothing for energy gap signal
}


# ── Macro Signals ────────────────────────────────────────────────────────────

MACRO_SIGNALS = [
    ("VIX",       "VIX",           0.30, -1.0),
    ("T10Y2Y",    "10Y–2Y Spread", 0.25, +1.0),
    ("DXY",       "DXY",           0.20, -1.0),
    ("IG_SPREAD", "IG Spread",     0.15, -1.0),
    ("HY_SPREAD", "HY Spread",     0.10, -1.0),
]

MACRO_COLS_CORE = ["VIX", "T10Y2Y", "DXY"]
MACRO_COLS_EXTENDED = ["IG_SPREAD", "HY_SPREAD"]
