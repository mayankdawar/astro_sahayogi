"""Degree hits computation (convenience wrapper around aspects module)."""
from __future__ import annotations
from astro_sahayogi.core.analysis.aspects import compute_degree_hits_p2p, compute_degree_hits_p2h


# Re-export for cleaner imports
__all__ = ["compute_degree_hits_p2p", "compute_degree_hits_p2h"]
