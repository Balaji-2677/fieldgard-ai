"""
Machine Learning and Agronomy Package for Crop Yield Prediction
"""

import sys
import types

# Windows Smart App Control patch: Avoid loading blocked unsigned _cd_fast pyd
if "sklearn.linear_model._cd_fast" not in sys.modules:
    _dummy_cd_fast = types.ModuleType("sklearn.linear_model._cd_fast")
    _dummy_cd_fast.enet_coordinate_descent = lambda *a, **k: None
    _dummy_cd_fast.enet_coordinate_descent_gram = lambda *a, **k: (0, 0, 0, 0)
    _dummy_cd_fast.enet_coordinate_descent_multi_task = lambda *a, **k: None
    _dummy_cd_fast.sparse_enet_coordinate_descent = lambda *a, **k: None
    sys.modules["sklearn.linear_model._cd_fast"] = _dummy_cd_fast
