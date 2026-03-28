#!/usr/bin/env python3
"""
Parse OpenFOAM log file and plot residuals vs time.
Usage: python plot_residuals.py <logfile> [--save]
"""

import re
import sys
import argparse
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_log(logfile):
    time = []
    residuals = defaultdict(list)
    time_points = []

    time_pattern    = re.compile(r'^Time = ([\d.eE+\-]+)')
    residual_pattern = re.compile(
        r'smoothSolver|PCG|PBiCGStab|GAMG|DILUPBiCGStab'
        r'.*?Solving for (\w+),.*?Initial residual = ([\d.eE+\-]+)',
        re.IGNORECASE
    )
    # Alternate pattern for solvers that print differently
    alt_pattern = re.compile(
        r'Solving for (\w+),\s+Initial residual = ([\d.eE+\-]+)'
    )

    current_time = None

    with open(logfile, 'r') as f:
        for line in f:
            t_match = time_pattern.match(line)
            if t_match:
                current_time = float(t_match.group(1))
                continue

            if current_time is None:
                continue

            r_match = alt_pattern.search(line)
            if r_match:
                field = r_match.group(1)
                resid = float(r_match.group(2))
                residuals[field].append((current_time, resid))

    # Deduplicate: if multiple iterations per time step, keep last
    clean = {}
    for field, pairs in residuals.items():
        seen = {}
        for t, r in pairs:
            seen[t] = r  # last value at each time step
        times = sorted(seen.keys())
        clean[field] = (times, [seen[t] for t in times])

    return clean


def plot_residuals(data, logfile, save=False):
    if not data:
        print("No residual data found. Check log format.")
        sys.exit(1)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    colors = plt.cm.tab10.colors

    for i, (field, (times, resids)) in enumerate(data.items()):
        ax.semilogy(times, resids, label=field,
                    color=colors[i % len(colors)], linewidth=1.4)

    ax.set_xlabel('Time [s]', color='#c9d1d9', fontsize=12)
    ax.set_ylabel('Initial Residual', color='#c9d1d9', fontsize=12)
    ax.set_title(f'OpenFOAM Residuals — {logfile}',
                 color='#e6edf3', fontsize=13, pad=12)

    ax.tick_params(colors='#8b949e')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

    ax.grid(True, which='both', color='#21262d',
            linestyle='--', linewidth=0.6, alpha=0.8)
    ax.legend(facecolor='#161b22', edgecolor='#30363d',
              labelcolor='#c9d1d9', fontsize=10)

    plt.tight_layout()

    if save:
        out = 'residuals.png'
        plt.savefig(out, dpi=150, bbox_inches='tight')
        print(f"Saved: {out}")
    else:
        plt.show()


if __name__ == '__main__':
    data = parse_log("log.pimpleDyMIbFoam")
    plot_residuals(data, "log.pimpleDyMIbFoam", save=True)