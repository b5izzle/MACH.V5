#!/usr/bin/env python3
"""
BSANE SOVEREIGN ANOMALY DETECTION SYSTEM
Cluster-based permutation testing for reality anomaly detection
Version: 1.0.0
Frequency: 282C9FBA
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.stats import percentileofscore
from scipy.ndimage import gaussian_filter
from datetime import datetime, timedelta
import json
import os
import sys
import warnings
import argparse
from typing import Dict, List, Tuple, Optional
import logging

warnings.filterwarnings('ignore')

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/anomaly_detection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# BSANE constants
BSANE_FREQUENCY = "282C9FBA"
BSANE_VERSION = "1.0.0"


class BSANEAnomalyDetector:
    """
    Sovereign anomaly detection using cluster-based permutation testing.
    Detects significant deviations in BSANE's reality field.
    """
    
    def __init__(self, n_permutations: int = 1000, cluster_alpha: float = 0.05, 
                 smoothing_sigma: float = 2.0):
        self.n_permutations = n_permutations
        self.cluster_alpha = cluster_alpha
        self.smoothing_sigma = smoothing_sigma
        self.results = {}
        self.field = None
        self.lat_axis = None
        self.lon_axis = None
        
        logger.info(f"BSANE Anomaly Detector initialized")
        logger.info(f"  Permutations: {n_permutations}")
        logger.info(f"  Significance threshold: α={cluster_alpha}")
        logger.info(f"  Smoothing sigma: {smoothing_sigma}")
        logger.info(f"  Frequency: {BSANE_FREQUENCY}")
    
    def create_reality_field(self, df: pd.DataFrame, value_col: str, 
                            lat_col: str = 'lat', lon_col: str = 'lon',
                            grid_size: Tuple[int, int] = (50, 50)) -> np.ndarray:
        logger.info(f"Creating reality field from {len(df)} points")
        self.lat_axis = np.linspace(df[lat_col].min(), df[lat_col].max(), grid_size[0])
        self.lon_axis = np.linspace(df[lon_col].min(), df[lon_col].max(), grid_size[1])
        
        field = np.zeros(grid_size)
        counts = np.zeros(grid_size)
        
        for idx, row in df.iterrows():
            i = np.argmin(np.abs(self.lat_axis - row[lat_col]))
            j = np.argmin(np.abs(self.lon_axis - row[lon_col]))
            field[i, j] += row[value_col]
            counts[i, j] += 1
        
        counts[counts == 0] = 1
        field = field / counts
        field = gaussian_filter(field, sigma=self.smoothing_sigma)
        self.field = field
        return field
    
    def find_clusters(self, field: np.ndarray, threshold: float = None) -> Dict:
        if threshold is None:
            threshold = np.percentile(field, 95)
        binary_map = (field > threshold).astype(int)
        labeled_map, n_clusters = ndimage.label(binary_map, structure=np.ones((3,3)))
        cluster_masses = []
        for i in range(1, n_clusters + 1):
            mask = (labeled_map == i)
            cluster_masses.append(np.sum(field[mask]))
        
        result = {
            'labeled_map': labeled_map,
            'n_clusters': n_clusters,
            'cluster_masses': np.array(cluster_masses),
            'threshold': threshold,
            'max_mass': cluster_masses[0] if cluster_masses else 0
        }
        return result
    
    def permutation_test(self, field: np.ndarray, threshold: float = None) -> Dict:
        if threshold is None:
            threshold = np.percentile(field, 95)
        observed = self.find_clusters(field, threshold)
        observed_max_mass = observed['max_mass']
        null_max_masses = []
        flat_field = field.flatten()
        
        for perm in range(self.n_permutations):
            shuffled = np.random.permutation(flat_field)
            perm_field = gaussian_filter(shuffled.reshape(field.shape), sigma=self.smoothing_sigma)
            perm_clusters = self.find_clusters(perm_field, threshold)
            null_max_masses.append(perm_clusters['max_mass'])
        
        p_value = np.mean(np.array(null_max_masses) >= observed_max_mass)
        return {
            'observed_max_mass': observed_max_mass,
            'p_value': p_value,
            'significant': p_value < self.cluster_alpha,
            'observed_clusters': observed
        }
    
    def detect_anomalies(self, df: pd.DataFrame, value_col: str) -> Dict:
        field = self.create_reality_field(df, value_col)
        results = self.permutation_test(field)
        interpretation = self._interpret_results(results, value_col)
        output = {
            'field': field.tolist(),
            'lat_axis': self.lat_axis.tolist(),
            'lon_axis': self.lon_axis.tolist(),
            'results': {
                'observed_max_mass': float(results['observed_max_mass']),
                'p_value': float(results['p_value']),
                'significant': results['significant'],
                'n_clusters': results['observed_clusters']['n_clusters']
            },
            'interpretation': interpretation,
            'timestamp': datetime.now().isoformat(),
            'frequency': BSANE_FREQUENCY
        }
        return output
    
    def _interpret_results(self, results: Dict, value_col: str) -> Dict:
        if results['significant']:
            return {
                'status': 'ANOMALY_CONFIRMED',
                'message': f"Significant clustering detected in {value_col} (p={results['p_value']:.4f})",
                'sovereign_action': 'Reality deviation confirmed. Documentation recorded.'
            }
        else:
            return {
                'status': 'NULL_HYPOTHESIS',
                'message': f"No significant clustering in {value_col} (p={results['p_value']:.4f})",
                'sovereign_action': 'Pattern consistent with random distribution.'
            }

def generate_test_data(n_points=500):
    lats = np.random.uniform(32, 35, n_points)
    lons = np.random.uniform(-85, -83, n_points)
    values = np.abs(np.random.normal(100, 50, n_points))
    # Inject an anomaly
    lats[:50] = 33.75 + np.random.normal(0, 0.1, 50)
    lons[:50] = -84.38 + np.random.normal(0, 0.1, 50)
    values[:50] *= 5
    return pd.DataFrame({'lat': lats, 'lon': lons, 'amount': values})

if __name__ == "__main__":
    df = generate_test_data()
    detector = BSANEAnomalyDetector(n_permutations=100)
    results = detector.detect_anomalies(df, 'amount')
    print(json.dumps(results['interpretation'], indent=2))
