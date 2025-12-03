#!/usr/bin/env python3
"""
Complex Permeability Calculator from VNA Impedance Measurements

This script calculates complex permeability (μ = μ' - jμ'') from impedance data
measured with a Vector Network Analyzer (VNA).

The calculation is based on the relationship between impedance and permeability
for a toroidal core or similar magnetic sample configuration.

Author: Notion Scripts Collection
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt


def calculate_permeability(impedance, frequency, sample_dimensions):
    """
    Calculate complex permeability from impedance measurements.
    
    Parameters:
    -----------
    impedance : complex array
        Complex impedance Z = R + jX (Ohms)
    frequency : array
        Frequency points (Hz)
    sample_dimensions : dict
        Dictionary containing:
        - 'outer_diameter': Outer diameter of toroid (m)
        - 'inner_diameter': Inner diameter of toroid (m)
        - 'height': Height of toroid (m)
        - 'turns': Number of wire turns
    
    Returns:
    --------
    permeability : complex array
        Complex permeability μ = μ' - jμ''
    mu_real : array
        Real part of permeability (μ')
    mu_imag : array
        Imaginary part of permeability (μ'')
    """
    # Extract dimensions
    outer_d = sample_dimensions['outer_diameter']
    inner_d = sample_dimensions['inner_diameter']
    height = sample_dimensions['height']
    turns = sample_dimensions['turns']
    
    # Calculate geometric parameters
    mean_diameter = (outer_d + inner_d) / 2
    cross_section_area = height * (outer_d - inner_d) / 2
    mean_length = np.pi * mean_diameter
    
    # Calculate inductance from impedance
    # Z = R + jωL for inductive component
    omega = 2 * np.pi * frequency
    
    # Avoid division by zero for omega
    with np.errstate(divide='ignore', invalid='ignore'):
        inductance = np.where(omega != 0, np.imag(impedance) / omega, 0)
    
    # Calculate permeability
    # L = μ₀ μᵣ N² A / l
    # Therefore: μᵣ = L * l / (μ₀ N² A)
    mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)
    
    permeability = (inductance * mean_length) / (mu_0 * turns**2 * cross_section_area)
    
    # Also account for resistance (loss component)
    # The loss can be related to imaginary permeability
    resistance = np.real(impedance)
    
    # Avoid division by zero for loss factor calculation
    with np.errstate(divide='ignore', invalid='ignore'):
        denominator = omega * inductance
        loss_factor = np.where(denominator != 0, resistance / denominator, 0)
    
    # Complex permeability
    mu_real = np.real(permeability)
    mu_imag = mu_real * loss_factor
    
    complex_permeability = mu_real - 1j * mu_imag
    
    return complex_permeability, mu_real, mu_imag


def plot_permeability(frequency, mu_real, mu_imag):
    """
    Plot the complex permeability vs frequency.
    
    Parameters:
    -----------
    frequency : array
        Frequency points (Hz)
    mu_real : array
        Real part of permeability (μ')
    mu_imag : array
        Imaginary part of permeability (μ'')
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot real part
    ax1.semilogx(frequency / 1e6, mu_real, 'b-', linewidth=2)
    ax1.set_xlabel('Frequency (MHz)')
    ax1.set_ylabel("Real Permeability (μ')")
    ax1.set_title('Complex Permeability vs Frequency')
    ax1.grid(True, which='both', alpha=0.3)
    
    # Plot imaginary part
    ax2.semilogx(frequency / 1e6, mu_imag, 'r-', linewidth=2)
    ax2.set_xlabel('Frequency (MHz)')
    ax2.set_ylabel("Imaginary Permeability (μ'')")
    ax2.grid(True, which='both', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('permeability_plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'permeability_plot.png'")
    plt.show()


def example_usage():
    """
    Example usage with simulated VNA impedance data.
    """
    print("=" * 60)
    print("Complex Permeability Calculator - Example")
    print("=" * 60)
    
    # Simulated VNA measurement parameters
    frequency = np.logspace(4, 8, 100)  # 10 kHz to 100 MHz
    
    # Sample dimensions for a toroidal core
    sample_dimensions = {
        'outer_diameter': 20e-3,   # 20 mm
        'inner_diameter': 10e-3,   # 10 mm
        'height': 5e-3,            # 5 mm
        'turns': 10                # 10 turns of wire
    }
    
    # Simulated impedance data (typical ferrite behavior)
    # Z = R + jωL with frequency-dependent parameters
    base_inductance = 1e-6  # 1 μH base inductance
    mu_initial = 1000  # Initial permeability
    
    # Simple model with frequency-dependent permeability
    omega = 2 * np.pi * frequency
    mu_freq = mu_initial / (1 + (frequency / 1e7)**2)  # Decreases with frequency
    
    # Calculate impedance from model
    L = base_inductance * mu_freq / mu_initial
    R = 0.1 * omega * L  # Loss increases with frequency
    impedance = R + 1j * omega * L
    
    print("\nSample Configuration:")
    print(f"  Outer Diameter: {sample_dimensions['outer_diameter']*1000:.1f} mm")
    print(f"  Inner Diameter: {sample_dimensions['inner_diameter']*1000:.1f} mm")
    print(f"  Height: {sample_dimensions['height']*1000:.1f} mm")
    print(f"  Turns: {sample_dimensions['turns']}")
    
    print("\nFrequency Range:")
    print(f"  Min: {frequency.min()/1e3:.1f} kHz")
    print(f"  Max: {frequency.max()/1e6:.1f} MHz")
    
    # Calculate permeability
    complex_mu, mu_real, mu_imag = calculate_permeability(
        impedance, frequency, sample_dimensions
    )
    
    # Display results at selected frequencies
    print("\nCalculated Permeability at Selected Frequencies:")
    print("-" * 60)
    print(f"{'Frequency':>12} {'μ (real)':>12} {'μ (imag)':>12} {'|μ|':>12}")
    print("-" * 60)
    
    indices = [0, len(frequency)//4, len(frequency)//2, 3*len(frequency)//4, -1]
    for idx in indices:
        freq_mhz = frequency[idx] / 1e6
        mu_r = mu_real[idx]
        mu_i = mu_imag[idx]
        mu_mag = np.abs(complex_mu[idx])
        print(f"{freq_mhz:10.3f} MHz {mu_r:12.2f} {mu_i:12.2f} {mu_mag:12.2f}")
    
    # Plot results
    print("\nGenerating plot...")
    plot_permeability(frequency, mu_real, mu_imag)
    
    print("\n" + "=" * 60)
    print("Calculation complete!")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
