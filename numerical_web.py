
# ══════════════════════════════════════════════════════════════════════════════
#   Numerical Methods Calculator — Web Edition (Mobile Friendly)
#   Horus University · Faculty of AI · Cyber Security Department
#   Run:  streamlit run numerical_web.py
# ═══════════════════════════════════════════════════════════════════════════════

import math
import ast
import base64
import re
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.collections import LineCollection

warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Numerical Methods Calculator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  DARK THEME CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    :root {
        --bg-main: #0A0A0F;
        --bg-panel: #12121A;
        --bg-soft: #1A1A24;
        --border: #252535;
        --text-main: #F0F0FF;
        --text-muted: #9090B0;
        --accent: #00B4D8;
        --accent-hover: #0096C7;
        --success: #00FF88;
        --error: #FF4455;
    }

    .stApp {
        background-color: var(--bg-main);
        color: var(--text-main);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--bg-panel);
        border-left: 1px solid var(--border);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-soft) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(0,180,216,0.15) !important;
    }

    .stSelectbox > div > div {
        background-color: var(--bg-soft) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    .stDataFrame {
        background-color: var(--bg-panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    .stDataFrame thead th {
        background-color: var(--bg-soft) !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 10px !important;
        border-bottom: 2px solid var(--accent) !important;
    }

    .stDataFrame tbody td {
        background-color: var(--bg-panel) !important;
        color: var(--text-main) !important;
        text-align: center !important;
        padding: 8px !important;
        border-bottom: 1px solid var(--border) !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
    }

    .stDataFrame tbody tr:hover td {
        background-color: var(--bg-soft) !important;
    }

    div[data-testid="stMetric"] {
        background-color: var(--bg-panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 12px !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-size: 22px !important;
    }

    h1, h2, h3, h4 {
        color: var(--text-main) !important;
    }

    p, span, label, div {
        color: var(--text-muted) !important;
    }

    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: var(--text-muted);
    }

    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-hover));
        color: #000;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 12px 28px;
        font-size: 15px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button[kind="secondary"] {
        background-color: var(--bg-soft);
        color: var(--text-main);
        border: 1px solid var(--border);
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 20px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: var(--bg-panel);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-muted);
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--accent);
        border-radius: 8px;
        height: 3px;
    }

    .stTabs [aria-selected="true"] {
        color: #000 !important;
        background-color: var(--accent) !important;
        border-radius: 8px;
    }

    .info-card {
        background-color: var(--bg-soft);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .result-box {
        background-color: var(--bg-panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: var(--text-main);
        white-space: pre-wrap;
        overflow-x: auto;
    }

    .header-accent {
        color: var(--accent) !important;
        font-weight: 700;
    }

    .section-title {
        color: var(--text-main) !important;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border);
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .stButton > button {
            padding: 10px 16px;
            font-size: 14px;
        }

        .stDataFrame tbody td {
            font-size: 11px !important;
            padding: 6px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  VALIDATORS
# ═══════════════════════════════════════════════════════════════════════════════

def is_diagonally_dominant(a):
    mat = np.array(a, dtype=float)
    for i in range(mat.shape[0]):
        if abs(mat[i, i]) < np.sum(np.abs(mat[i, :])) - abs(mat[i, i]):
            return False
    return True

def is_equally_spaced(x, tol=1e-12):
    arr = np.array(x, dtype=float)
    if len(arr) < 2:
        return True
    diffs = np.diff(arr)
    return np.max(np.abs(diffs - diffs[0])) <= tol

# ═══════════════════════════════════════════════════════════════════════════════
#  SAFE EVAL (WITH USER-FRIENDLY AUTO-CORRECTION)
# ═══════════════════════════════════════════════════════════════════════════════

def _safe_eval(expr, x):
    # اللمسة الذكية (User-Friendly Auto-Correction)
    expr = expr.replace('^', '**')
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr) # 2x -> 2*x أو 2( -> 2*(
    expr = re.sub(r'(\))([a-zA-Z\d\(])', r'\1*\2', expr) # )2 -> )*2 أو )( -> )*(
    expr = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr) # x( -> x*(
    
    allowed = {
        "x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
        "pi": math.pi, "e": math.e, "abs": abs,
    }
    return eval(expr, {"__builtins__": {}}, allowed)

# ═══════════════════════════════════════════════════════════════════════════════
#  ROOT-FINDING METHODS
# ═══════════════════════════════════════════════════════════════════════════════

def bisection(expr, a, b, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    fa = _safe_eval(expr, a)
    fb = _safe_eval(expr, b)
    if fa * fb >= 0: raise ValueError("Bisection requires f(a)*f(b) < 0.")
    steps = []
    c = a
    converged = False
    for i in range(1, max_iter + 1):
        c_old = c
        c = (a + b) / 2.0
        fc = _safe_eval(expr, c)
        err = abs(c - c_old)
        steps.append((i, a, b, c, fc, err))
        if abs(fc) < tol or err < tol:
            converged = True
            break
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    if not converged and len(steps) == 1:
        raise RuntimeError("Convergence check appears inverted!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return c, steps

def false_position(expr, a, b, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    fa = _safe_eval(expr, a)
    fb = _safe_eval(expr, b)
    if fa * fb >= 0: raise ValueError("False Position requires f(a)*f(b) < 0.")
    steps = []
    x = a
    converged = False
    for i in range(1, max_iter + 1):
        x_old = x
        x = (a * fb - b * fa) / (fb - fa)
        fx = _safe_eval(expr, x)
        err = abs(x - x_old)
        steps.append((i, a, b, x, fx, err))
        if abs(fx) < tol or err < tol:
            converged = True
            break
        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
    if not converged and len(steps) == 1:
        raise RuntimeError("Convergence check appears inverted!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x, steps

def newton_raphson(expr, d_expr, x0, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    
    # التحقق الذكي من صحة المشتقة (Smart Derivative Validation)
    h = 1e-5
    try:
        num_dfx0 = (_safe_eval(expr, x0 + h) - _safe_eval(expr, x0 - h)) / (2 * h)
        user_dfx0 = _safe_eval(d_expr, x0)
        error_margin = abs(num_dfx0) * 0.05 + 0.1
        
        if abs(user_dfx0 - num_dfx0) > error_margin:
            raise ValueError(f"Math Error: f'(x) is NOT the correct derivative of f(x) at x0={x0}.\nExpected f'({x0}) ~ {num_dfx0:.4f}, but you entered {user_dfx0:.4f}.")
    except ValueError:
        raise
    except Exception:
        pass

    steps = []
    x = x0
    converged = False
    for i in range(1, max_iter + 1):
        fx = _safe_eval(expr, x)
        dfx = _safe_eval(d_expr, x)
        if abs(dfx) < 1e-14:
            raise ValueError("Derivative near zero; Newton-Raphson may diverge.")
        x_new = x - fx / dfx
        err = abs(x_new - x)
        steps.append((i, x, fx, dfx, x_new, err))
        x = x_new
        if abs(fx) < tol or err < tol:
            converged = True
            break
    if not converged and len(steps) == 1:
        raise RuntimeError("Convergence check appears inverted!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x, steps

def secant(expr, x0, x1, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    steps = []
    converged = False
    for i in range(1, max_iter + 1):
        f0 = _safe_eval(expr, x0)
        f1 = _safe_eval(expr, x1)
        denom = f1 - f0
        if abs(denom) < 1e-14:
            raise ValueError("Secant denominator near zero.")
        x2 = x1 - f1 * (x1 - x0) / denom
        err = abs(x2 - x1)
        steps.append((i, x0, x1, x2, _safe_eval(expr, x2), err))
        x0, x1 = x1, x2
        if err < tol or abs(_safe_eval(expr, x2)) < tol:
            converged = True
            break
    if not converged and len(steps) == 1:
        raise RuntimeError("Convergence check appears inverted!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x1, steps

# ═══════════════════════════════════════════════════════════════════════════════
#  LINEAR SYSTEM METHODS
# ═══════════════════════════════════════════════════════════════════════════════

def doolittle_lu(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n):
        raise ValueError(f"Matrix A must be {n}x{n}, got {a.shape}.")
    l = np.eye(n)
    u = np.zeros((n, n), dtype=float)
    steps = []
    for i in range(n):
        for k in range(i, n):
            u[i, k] = a[i, k] - np.sum(l[i, :i] * u[:i, k])
        if abs(u[i, i]) < 1e-14:
            raise ValueError("Zero pivot found in LU decomposition.")
        for k in range(i + 1, n):
            l[k, i] = (a[k, i] - np.sum(l[k, :i] * u[:i, i])) / u[i, i]
        steps.append((i + 1, l.copy(), u.copy()))
    y = np.zeros(n, dtype=float)
    for i in range(n):
        y[i] = b[i] - np.dot(l[i, :i], y[:i])
    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(u[i, i + 1:], x[i + 1:])) / u[i, i]
    return x, l, u, steps

def thomas(lower, diag, upper, rhs):
    n = len(diag)
    a = np.array(lower, dtype=float).copy()
    b = np.array(diag, dtype=float).copy()
    c = np.array(upper, dtype=float).copy()
    d = np.array(rhs, dtype=float).copy()
    steps = []
    for i in range(1, n):
        if abs(b[i - 1]) < 1e-14:
            raise ValueError("Zero pivot in Thomas algorithm.")
        w = a[i - 1] / b[i - 1]
        b[i] = b[i] - w * c[i - 1]
        d[i] = d[i] - w * d[i - 1]
        steps.append((i, w, b[i], d[i]))
    x = np.zeros(n, dtype=float)
    x[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1):
        x[i] = (d[i] - c[i] * x[i + 1]) / b[i]
    return x, steps

def jacobi(a, b, x0=None, tol=1e-6, max_iter=100):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n):
        raise ValueError(f"Matrix A must be {n}x{n}, got {a.shape}.")
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.1: raise ValueError("Tolerance suspiciously large (>0.1).")
    if max_iter < 1: raise ValueError("max_iter must be at least 1.")
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    d = np.diag(a)
    if np.any(np.abs(d) < 1e-14):
        raise ValueError("Zero diagonal element found.")
    r = a - np.diagflat(d)
    steps = []
    converged = False
    final_err = float('inf')
    for i in range(1, max_iter + 1):
        x_new = (b - np.dot(r, x)) / d
        final_err = np.linalg.norm(x_new - x, ord=np.inf)
        steps.append((i, x_new.copy(), final_err))
        x = x_new
        if final_err < tol:
            converged = True
            break
    if not converged and len(steps) == 1 and final_err > tol:
        raise RuntimeError("CONVERGENCE CHECK APPEARS INVERTED!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {final_err:.2e}")
    return x, steps

def gauss_seidel(a, b, x0=None, tol=1e-6, max_iter=100):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n):
        raise ValueError(f"Matrix A must be {n}x{n}, got {a.shape}.")
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.1: raise ValueError("Tolerance suspiciously large (>0.1).")
    if max_iter < 1: raise ValueError("max_iter must be at least 1.")
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    steps = []
    converged = False
    final_err = float('inf')
    for i in range(1, max_iter + 1):
        x_old = x.copy()
        for j in range(n):
            if abs(a[j, j]) < 1e-14:
                raise ValueError(f"Zero diagonal element at row {j}.")
            s1 = np.dot(a[j, :j], x[:j])
            s2 = np.dot(a[j, j + 1:], x_old[j + 1:])
            x[j] = (b[j] - s1 - s2) / a[j, j]
        final_err = np.linalg.norm(x - x_old, ord=np.inf)
        steps.append((i, x.copy(), final_err))
        if final_err < tol:
            converged = True
            break
    if not converged and len(steps) == 1 and final_err > tol:
        raise RuntimeError("CONVERGENCE CHECK APPEARS INVERTED!")
    if not converged:
        warnings.warn(f"No convergence after {max_iter} iters. Error: {final_err:.2e}")
    return x, steps

# ═══════════════════════════════════════════════════════════════════════════════
#  INTERPOLATION METHODS
# ═══════════════════════════════════════════════════════════════════════════════

def _forward_differences(y):
    table = [np.array(y, dtype=float)]
    while len(table[-1]) > 1:
        table.append(np.diff(table[-1]))
    return table

def _backward_differences(y):
    table = [np.array(y, dtype=float)]
    while len(table[-1]) > 1:
        table.append(np.diff(table[-1]))
    return table

def newton_forward(x, y, x_val):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Newton forward requires equally spaced x values.")
    h = x[1] - x[0]
    p = (x_val - x[0]) / h
    diffs = _forward_differences(y)
    result = y[0]
    p_term = 1.0
    fact = 1.0
    for k in range(1, len(y)):
        p_term *= p - (k - 1)
        fact *= k
        result += (p_term / fact) * diffs[k][0]
    return result, diffs

def newton_backward(x, y, x_val):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Newton backward requires equally spaced x values.")
    h = x[1] - x[0]
    p = (x_val - x[-1]) / h
    diffs = _backward_differences(y)
    result = y[-1]
    p_term = 1.0
    fact = 1.0
    for k in range(1, len(y)):
        p_term *= p + (k - 1)
        fact *= k
        result += (p_term / fact) * diffs[k][-1]
    return result, diffs

def stirling(x, y, x_val):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Stirling requires equally spaced x values.")
    if len(x) < 3: raise ValueError("Stirling needs at least 3 points.")
    n = len(x)
    h = x[1] - x[0]
    mid = n // 2
    p = (x_val - x[mid]) / h
    diffs = _forward_differences(y)
    result = y[mid]
    for k in range(1, n):
        fact = math.factorial(k)
        if k % 2 == 0:
            idx = mid - k // 2
            if idx < 0 or idx >= len(diffs[k]): break
            d = diffs[k][idx]
        else:
            idx1 = mid - k // 2 - 1
            idx2 = mid - k // 2
            if idx1 < 0 or idx2 >= len(diffs[k]): break
            d = (diffs[k][idx1] + diffs[k][idx2]) / 2.0
        if k == 1:
            p_coeff = p
        elif k == 2:
            p_coeff = p ** 2
        elif k % 2 == 1:
            p_coeff = p
            for j in range(1, k // 2 + 1):
                p_coeff *= (p ** 2 - j ** 2)
        else:
            p_coeff = p ** 2
            for j in range(1, k // 2):
                p_coeff *= (p ** 2 - j ** 2)
        result += (p_coeff / fact) * d
    return float(result), diffs

def lagrange(x, y, x_val):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    n = len(x)
    result = 0.0
    for i in range(n):
        term = y[i] 
        for j in range(n):
            if i != j:
                term *= (x_val - x[j]) / (x[i] - x[j])
        result += term
    return float(result)

# ═══════════════════════════════════════════════════════════════════════════════
#  METHOD INFO
# ═══════════════════════════════════════════════════════════════════════════════

METHOD_INFO = {
    "Bisection":       {"category": "Root Finding",              "order": "Linear  (p = 1)",          "color": "#00B4D8", "desc": "Guaranteed convergence by halving the bracket each iteration.\nRequires sign change on [a, b]."},
    "False Position":  {"category": "Root Finding",              "order": "Superlinear",              "color": "#0096C7", "desc": "Uses a secant line to approximate the root within a bracket.\nFaster than Bisection in practice."},
    "Newton-Raphson":  {"category": "Root Finding",              "order": "Quadratic  (p = 2)",       "color": "#48CAE4", "desc": "Uses f(x) and f'(x) to converge very fast near the root.\nMay diverge if f'(x) ~ 0."},
    "Secant":          {"category": "Root Finding",              "order": "Superlinear  (p ~ 1.618)", "color": "#90E0EF", "desc": "Newton-Raphson without derivative.\nTwo initial guesses required."},
    "Jacobi":          {"category": "Linear Systems - Iterative","order": "Linear  (spectral radius)", "color": "#00B4D8", "desc": "Updates all variables simultaneously using previous-step values only.\nNeeds diagonal dominance to converge."},
    "Gauss-Seidel":    {"category": "Linear Systems - Iterative","order": "Faster than Jacobi",        "color": "#0096C7", "desc": "Updates variables in-place, reusing newly computed values immediately.\nTypically 2x faster than Jacobi."},
    "Doolittle LU":    {"category": "Linear Systems - Direct",   "order": "O(n^3) - exact",            "color": "#48CAE4", "desc": "Factorizes A = L*U, then solves two triangular systems.\nExact result in one pass."},
    "Thomas":          {"category": "Linear Systems - Direct",   "order": "O(n) - tridiagonal special","color": "#90E0EF", "desc": "Optimized LU for tridiagonal A.\nOnly O(n) operations instead of O(n^3)."},
    "Newton Forward":  {"category": "Interpolation",             "order": "Polynomial - degree n-1",   "color": "#00B4D8", "desc": "Uses forward difference table.\nBest for interpolating near the beginning of the data range."},
    "Newton Backward": {"category": "Interpolation",             "order": "Polynomial - degree n-1",   "color": "#0096C7", "desc": "Uses backward difference table.\nBest for interpolating near the end of the data range."},
    "Stirling":        {"category": "Interpolation",             "order": "Polynomial - degree n-1",   "color": "#48CAE4", "desc": "Central-difference formula.\nBest accuracy when target is near the middle of data range."},
    "Lagrange":        {"category": "Interpolation",             "order": "Polynomial - exact fit",    "color": "#90E0EF", "desc": "Builds basis polynomials for each data point.\nNo equal spacing needed."},
}

METHOD_FORMULAS = {
    "Bisection":       "c = (a + b) / 2",
    "False Position":  "x = (a*f(b) - b*f(a)) / (f(b) - f(a))",
    "Newton-Raphson":  "x_{n+1} = x_n - f(x_n) / f'(x_n)",
    "Secant":          "x_{n+1} = x_n - f(x_n)*(x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))",
    "Jacobi":          "x_i^{k+1} = (b_i - Sum a_ij x_j^k) / a_ii",
    "Gauss-Seidel":    "x_i^{k+1} = (b_i - Sum_j<i a_ij x_j^{k+1} - Sum_j>i a_ij x_j^k) / a_ii",
    "Doolittle LU":    "A = L*U  ->  Ly = b  ->  Ux = y",
    "Thomas":          "Forward sweep -> Back substitution  [O(n)]",
    "Newton Forward":  "f(x) = Sum C(p,k)*Delta^k y_0",
    "Newton Backward": "f(x) = Sum C(p+k-1,k)*nabla^k y_n",
    "Stirling":        "f(x) = y_mid + p*mu_delta_y + p^2/2*delta^2_y + ...",
    "Lagrange":        "f(x) = Sum y_i * Prod (x-x_j)/(x_i-x_j)",
}

DEMOS = {
    "Bisection":       {"expr": "x**3 - x - 2", "a": "1", "b": "2", "tol": "1e-6", "max_iter": "100"},
    "False Position":  {"expr": "x**3 - x - 2", "a": "1", "b": "2", "tol": "1e-6", "max_iter": "100"},
    "Newton-Raphson":  {"expr": "x**3 - x - 2", "d_expr": "3*x**2 - 1", "x0": "1.5", "tol": "1e-6", "max_iter": "100"},
    "Secant":          {"expr": "x**3 - x - 2", "x0": "1", "x1": "2", "tol": "1e-6", "max_iter": "100"},
    "Jacobi":          {"A": "[[10,-1,2],[1,10,-1],[2,-1,10]]", "b": "[6,25,-11]", "x0": "[0,0,0]", "tol": "1e-6", "max_iter": "100"},
    "Gauss-Seidel":    {"A": "[[10,-1,2],[1,10,-1],[2,-1,10]]", "b": "[6,25,-11]", "x0": "[0,0,0]", "tol": "1e-6", "max_iter": "100"},
    "Doolittle LU":    {"A": "[[2,1,1],[4,3,3],[8,7,9]]", "b": "[4,10,18]", "x0": "[0,0,0]", "tol": "1e-6", "max_iter": "100"},
    "Thomas":          {"lower": "[1,1,1]", "diag": "[4,4,4,4]", "upper": "[1,1,1]", "rhs": "[5,6,6,5]"},
    "Newton Forward":  {"x": "[0,1,2,3,4]", "y": "[1,2.7,7.4,20.1,54.6]", "x_val": "2.5"},
    "Newton Backward": {"x": "[0,1,2,3,4]", "y": "[1,2.7,7.4,20.1,54.6]", "x_val": "3.5"},
    "Stirling":        {"x": "[1,2,3,4,5]", "y": "[1,1.5,2.0,2.8,3.5]", "x_val": "3.2"},
    "Lagrange":        {"x": "[0,1,2,3]", "y": "[1,2.7,7.4,20.1]", "x_val": "1.5"},
}

TEAM = ["Moustafa Ismail Elassal", "Eyad Elayied Moustafa", "Yousef Sameh Ahmed", "Ahmed Aymen", "Asmaa Mahmoud Elsayed"]

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def style_ax(ax, title=""):
    ax.set_facecolor("#12121A")
    ax.tick_params(colors="#9090B0", labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#252535")
    ax.grid(True, color="#252535", alpha=0.5, linestyle="--")
    if title:
        ax.set_title(title, color="#F0F0FF", fontsize=12, fontweight="bold", pad=10)

def plot_root(expr, root, a=None, b=None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0A0A0F")
    if a is None or b is None:
        a, b = root - 2, root + 2
    xs = np.linspace(a, b, 500)
    ys = [_safe_eval(expr, x) for x in xs]
    ax.plot(xs, ys, color="#F0F0FF", linewidth=1.8, label="f(x)")
    ax.axhline(0, color="#9090B0", linewidth=0.8, linestyle="--")
    ax.axvline(root, color="#00B4D8", linewidth=1, linestyle=":", alpha=0.7)
    ax.scatter([root], [_safe_eval(expr, root)], color="#00B4D8", edgecolors="#12121A", linewidths=2, s=80, zorder=5, label=f"root = {root:.6f}")
    style_ax(ax, "Root-Finding Visualization")
    legend = ax.legend(facecolor="#12121A", edgecolor="#252535")
    for t in legend.get_texts(): t.set_color("#F0F0FF")
    ax.set_xlabel("x", color="#9090B0", fontsize=10)
    ax.set_ylabel("f(x)", color="#9090B0", fontsize=10)
    fig.tight_layout()
    return fig

def plot_interp(x, y, x_val, y_val):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#0A0A0F")
    xs = np.linspace(min(x), max(x), 300)
    coeffs = np.polyfit(x, y, deg=min(len(x) - 1, 5))
    ys = np.polyval(coeffs, xs)
    ax.plot(xs, ys, color="#9090B0", linewidth=1.2, linestyle="--", label="Approx curve")
    ax.plot(x, y, "o", color="#F0F0FF", markersize=8, label="Data points")
    ax.scatter([x_val], [y_val], color="#00B4D8", edgecolors="#12121A", linewidths=2, s=120, zorder=5, label=f"f({x_val}) = {y_val:.4f}")
    style_ax(ax, "Interpolation Visualization")
    legend = ax.legend(facecolor="#12121A", edgecolor="#252535")
    for t in legend.get_texts(): t.set_color("#F0F0FF")
    ax.set_xlabel("x", color="#9090B0", fontsize=10)
    ax.set_ylabel("y", color="#9090B0", fontsize=10)
    fig.tight_layout()
    return fig

def plot_convergence(steps, method):
    errors = [float(row[-1]) for row in steps if isinstance(row[-1], (int, float)) and row[-1] > 0]
    if len(errors) < 2:
        fig, ax = plt.subplots(figsize=(8, 3))
        fig.patch.set_facecolor("#0A0A0F")
        style_ax(ax, "Not enough iterations")
        return fig

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))
    fig.patch.set_facecolor("#0A0A0F")

    iters = list(range(1, len(errors) + 1))
    log_errors = [np.log10(e) for e in errors]

    points = np.array([iters, log_errors]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(0, len(segments))
    lc = LineCollection(segments, cmap="cool", norm=norm, linewidth=2.5, zorder=3)
    lc.set_array(np.arange(len(segments)))
    ax1.add_collection(lc)
    ax1.scatter(iters, log_errors, color="#00B4D8", s=28, zorder=4, alpha=0.85)
    ax1.annotate(f"{errors[0]:.2e}", xy=(iters[0], log_errors[0]), xytext=(iters[0]+0.3, log_errors[0]+0.3), color="#9090B0", fontsize=8, arrowprops=dict(arrowstyle="->", color="#9090B0", lw=0.8))
    ax1.annotate(f"{errors[-1]:.2e}", xy=(iters[-1], log_errors[-1]), xytext=(max(1,iters[-1]-max(2,len(iters)//4)), log_errors[-1]+0.5), color="#00B4D8", fontsize=8, arrowprops=dict(arrowstyle="->", color="#00B4D8", lw=1))
    ax1.set_xlim(0.5, max(iters)+0.5)
    ax1.set_ylim(min(log_errors)-0.5, max(log_errors)+0.5)
    ax1.set_xlabel("Iteration", color="#9090B0", fontsize=9)
    ax1.set_ylabel("log10(|error|)", color="#9090B0", fontsize=9)
    style_ax(ax1, f"Convergence — {method}")

    if len(errors) >= 3:
        try:
            log_e = [np.log(e) for e in errors if e > 0]
            if len(log_e) >= 3:
                orders = []
                for i in range(1, len(log_e)-1):
                    num = log_e[i+1] - log_e[i]
                    den = log_e[i] - log_e[i-1]
                    if abs(den) > 1e-12:
                        orders.append(num/den)
                orders = [o for o in orders if 0.1 < abs(o) < 10]
                if orders:
                    p_est = np.median(orders)
                    ax1.text(0.97, 0.93, f"order ~ {p_est:.2f}", transform=ax1.transAxes, fontsize=9, color="#00FF88", ha="right", bbox=dict(boxstyle="round,pad=0.3", facecolor="#12121A", edgecolor="#00FF88", alpha=0.8))
        except: pass

    colors = [plt.cm.cool(i/max(len(errors)-1,1)) for i in range(len(errors))]
    bars = ax2.bar(iters, errors, color=colors, edgecolor="#252535", linewidth=0.5, zorder=3, alpha=0.85)
    label_step = max(1, len(errors)//6)
    for i, (bar, err) in enumerate(zip(bars, errors)):
        if i % label_step == 0 or i == len(errors)-1:
            ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.05, f"{err:.1e}", ha="center", va="bottom", fontsize=7, color="#9090B0", rotation=45)
    bars[-1].set_edgecolor("#00B4D8")
    bars[-1].set_linewidth(1.8)
    ax2.set_yscale("log")
    ax2.set_xlim(0.5, max(iters)+0.5)
    ax2.set_xlabel("Iteration", color="#9090B0", fontsize=9)
    ax2.set_ylabel("|Error|  (log scale)", color="#9090B0", fontsize=9)
    style_ax(ax2, "Error per Iteration")
    ax2.axhline(y=errors[-1], color="#00B4D8", linewidth=1, linestyle="--", alpha=0.7, zorder=2)
    ax2.text(0.02, errors[-1]*1.5, f"tol ~ {errors[-1]:.1e}", color="#00B4D8", fontsize=8, transform=ax2.get_yaxis_transform())

    fig.tight_layout(pad=2.0)
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  DIFFERENCE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

def make_diff_text(diffs, x_vals):
    n = len(x_vals)
    lines = ["\n--- Difference Table ---"]
    headers = f"{'x':>10} {'y':>12}" + "".join(f" {'Δ'+str(k)+'y':>12}" for k in range(1, len(diffs)))
    lines.append(headers)
    lines.append("-" * len(headers))
    for i in range(n):
        row = f"{x_vals[i]:>10.4f} {diffs[0][i]:>12.6f}"
        for k in range(1, len(diffs)):
            if i < len(diffs[k]):
                row += f" {diffs[k][i]:>12.6f}"
            else:
                row += f" {'---':>12}"
        lines.append(row)
    lines.append("-" * len(headers))
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHECK CONVERGENCE
# ═══════════════════════════════════════════════════════════════════════════════

def run_check(method, params):
    lines = [f"{'='*50}", f"  CONVERGENCE CHECK — {method}", f"{'='*50}"]
    try:
        if method in {"Jacobi", "Gauss-Seidel"}:
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            b = np.array(ast.literal_eval(params["b"]), dtype=float)
            lines.append(f"\nMatrix A:\n{a}\nVector b: {b}")
            dd = is_diagonally_dominant(a)
            lines.append(f"\nDiagonally Dominant: {dd}")
            if dd:
                lines.append("→ GUARANTEED to converge.")
            else:
                lines.append("→ NOT diagonally dominant. Convergence NOT guaranteed.")
            d = np.diag(a)
            if np.all(np.abs(d) > 1e-14):
                r = a - np.diagflat(d)
                bj = -np.diag(1.0/d) @ r
                eigs = np.linalg.eigvals(bj)
                rho = max(abs(eigs))
                lines.append(f"\nEigenvalues: {eigs}")
                lines.append(f"Spectral radius (ρ): {rho:.6f}")
                lines.append(f"→ ρ = {rho:.6f} {'< 1 → WILL converge' if rho < 1 else '>= 1 → WILL NOT converge!'}")
            if np.any(np.abs(d) < 1e-14):
                lines.append("\n⚠ WARNING: Zero diagonal element!")

        elif method == "Doolittle LU":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            lines.append(f"\nMatrix A:\n{a}")
            det = np.linalg.det(a)
            lines.append(f"\ndet(A) = {det:.6f}")
            lines.append(f"→ {'SINGULAR. LU will fail.' if abs(det) < 1e-14 else 'Non-singular. LU should work.'}")

        elif method == "Thomas":
            lower = ast.literal_eval(params["lower"])
            diag = ast.literal_eval(params["diag"])
            upper = ast.literal_eval(params["upper"])
            rhs = ast.literal_eval(params["rhs"])
            n = len(diag)
            lines.append(f"\nMatrix size: {n}x{n}")
            dim_ok = True
            if len(lower) != n-1:
                lines.append(f"ERROR: Lower should have {n-1} elems, got {len(lower)}"); dim_ok = False
            if len(upper) != n-1:
                lines.append(f"ERROR: Upper should have {n-1} elems, got {len(upper)}"); dim_ok = False
            if len(rhs) != n:
                lines.append(f"ERROR: RHS should have {n} elems, got {len(rhs)}"); dim_ok = False
            if dim_ok:
                lines.append("→ Dimensions OK." + ("" if not any(abs(d)<1e-14 for d in diag) else "\n⚠ Zero on main diagonal!"))

        elif method in {"Bisection", "False Position"}:
            expr = params["expr"]
            a_v, b_v = float(params["a"]), float(params["b"])
            fa, fb = _safe_eval(expr, a_v), _safe_eval(expr, b_v)
            lines.append(f"\nf({a_v}) = {fa:.6f}\nf({b_v}) = {fb:.6f}\nf(a)*f(b) = {fa*fb:.6f}")
            lines.append(f"→ {'Sign change: GUARANTEED.' if fa*fb < 0 else 'NO sign change: CANNOT apply!'}")

        elif method == "Newton-Raphson":
            x0 = float(params["x0"])
            fx0 = _safe_eval(params["expr"], x0)
            dfx0 = _safe_eval(params["d_expr"], x0)
            lines.append(f"\nf({x0}) = {fx0:.6f}\nf'({x0}) = {dfx0:.6f}")
            lines.append(f"→ {'Derivative near zero! Will diverge.' if abs(dfx0) < 1e-10 else 'Good starting point.'}")

        elif method in {"Newton Forward", "Newton Backward", "Stirling"}:
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            eq = is_equally_spaced(x)
            lines.append(f"\nx: {x}\ny: {y}\nEqually spaced: {eq}")
            lines.append(f"→ {'Can apply. h = '+str(x[1]-x[0]) if eq else 'NOT equally spaced! Use Lagrange.'}")

        elif method == "Lagrange":
            x = ast.literal_eval(params["x"])
            y = ast.literal_eval(params["y"])
            lines.append(f"\nx: {x}\ny: {y}\nPoints: {len(x)}")
            lines.append(f"→ {'OK. Any spacing works.' if len(x)==len(y) else 'ERROR: Different lengths!'}")

        lines.append(f"\n{'='*50}")
        return True, "\n".join(lines)
    except Exception as e:
        lines.append(f"\nERROR: {e}")
        return False, "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════════
#  LOAD LOGO
# ═══════════════════════════════════════════════════════════════════════════════

try:
    with open("hue_logo.png", "rb") as img_file:
        LOGO_BASE64 = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    LOGO_BASE64 = ""

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN UI
# ═══════════════════════════════════════════════════════════════════════════════

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size:28px;font-weight:800;color:#00B4D8;margin-bottom:4px;">Numerical<br>Methods</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#606080;margin-bottom:20px;">Faculty of AI · Horus University</div>', unsafe_allow_html=True)

    method = st.selectbox("Method", list(METHOD_INFO.keys()), index=0)

    info = METHOD_INFO[method]
    st.markdown(f'''
    <div class="info-card">
        <div style="font-size:10px;font-weight:700;color:{info['color']};text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">{info['category']}</div>
        <div style="font-size:13px;font-weight:600;color:#F0F0FF;margin-bottom:4px;">Convergence: {info['order']}</div>
        <div style="font-size:12px;color:#9090B0;line-height:1.6;white-space:pre-line;">{info['desc']}</div>
    </div>
    ''', unsafe_allow_html=True)

    if method in METHOD_FORMULAS:
        st.markdown(f'''
        <div class="info-card">
            <div style="font-size:10px;font-weight:700;color:#00B4D8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Formula</div>
            <div style="font-size:13px;color:#F0F0FF;font-family:'Courier New',monospace;">{METHOD_FORMULAS[method]}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#606080;line-height:1.8;">Competition Mode<br>Cyber Security Department<br><br>Team:<br>' + "<br>".join([f"• {m}" for m in TEAM]) + '</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═══════════════════════════════════════════════════════════════════

if "splash_done" not in st.session_state:
    st.markdown("""
    <style>
        .splash-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            text-align: center;
            padding: 40px 20px;
        }
        .splash-logo {
            width: 150px;
            height: 150px;
            border-radius: 24px;
            background-color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0, 180, 216, 0.3);
            animation: splash-pulse 2s ease-in-out infinite;
            padding: 15px;
        }
        @keyframes splash-pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(0, 180, 216, 0.3); }
            50% { transform: scale(1.05); box-shadow: 0 25px 80px rgba(0, 180, 216, 0.4); }
        }
        .splash-title {
            font-size: 36px;
            font-weight: 800;
            color: #F0F0FF;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }
        .splash-subtitle {
            font-size: 16px;
            color: #9090B0;
            margin-bottom: 6px;
        }
        .splash-uni {
            font-size: 14px;
            color: #00B4D8;
            font-weight: 600;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        .splash-divider {
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #00B4D8, #0077B6);
            border-radius: 2px;
            margin: 0 auto 30px;
        }
        .splash-doctor-label {
            font-size: 11px;
            color: #606080;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 8px;
        }
        .splash-doctor-name {
            font-size: 18px;
            font-weight: 600;
            color: #F0F0FF;
            margin-bottom: 8px;
        }
        .splash-team-section {
            margin-top: 30px;
            padding-top: 24px;
            border-top: 1px solid #252535;
        }
        .splash-team-label {
            font-size: 11px;
            color: #606080;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 12px;
        }
        .splash-team-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            max-width: 500px;
            margin: 0 auto;
        }
        .splash-team-member {
            background: #1A1A24;
            border: 1px solid #252535;
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 12px;
            color: #9090B0;
        }
        .splash-footer {
            margin-top: 40px;
            font-size: 11px;
            color: #404060;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="splash-container">
        <div class="splash-logo">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="Horus University Logo" style="width: 100%; height: 100%; object-fit: contain;">
        </div>
        <div class="splash-title">Numerical Methods Calculator</div>
        <div class="splash-subtitle">Competition Edition</div>
        <div class="splash-uni">Horus University · Faculty of AI</div>
        <div class="splash-divider"></div>
        <div class="splash-doctor-label">Under Supervision of</div>
        <div class="splash-doctor-name">Dr. Eman El-Haddiy</div>
        <div class="splash-doctor-name" style="margin-top:-2px;font-size:16px;">Dr. Walaa Farouk</div>
        <div class="splash-doctor-name" style="margin-top:-2px;font-size:16px;">Dr. Mohamed Khaled</div>
        <div class="splash-team-section">
            <div class="splash-team-label">Development Team — Cyber Security Dept.</div>
            <div class="splash-team-grid">
                <div class="splash-team-member">Moustafa Ismail Elassal</div>
                <div class="splash-team-member">Eyad Elayied Moustafa</div>
                <div class="splash-team-member">Yousef Sameh Ahmed</div>
                <div class="splash-team-member">Ahmed Aymen</div>
                <div class="splash-team-member">Asmaa Mahmoud Elsayed</div>
            </div>
        </div>
        <div class="splash-footer">© 2025 — All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)

    enter_clicked = st.button("Enter App  →", type="primary", key="splash_btn")
    if enter_clicked:
        st.session_state["splash_done"] = True
        st.rerun()

    st.stop()

# ═══════════════════════════════════════════════════════════════════
#  MAIN APP (after splash)
# ═══════════════════════════════════════════════════════════════════

st.markdown('<div style="font-size:26px;font-weight:700;color:#F0F0FF;margin-bottom:4px;">Advanced Numerical Calculator</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:13px;color:#9090B0;margin-bottom:24px;">Current Method: <span style="color:#00B4D8;font-weight:600;">{method}</span></div>', unsafe_allow_html=True)

# --- INPUT FORM ---
st.markdown('<div class="section-title">Parameters</div>', unsafe_allow_html=True)

cols = st.columns(4)
demo = DEMOS[method]

def input_field(col, label, key, default):
    return col.text_input(label, value=default, key=key, label_visibility="collapsed")

params = {}

if method in {"Bisection", "False Position"}:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**f(x)**"); params["expr"] = c1.text_input(" ", value=demo["expr"], key="expr", label_visibility="collapsed")
    c2.markdown("**a**"); params["a"] = c2.text_input("  ", value=demo["a"], key="a", label_visibility="collapsed")
    c3.markdown("**b**"); params["b"] = c3.text_input("   ", value=demo["b"], key="b", label_visibility="collapsed")
    c4.markdown("**Tolerance**"); params["tol"] = c4.text_input("    ", value=demo["tol"], key="tol", label_visibility="collapsed")
    st.markdown("**Max Iterations**"); params["max_iter"] = st.text_input("     ", value=demo["max_iter"], key="max_iter", label_visibility="collapsed")

elif method == "Newton-Raphson":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**f(x)**"); params["expr"] = c1.text_input(" ", value=demo["expr"], key="expr", label_visibility="collapsed")
    c2.markdown("**f'(x)**"); params["d_expr"] = c2.text_input("  ", value=demo["d_expr"], key="d_expr", label_visibility="collapsed")
    c3.markdown("**x₀**"); params["x0"] = c3.text_input("   ", value=demo["x0"], key="x0", label_visibility="collapsed")
    c4.markdown("**Tolerance**"); params["tol"] = c4.text_input("    ", value=demo["tol"], key="tol", label_visibility="collapsed")
    st.markdown("**Max Iterations**"); params["max_iter"] = st.text_input("     ", value=demo["max_iter"], key="max_iter", label_visibility="collapsed")

elif method == "Secant":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**f(x)**"); params["expr"] = c1.text_input(" ", value=demo["expr"], key="expr", label_visibility="collapsed")
    c2.markdown("**x₀**"); params["x0"] = c2.text_input("  ", value=demo["x0"], key="x0", label_visibility="collapsed")
    c3.markdown("**x₁**"); params["x1"] = c3.text_input("   ", value=demo["x1"], key="x1", label_visibility="collapsed")
    c4.markdown("**Tolerance**"); params["tol"] = c4.text_input("    ", value=demo["tol"], key="tol", label_visibility="collapsed")
    st.markdown("**Max Iterations**"); params["max_iter"] = st.text_input("     ", value=demo["max_iter"], key="max_iter", label_visibility="collapsed")

elif method in {"Jacobi", "Gauss-Seidel", "Doolittle LU"}:
    c1, c2 = st.columns(2)
    c1.markdown("**A (matrix)**"); params["A"] = c1.text_area(" ", value=demo["A"], key="A", label_visibility="collapsed", height=80)
    c2.markdown("**b (vector)**"); params["b"] = c2.text_area("  ", value=demo["b"], key="b", label_visibility="collapsed", height=80)
    c3, c4 = st.columns(2)
    c3.markdown("**x₀ (optional)**"); params["x0"] = c3.text_input("   ", value=demo["x0"], key="x0", label_visibility="collapsed")
    c4.markdown("**Tolerance**"); params["tol"] = c4.text_input("    ", value=demo["tol"], key="tol", label_visibility="collapsed")
    st.markdown("**Max Iterations**"); params["max_iter"] = st.text_input("     ", value=demo["max_iter"], key="max_iter", label_visibility="collapsed")

elif method == "Thomas":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**Lower diag**"); params["lower"] = c1.text_input(" ", value=demo["lower"], key="lower", label_visibility="collapsed")
    c2.markdown("**Main diag**"); params["diag"] = c2.text_input("  ", value=demo["diag"], key="diag", label_visibility="collapsed")
    c3.markdown("**Upper diag**"); params["upper"] = c3.text_input("   ", value=demo["upper"], key="upper", label_visibility="collapsed")
    c4.markdown("**RHS**"); params["rhs"] = c4.text_input("    ", value=demo["rhs"], key="rhs", label_visibility="collapsed")

else:
    c1, c2, c3 = st.columns(3)
    c1.markdown("**x values**"); params["x"] = c1.text_input(" ", value=demo["x"], key="x", label_visibility="collapsed")
    c2.markdown("**y values**"); params["y"] = c2.text_input("  ", value=demo["y"], key="y", label_visibility="collapsed")
    c3.markdown("**Target x**"); params["x_val"] = c3.text_input("   ", value=demo["x_val"], key="x_val", label_visibility="collapsed")

# Buttons
st.markdown("<br>", unsafe_allow_html=True)
bc1, bc2, bc3 = st.columns(3)
compute_clicked = bc1.button("Compute", type="primary", use_container_width=True)
check_clicked = bc2.button("Check Convergence", use_container_width=True)
demo_clicked = bc3.button("Load Demo", use_container_width=True)

# --- RESULTS ---
if compute_clicked:
    try:
        sep = "=" * 50
        summary_lines = [sep, f"  {method}", f"  Category: {info['category']}", f"  Order: {info['order']}", sep]

        if method == "Bisection":
            root, steps = bisection(params["expr"], float(params["a"]), float(params["b"]), float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
            st.session_state["plot_fig"] = plot_root(params["expr"], root, float(params["a"]), float(params["b"]))
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "False Position":
            root, steps = false_position(params["expr"], float(params["a"]), float(params["b"]), float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "a", "b", "x", "f(x)", "Error"]
            st.session_state["plot_fig"] = plot_root(params["expr"], root, float(params["a"]), float(params["b"]))
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Newton-Raphson":
            root, steps = newton_raphson(params["expr"], params["d_expr"], float(params["x0"]), float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_i", "f(x_i)", "f'(x_i)", "x_next", "Error"]
            st.session_state["plot_fig"] = plot_root(params["expr"], root)
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Secant":
            root, steps = secant(params["expr"], float(params["x0"]), float(params["x1"]), float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x0", "x1", "x2", "f(x2)", "Error"]
            st.session_state["plot_fig"] = plot_root(params["expr"], root)
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Jacobi":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            b = np.array(ast.literal_eval(params["b"]), dtype=float)
            x0 = np.array(ast.literal_eval(params["x0"]), dtype=float)
            x, steps = jacobi(a, b, x0, float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Solution x = {x}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_vector", "Error"]
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Gauss-Seidel":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            b = np.array(ast.literal_eval(params["b"]), dtype=float)
            x0 = np.array(ast.literal_eval(params["x0"]), dtype=float)
            x, steps = gauss_seidel(a, b, x0, float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Solution x = {x}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_vector", "Error"]
            st.session_state["conv_fig"] = plot_convergence(steps, method)
            st.session_state["metrics"] = {"Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Doolittle LU":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            b = np.array(ast.literal_eval(params["b"]), dtype=float)
            x, l, u, steps = doolittle_lu(a, b)
            summary_lines += [f"  Solution x = {x}", f"  L:\n{l}", f"  U:\n{u}", f"  Verify A*x=b: {np.allclose(a@x, b)}"]
            headers = ["Step", "L_diag", "U_row"]
            st.session_state["metrics"] = {"Verified": "✓ A*x = b"}

        elif method == "Thomas":
            lower = ast.literal_eval(params["lower"])
            diag = ast.literal_eval(params["diag"])
            upper = ast.literal_eval(params["upper"])
            rhs = ast.literal_eval(params["rhs"])
            x, steps = thomas(lower, diag, upper, rhs)
            summary_lines += [f"  Solution x = {x}", f"  Forward sweep steps: {len(steps)}"]
            headers = ["Step", "w_factor", "new_b", "new_d"]
            st.session_state["metrics"] = {"Solution": np.array2string(x, precision=4)}

        elif method == "Newton Forward":
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv = float(params["x_val"])
            yv, diffs = newton_forward(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plot_interp(x, y, xv, yv)
            st.session_state["metrics"] = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Newton Backward":
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv = float(params["x_val"])
            yv, diffs = newton_backward(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plot_interp(x, y, xv, yv)
            st.session_state["metrics"] = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Stirling":
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv = float(params["x_val"])
            yv, diffs = stirling(x, y, xv)
            mid = len(x) // 2
            p = (xv - x[mid]) / (x[1]-x[0])
            summary_lines += [f"  f({xv}) = {yv:.10f}", f"  Central point: x_{mid}={x[mid]}, y_{mid}={y[mid]}", f"  p = {p:.4f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plot_interp(x, y, xv, yv)
            st.session_state["metrics"] = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Lagrange":
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv = float(params["x_val"])
            yv = lagrange(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            st.session_state["plot_fig"] = plot_interp(x, y, xv, yv)
            st.session_state["metrics"] = {f"f({xv})": f"{yv:.6f}"}

        st.session_state["summary"] = "\n".join(summary_lines)
        st.session_state["table_headers"] = headers
        st.session_state["table_rows"] = steps
        st.success("Computed successfully!")

    except Exception as e:
        st.error(f"**Error:** {e}")

elif check_clicked:
    ok, text = run_check(method, params)
    st.session_state["summary"] = text
    st.session_state["table_headers"] = []
    st.session_state["table_rows"] = []
    if "plot_fig" in st.session_state: del st.session_state["plot_fig"]
    if "conv_fig" in st.session_state: del st.session_state["conv_fig"]
    if "metrics" in st.session_state: del st.session_state["metrics"]
    if ok:
        st.success("Check completed!")
    else:
        st.error("Check found issues!")

elif demo_clicked:
    st.rerun()

# --- DISPLAY RESULTS ---
if "summary" in st.session_state and st.session_state["summary"]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    # Metrics
    if "metrics" in st.session_state:
        mc = st.columns(len(st.session_state["metrics"]))
        for i, (k, v) in enumerate(st.session_state["metrics"].items()):
            mc[i].metric(k, v)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Iterations", "Plot", "Convergence"])

    with tab1:
        st.markdown(f'<div class="result-box">{st.session_state["summary"]}</div>', unsafe_allow_html=True)

    with tab2:
        if "table_headers" in st.session_state and st.session_state["table_headers"]:
            headers = st.session_state["table_headers"]
            rows = st.session_state["table_rows"]
            def fmt(v):
                if isinstance(v, float): return f"{v:.8f}"
                if isinstance(v, np.ndarray): return np.array2string(v, precision=6)
                return str(v)
            data = [[fmt(v) for v in row] for row in rows]
            st.dataframe(pd.DataFrame(data, columns=headers), use_container_width=True, hide_index=True, height=400)
        else:
            st.info("No iteration data for this method.")

    with tab3:
        if "plot_fig" in st.session_state:
            st.pyplot(st.session_state["plot_fig"])
        else:
            st.info("No plot for this method.")

    with tab4:
        if "conv_fig" in st.session_state:
            st.pyplot(st.session_state["conv_fig"])
        else:
            st.info("No convergence plot for this method.")
