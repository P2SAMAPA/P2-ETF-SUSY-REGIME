"""
susy_regime.py  —  SUSY-Enhanced Regime Detection Engine
=========================================================

Implements:
- Supersymmetric Quantum Mechanics (SUSY-QM)
- Fokker-Planck equation with regime switches
- Partner potential and energy gap computation
- Early warning indicator for regime shifts
"""

import numpy as np
import pandas as pd
from scipy.linalg import eig, eigh
from scipy.special import hermite, factorial
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")


class SUSYRegimeEngine:
    """
    SUSY-Enhanced Regime Detection Engine.
    
    Applies Supersymmetric Quantum Mechanics to detect market regime shifts.
    The energy gap in the SUSY partner Hamiltonian becomes an early warning
    indicator for regime transitions.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.n_eigenvalues = config.get("n_eigenvalues", 10)
        self.potential_type = config.get("potential_type", "morse")
        self.superpotential = config.get("superpotential", "tanh")
        self.energy_gap_threshold = config.get("energy_gap_threshold", 0.1)
        self.ground_state_energy = config.get("ground_state_energy", 0.0)
        
    def compute_superpotential(self, x: np.ndarray, params: Dict) -> np.ndarray:
        """
        Compute the superpotential W(x) for the SUSY system.
        
        The superpotential determines the partner potentials:
        V_±(x) = W(x)^2 ± W'(x)
        """
        if self.superpotential == "tanh":
            # Tanh superpotential: W(x) = a * tanh(b * x)
            a = params.get("a", 1.0)
            b = params.get("b", 0.5)
            return a * np.tanh(b * x)
        
        elif self.superpotential == "polynomial":
            # Polynomial superpotential: W(x) = a*x^3 + b*x
            a = params.get("a", 0.5)
            b = params.get("b", 1.0)
            return a * x**3 + b * x
        
        elif self.superpotential == "morse":
            # Morse superpotential: W(x) = a * (1 - exp(-b*x))
            a = params.get("a", 2.0)
            b = params.get("b", 0.5)
            return a * (1 - np.exp(-b * x))
        
        else:
            # Default: simple linear
            return params.get("a", 1.0) * x
    
    def compute_potential(self, x: np.ndarray, params: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the partner potentials V_+(x) and V_-(x).
        
        V_±(x) = W(x)^2 ± W'(x)
        """
        W = self.compute_superpotential(x, params)
        
        # Compute derivative of superpotential
        dx = x[1] - x[0] if len(x) > 1 else 0.01
        W_prime = np.gradient(W, dx)
        
        V_plus = W**2 + W_prime
        V_minus = W**2 - W_prime
        
        return V_plus, V_minus
    
    def compute_fokker_planck_hamiltonian(self, x: np.ndarray, params: Dict) -> np.ndarray:
        """
        Construct the Fokker-Planck Hamiltonian H_FP.
        
        H_FP = -∂²/∂x² + V_+(x)
        """
        V_plus, V_minus = self.compute_potential(x, params)
        
        n = len(x)
        dx = x[1] - x[0] if len(x) > 1 else 0.01
        
        # Kinetic term: -∂²/∂x² (discretized)
        kinetic = np.zeros((n, n))
        for i in range(1, n-1):
            kinetic[i, i-1] = -1 / dx**2
            kinetic[i, i] = 2 / dx**2
            kinetic[i, i+1] = -1 / dx**2
        
        # Boundary conditions
        kinetic[0, 0] = 1 / dx**2
        kinetic[0, 1] = -1 / dx**2
        kinetic[-1, -1] = 1 / dx**2
        kinetic[-1, -2] = -1 / dx**2
        
        # Potential term
        potential = np.diag(V_plus)
        
        # Hamiltonian
        H_FP = -kinetic + potential
        
        return H_FP
    
    def compute_susy_partner_hamiltonian(self, x: np.ndarray, params: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the SUSY partner Hamiltonians H_+ and H_-.
        
        H_+ = -∂²/∂x² + V_+(x)
        H_- = -∂²/∂x² + V_-(x)
        """
        V_plus, V_minus = self.compute_potential(x, params)
        
        n = len(x)
        dx = x[1] - x[0] if len(x) > 1 else 0.01
        
        # Kinetic term
        kinetic = np.zeros((n, n))
        for i in range(1, n-1):
            kinetic[i, i-1] = -1 / dx**2
            kinetic[i, i] = 2 / dx**2
            kinetic[i, i+1] = -1 / dx**2
        
        kinetic[0, 0] = 1 / dx**2
        kinetic[0, 1] = -1 / dx**2
        kinetic[-1, -1] = 1 / dx**2
        kinetic[-1, -2] = -1 / dx**2
        
        H_plus = -kinetic + np.diag(V_plus)
        H_minus = -kinetic + np.diag(V_minus)
        
        return H_plus, H_minus
    
    def compute_energy_spectrum(self, H: np.ndarray) -> np.ndarray:
        """Compute the energy eigenvalues of a Hamiltonian."""
        try:
            eigenvalues = eigh(H, eigvals_only=True)
            return eigenvalues[:self.n_eigenvalues]
        except:
            # Fallback: use eig
            eigenvalues = eig(H)[0]
            eigenvalues = np.sort(np.real(eigenvalues))
            return eigenvalues[:self.n_eigenvalues]
    
    def compute_energy_gap(self, eigenvalues: np.ndarray) -> float:
        """
        Compute the energy gap between ground state and first excited state.
        
        The energy gap is the early warning indicator for regime shifts.
        A decreasing gap indicates an approaching regime shift.
        """
        if len(eigenvalues) < 2:
            return 0.0
        
        gap = eigenvalues[1] - eigenvalues[0]
        return max(0.0, gap)
    
    def compute_regime_signal(self, returns: np.ndarray, window: int = 252) -> Dict:
        """
        Compute the full SUSY regime detection signal.
        """
        if len(returns) < window:
            return {
                "energy_gap": 0.0,
                "ground_state_energy": 0.0,
                "first_excited_energy": 0.0,
                "eigenvalues": [],
                "regime_shift_signal": 0.0,
                "regime_type": "unknown",
                "error": "Insufficient data"
            }
        
        # Use rolling window for regime detection
        n_steps = min(len(returns), window)
        recent_returns = returns[-n_steps:]
        
        # Normalize returns for numerical stability
        returns_norm = (recent_returns - np.mean(recent_returns)) / (np.std(recent_returns) + 1e-6)
        
        # Create spatial grid
        n_grid = min(100, len(returns_norm))
        x = np.linspace(-3, 3, n_grid)
        
        # Fit parameters to data
        params = self._fit_parameters(recent_returns)
        
        # Compute Hamiltonians
        H_plus, H_minus = self.compute_susy_partner_hamiltonian(x, params)
        
        # Compute energy spectra
        eigenvalues_plus = self.compute_energy_spectrum(H_plus)
        eigenvalues_minus = self.compute_energy_spectrum(H_minus)
        
        # Compute energy gaps
        gap_plus = self.compute_energy_gap(eigenvalues_plus)
        gap_minus = self.compute_energy_gap(eigenvalues_minus)
        
        # Use average gap as signal
        energy_gap = (gap_plus + gap_minus) / 2
        
        # Compute SUSY-breaking signal (near-zero ground state)
        ground_state = eigenvalues_plus[0] if len(eigenvalues_plus) > 0 else 0
        susy_breaking = abs(ground_state - self.ground_state_energy)
        
        # Regime shift signal: combination of energy gap and SUSY breaking
        # Lower energy gap + higher SUSY breaking = impending regime shift
        regime_shift_signal = energy_gap / (susy_breaking + 0.01)
        
        # Determine regime type
        if regime_shift_signal < 0.5:
            regime_type = "REGIME_SHIFT_IMMINENT"
        elif regime_shift_signal < 1.0:
            regime_type = "REGIME_SHIFT_POSSIBLE"
        elif regime_shift_signal < 2.0:
            regime_type = "STABLE_REGIME"
        else:
            regime_type = "STRONG_STABLE_REGIME"
        
        return {
            "energy_gap": energy_gap,
            "ground_state_energy": eigenvalues_plus[0] if len(eigenvalues_plus) > 0 else 0,
            "first_excited_energy": eigenvalues_plus[1] if len(eigenvalues_plus) > 1 else 0,
            "eigenvalues": eigenvalues_plus[:5].tolist(),
            "gap_plus": gap_plus,
            "gap_minus": gap_minus,
            "susy_breaking": susy_breaking,
            "regime_shift_signal": regime_shift_signal,
            "regime_type": regime_type,
            "window": window,
            "error": None
        }
    
    def _fit_parameters(self, returns: np.ndarray) -> Dict:
        """
        Fit the superpotential parameters to the data.
        """
        # Use moments of returns to estimate parameters
        mean_r = np.mean(returns)
        std_r = np.std(returns) + 1e-6
        skew_r = pd.Series(returns).skew() if len(returns) > 2 else 0
        kurt_r = pd.Series(returns).kurtosis() if len(returns) > 3 else 0
        
        # Map moments to superpotential parameters
        params = {
            "a": 0.5 + 0.5 * abs(skew_r),
            "b": 0.5 + 0.5 * std_r * 10,
        }
        
        # Adjust for regime characteristics
        if abs(kurt_r) > 3:
            params["a"] *= 1.5  # Heavy tails = stronger superpotential
        
        return params


def compute_susy_regime(
    prices: pd.Series,
    config: Dict,
    window: int = 252
) -> Dict:
    """
    Compute SUSY regime detection for a single ticker.
    """
    returns = np.log(prices / prices.shift(1)).dropna().values
    
    if len(returns) < window:
        return {
            "energy_gap": 0.0,
            "regime_shift_signal": 0.0,
            "regime_type": "insufficient_data",
            "z_score": 0,
            "error": "Insufficient data"
        }
    
    engine = SUSYRegimeEngine(config.get("susy", {}))
    result = engine.compute_regime_signal(returns, window)
    
    return result


def compute_universe_regime(
    prices_df: pd.DataFrame,
    config: Dict,
    window: int = 252
) -> Dict:
    """
    Compute SUSY regime detection for all ETFs in a universe.
    """
    results = {}
    
    for ticker in prices_df.columns:
        prices = prices_df[ticker]
        result = compute_susy_regime(prices, config, window)
        
        results[ticker] = {
            "energy_gap": result.get("energy_gap", 0),
            "regime_shift_signal": result.get("regime_shift_signal", 0),
            "regime_type": result.get("regime_type", "unknown"),
            "ground_state": result.get("ground_state_energy", 0),
            "susy_breaking": result.get("susy_breaking", 0),
            "z_score": 0  # Will be normalized
        }
    
    # Normalize z-scores
    signals = np.array([r["regime_shift_signal"] for r in results.values()])
    if len(signals) > 1 and np.std(signals) > 1e-6:
        mean_s = np.mean(signals)
        std_s = np.std(signals)
        for ticker, r in results.items():
            r["z_score"] = (r["regime_shift_signal"] - mean_s) / std_s
    else:
        # Use energy gap as fallback
        gaps = np.array([r["energy_gap"] for r in results.values()])
        if len(gaps) > 1 and np.std(gaps) > 1e-6:
            mean_g = np.mean(gaps)
            std_g = np.std(gaps)
            for ticker, r in results.items():
                r["z_score"] = (r["energy_gap"] - mean_g) / std_g
        else:
            for r in results.values():
                r["z_score"] = 0
    
    return results
