# ══════════════════════════════════════════════════════════════════════════════
#   Numerical Methods Calculator — Premium Web Edition
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
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
#  PREMIUM DARK THEME CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    :root {
        --bg-main: #05050A;
        --bg-panel: rgba(16, 16, 28, 0.65);
        --bg-soft: rgba(28, 28, 45, 0.6);
        --border: rgba(120, 140, 200, 0.2);
        --border-strong: rgba(0, 180, 216, 0.45);
        --text-main: #F5F5FF;
        --text-muted: #9090B0;
        --accent: #00B4D8;
        --accent-2: #7B5BFF;
        --accent-hover: #0096C7;
        --success: #00FF88;
        --error: #FF4455;
        --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    }

    .stApp {
        background:
            radial-gradient(1200px 700px at 10% -10%, rgba(0,180,216,0.2), transparent 60%),
            radial-gradient(1000px 800px at 110% 10%, rgba(123,91,255,0.18), transparent 60%),
            radial-gradient(800px 600px at 50% 120%, rgba(0,255,136,0.12), transparent 60%),
            #05050A;
        background-attachment: fixed;
        color: var(--text-main);
        font-family: var(--font-main);
    }

    .stApp::before {
        content: "";
        position: fixed; inset: 0;
        background-image:
            linear-gradient(rgba(120,140,200,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(120,140,200,0.06) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
        animation: gridShift 60s linear infinite;
    }
    @keyframes gridShift {
        from { background-position: 0 0, 0 0; }
        to   { background-position: 40px 40px, 40px 40px; }
    }

    .block-container { position: relative; z-index: 1; padding-top: 2.5rem; padding-bottom: 2.5rem; max-width: 1200px; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(12,12,20,0.9), rgba(6,6,12,0.95));
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-right: 1px solid var(--border-strong);
        box-shadow: 5px 0 25px rgba(0,0,0,0.5);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(18,18,32,0.8) !important;
        color: var(--text-main) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        font-family: var(--font-mono) !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(0,180,216,0.2), 0 6px 20px rgba(0,180,216,0.15) !important;
        transform: translateY(-2px);
    }
    .stSelectbox > div > div {
        background-color: rgba(18,18,32,0.8) !important;
        color: var(--text-main) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
    }

    .stDataFrame, div[data-testid="stMetric"], .info-card, .result-box,
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-panel) !important;
        backdrop-filter: blur(20px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(150%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .stDataFrame thead th {
        background: linear-gradient(180deg, rgba(0,180,216,0.15), rgba(0,180,216,0.05)) !important;
        color: var(--accent) !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 14px !important;
        border-bottom: 2px solid var(--border-strong) !important;
        font-family: var(--font-main) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stDataFrame tbody td {
        background: transparent !important;
        color: var(--text-main) !important;
        text-align: center !important;
        padding: 10px !important;
        border-bottom: 1px solid rgba(120,140,200,0.1) !important;
        font-family: var(--font-mono) !important;
        font-size: 13px !important;
    }
    .stDataFrame tbody tr:hover td {
        background: rgba(0,180,216,0.08) !important;
    }

    div[data-testid="stMetric"] {
        padding: 20px !important;
        transition: transform .3s ease, box-shadow .3s ease;
        border: 1px solid var(--border) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 45px rgba(0,180,216,0.25);
        border-color: var(--accent) !important;
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 13px !important;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: var(--font-mono) !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }

    h1, h2, h3, h4 { color: var(--text-main) !important; font-family: var(--font-main) !important; letter-spacing: -0.03em; font-weight: 800 !important;}
    p, label { color: var(--text-muted) !important; }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        color: #fff;
        border: none;
        border-radius: 16px;
        font-weight: 800;
        padding: 16px 32px;
        font-size: 16px;
        letter-spacing: 0.5px;
        width: 100%;
        box-shadow: 0 10px 30px rgba(0,180,216,0.4), inset 0 2px 0 rgba(255,255,255,0.2);
        transition: all 0.3s cubic-bezier(.2,.8,.2,1);
        position: relative;
        overflow: hidden;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 18px 45px rgba(0,180,216,0.55), inset 0 2px 0 rgba(255,255,255,0.3);
        filter: brightness(1.1);
    }
    .stButton > button[kind="primary"]:active { transform: translateY(0) scale(0.98); }

    .stButton > button[kind="secondary"] {
        background: rgba(30,30,48,0.7);
        backdrop-filter: blur(12px);
        color: var(--text-main);
        border: 1.5px solid var(--border);
        border-radius: 16px;
        font-weight: 700;
        padding: 14px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--border-strong);
        background: rgba(0,180,216,0.1);
        box-shadow: 0 0 15px rgba(0,180,216,0.1);
    }

    .stTabs [data-baseweb="tab-list"] { gap: 6px; padding: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-muted);
        border-radius: 12px;
        padding: 11px 20px;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text-main); background: rgba(255,255,255,0.04); }
    .stTabs [data-baseweb="tab-highlight"] { background: transparent; }
    .stTabs [aria-selected="true"] {
        color: #fff !important;
        background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,180,216,0.4);
    }

    .stDataFrame, div[data-testid="stMetric"], .result-box, .stSuccess, .stError, .stWarning, .stInfo {
        animation: fadeUp 0.5s cubic-bezier(.2,.8,.2,1) both;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 14px !important;
        padding: 16px 20px !important;
        backdrop-filter: blur(14px);
        border: 1px solid var(--border) !important;
    }
    .stSuccess { border-left: 4px solid var(--success) !important; }
    .stError   { border-left: 4px solid var(--error) !important; }

    .info-card {
        padding: 18px;
        margin-bottom: 14px;
        background: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }
    .result-box {
        padding: 20px;
        font-family: var(--font-mono);
        font-size: 14px;
        line-height: 1.9;
        color: var(--text-main);
        white-space: pre-wrap;
        overflow-x: auto;
        background: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
    }

    .section-title {
        color: var(--text-main) !important;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-strong);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .error-banner {
        background: rgba(255,68,85,0.08);
        border: 1.5px solid #FF4455;
        border-left: 5px solid #FF4455;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 20px;
        font-family: var(--font-mono, monospace);
        animation: fadeUp 0.4s ease both;
    }
    .error-banner-title {
        font-size: 13px;
        font-weight: 800;
        color: #FF4455;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .error-banner-msg {
        font-size: 13px;
        color: #FF8899;
        line-height: 1.6;
        word-break: break-word;
    }
    .error-banner-hint {
        font-size: 11px;
        color: #705060;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,68,85,0.2);
    }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,180,216,0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,180,216,0.5); }

    .streamlit-expanderHeader {
        background: var(--bg-soft) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    @media (max-width: 768px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .stButton > button { padding: 12px 18px; font-size: 15px; }
        .stDataFrame tbody td { font-size: 11px !important; padding: 6px !important; }
        div[data-testid="stMetricValue"] { font-size: 22px !important; }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  VALIDATORS & SAFE EVAL
# ═══════════════════════════════════════════════════════════════════════════════

def is_diagonally_dominant(a):
    mat = np.array(a, dtype=float)
    for i in range(mat.shape[0]):
        if abs(mat[i, i]) < np.sum(np.abs(mat[i, :])) - abs(mat[i, i]):
            return False
    return True

def is_equally_spaced(x, tol=1e-12):
    arr = np.array(x, dtype=float)
    if len(arr) < 2: return True
    diffs = np.diff(arr)
    return np.max(np.abs(diffs - diffs[0])) <= tol

_EXPR_CACHE: dict = {}
_MATH_GLOBALS = {
    "__builtins__": {},
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "exp": math.exp, "log": math.log, "log10": math.log10,
    "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "abs": abs,
}

def _normalize_expr(expr: str) -> str:
    expr = expr.replace('^', '**')
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z\d\(])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr)
    return expr

def _compile_expr(expr: str):
    code = _EXPR_CACHE.get(expr)
    if code is None:
        code = compile(_normalize_expr(expr), "<expr>", "eval")
        _EXPR_CACHE[expr] = code
    return code

def _safe_eval(expr, x):
    code = _compile_expr(expr)
    return eval(code, _MATH_GLOBALS, {"x": x})

# ═══════════════════════════════════════════════════════════════════════════════
#  CORE MATHEMATICAL METHODS
# ═══════════════════════════════════════════════════════════════════════════════

def bisection(expr, a, b, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    fa = _safe_eval(expr, a)
    fb = _safe_eval(expr, b)
    if fa * fb >= 0: raise ValueError("Bisection requires f(a)*f(b) < 0.")
    steps, c, converged = [], a, False
    for i in range(1, max_iter + 1):
        c_old = c
        c = (a + b) / 2.0
        fc = _safe_eval(expr, c)
        err = abs(c - c_old)
        steps.append((i, a, b, c, fc, err))
        if abs(fc) < tol or err < tol: converged = True; break
        if fa * fc < 0: b, fb = c, fc
        else: a, fa = c, fc
    if not converged and len(steps) == 1: raise RuntimeError("Convergence check appears inverted!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return c, steps

def false_position(expr, a, b, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if tol > 0.5: raise ValueError("Tolerance suspiciously large (>0.5).")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    fa, fb = _safe_eval(expr, a), _safe_eval(expr, b)
    if fa * fb >= 0: raise ValueError("False Position requires f(a)*f(b) < 0.")
    steps, x, converged = [], a, False
    for i in range(1, max_iter + 1):
        x_old = x
        x = (a * fb - b * fa) / (fb - fa)
        fx = _safe_eval(expr, x)
        err = abs(x - x_old)
        steps.append((i, a, b, x, fx, err))
        if abs(fx) < tol or err < tol: converged = True; break
        if fa * fx < 0: b, fb = x, fx
        else: a, fa = x, fx
    if not converged and len(steps) == 1: raise RuntimeError("Convergence check appears inverted!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x, steps

def newton_raphson(expr, d_expr, x0, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    h = 1e-5
    try:
        num_dfx0 = (_safe_eval(expr, x0 + h) - _safe_eval(expr, x0 - h)) / (2 * h)
        user_dfx0 = _safe_eval(d_expr, x0)
        error_margin = abs(num_dfx0) * 0.05 + 0.1
        if abs(user_dfx0 - num_dfx0) > error_margin:
            raise ValueError(f"Math Error: f'(x) is NOT the correct derivative of f(x) at x0={x0}.")
    except ValueError: raise
    except Exception: pass
    steps, x, converged = [], x0, False
    for i in range(1, max_iter + 1):
        fx, dfx = _safe_eval(expr, x), _safe_eval(d_expr, x)
        if abs(dfx) < 1e-14: raise ValueError("Derivative near zero; Newton-Raphson may diverge.")
        x_new = x - fx / dfx
        err = abs(x_new - x)
        steps.append((i, x, fx, dfx, x_new, err))
        x = x_new
        if abs(fx) < tol or err < tol: converged = True; break
    if not converged and len(steps) == 1: raise RuntimeError("Convergence check appears inverted!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x, steps

def secant(expr, x0, x1, tol=1e-6, max_iter=100):
    if tol <= 0: raise ValueError("Tolerance must be positive.")
    if max_iter < 1: raise ValueError("max_iter must be >= 1.")
    steps, converged = [], False
    for i in range(1, max_iter + 1):
        f0, f1 = _safe_eval(expr, x0), _safe_eval(expr, x1)
        denom = f1 - f0
        if abs(denom) < 1e-14: raise ValueError("Secant denominator near zero.")
        x2 = x1 - f1 * (x1 - x0) / denom
        err = abs(x2 - x1)
        steps.append((i, x0, x1, x2, _safe_eval(expr, x2), err))
        x0, x1 = x1, x2
        if err < tol or abs(_safe_eval(expr, x2)) < tol: converged = True; break
    if not converged and len(steps) == 1: raise RuntimeError("Convergence check appears inverted!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters. Error: {err:.2e}")
    return x1, steps

def doolittle_lu(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n): raise ValueError(f"Matrix A must be {n}x{n}.")
    l, u, steps = np.eye(n), np.zeros((n, n), dtype=float), []
    for i in range(n):
        for k in range(i, n): u[i, k] = a[i, k] - np.sum(l[i, :i] * u[:i, k])
        if abs(u[i, i]) < 1e-14: raise ValueError("Zero pivot found in LU decomposition.")
        for k in range(i + 1, n): l[k, i] = (a[k, i] - np.sum(l[k, :i] * u[:i, i])) / u[i, i]
        steps.append((i + 1, l.copy(), u.copy()))
    y = np.zeros(n, dtype=float)
    for i in range(n): y[i] = b[i] - np.dot(l[i, :i], y[:i])
    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1): x[i] = (y[i] - np.dot(u[i, i + 1:], x[i + 1:])) / u[i, i]
    return x, l, u, steps

def thomas(lower, diag, upper, rhs):
    n = len(diag)
    a, b, c, d = (np.array(lower, dtype=float).copy(), np.array(diag, dtype=float).copy(),
                  np.array(upper, dtype=float).copy(), np.array(rhs, dtype=float).copy())
    steps = []
    for i in range(1, n):
        if abs(b[i - 1]) < 1e-14: raise ValueError("Zero pivot in Thomas algorithm.")
        w = a[i - 1] / b[i - 1]
        b[i], d[i] = b[i] - w * c[i - 1], d[i] - w * d[i - 1]
        steps.append((i, w, b[i], d[i]))
    x = np.zeros(n, dtype=float)
    x[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1): x[i] = (d[i] - c[i] * x[i + 1]) / b[i]
    return x, steps

def jacobi(a, b, x0=None, tol=1e-6, max_iter=100):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n): raise ValueError(f"Matrix A must be {n}x{n}.")
    if tol <= 0 or tol > 0.1: raise ValueError("Invalid Tolerance.")
    if max_iter < 1: raise ValueError("max_iter must be at least 1.")
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    d = np.diag(a)
    if np.any(np.abs(d) < 1e-14): raise ValueError("Zero diagonal element found.")
    r = a - np.diagflat(d)
    steps, converged, final_err = [], False, float('inf')
    for i in range(1, max_iter + 1):
        x_new = (b - np.dot(r, x)) / d
        final_err = np.linalg.norm(x_new - x, ord=np.inf)
        steps.append((i, x_new.copy(), final_err))
        x = x_new
        if final_err < tol: converged = True; break
    if not converged and len(steps) == 1 and final_err > tol: raise RuntimeError("CONVERGENCE CHECK APPEARS INVERTED!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters.")
    return x, steps

def gauss_seidel(a, b, x0=None, tol=1e-6, max_iter=100):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n = len(b)
    if a.shape != (n, n): raise ValueError(f"Matrix A must be {n}x{n}.")
    if tol <= 0 or tol > 0.1: raise ValueError("Invalid Tolerance.")
    if max_iter < 1: raise ValueError("max_iter must be at least 1.")
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    steps, converged, final_err = [], False, float('inf')
    for i in range(1, max_iter + 1):
        x_old = x.copy()
        for j in range(n):
            if abs(a[j, j]) < 1e-14: raise ValueError(f"Zero diagonal element at row {j}.")
            x[j] = (b[j] - np.dot(a[j, :j], x[:j]) - np.dot(a[j, j + 1:], x_old[j + 1:])) / a[j, j]
        final_err = np.linalg.norm(x - x_old, ord=np.inf)
        steps.append((i, x.copy(), final_err))
        if final_err < tol: converged = True; break
    if not converged and len(steps) == 1 and final_err > tol: raise RuntimeError("CONVERGENCE CHECK APPEARS INVERTED!")
    if not converged: warnings.warn(f"No convergence after {max_iter} iters.")
    return x, steps

def _forward_differences(y):
    table = [np.array(y, dtype=float)]
    while len(table[-1]) > 1: table.append(np.diff(table[-1]))
    return table

def _backward_differences(y):
    table = [np.array(y, dtype=float)]
    while len(table[-1]) > 1: table.append(np.diff(table[-1]))
    return table

def newton_forward(x, y, x_val):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Newton forward requires equally spaced x values.")
    h, p = x[1] - x[0], (x_val - x[0]) / h
    diffs = _forward_differences(y)
    result, p_term, fact = y[0], 1.0, 1.0
    for k in range(1, len(y)):
        p_term *= p - (k - 1); fact *= k
        result += (p_term / fact) * diffs[k][0]
    return result, diffs

def newton_backward(x, y, x_val):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Newton backward requires equally spaced x values.")
    h, p = x[1] - x[0], (x_val - x[-1]) / h
    diffs = _backward_differences(y)
    result, p_term, fact = y[-1], 1.0, 1.0
    for k in range(1, len(y)):
        p_term *= p + (k - 1); fact *= k
        result += (p_term / fact) * diffs[k][-1]
    return result, diffs

def stirling(x, y, x_val):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    if not is_equally_spaced(x): raise ValueError("Stirling requires equally spaced x values.")
    if len(x) < 3: raise ValueError("Stirling needs at least 3 points.")
    n, h, mid = len(x), x[1] - x[0], len(x) // 2
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
            idx1, idx2 = mid - k // 2 - 1, mid - k // 2
            if idx1 < 0 or idx2 >= len(diffs[k]): break
            d = (diffs[k][idx1] + diffs[k][idx2]) / 2.0
        p_coeff = p if k == 1 else (p ** 2 if k == 2 else (p if k % 2 == 1 else p ** 2))
        if k >= 3:
            for j in range(1, k // 2 + (1 if k % 2 == 1 else 0)): p_coeff *= (p ** 2 - j ** 2)
        result += (p_coeff / fact) * d
    return float(result), diffs

def lagrange(x, y, x_val):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) != len(y): raise ValueError("x and y must have the same length.")
    n, result = len(x), 0.0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j: term *= (x_val - x[j]) / (x[i] - x[j])
        result += term
    return float(result)

# ═══════════════════════════════════════════════════════════════════════════════
#  METHOD INFO & LATEX FORMULAS
# ═══════════════════════════════════════════════════════════════════════════════

METHOD_INFO = {
    "Bisection":       {"category": "Root Finding",               "order": "Linear  (p = 1)",           "color": "#00B4D8", "desc": "Guaranteed convergence by halving the bracket.\nRequires sign change on [a, b]."},
    "False Position":  {"category": "Root Finding",               "order": "Superlinear",               "color": "#0096C7", "desc": "Uses a secant line to approximate the root within a bracket.\nFaster than Bisection in practice."},
    "Newton-Raphson":  {"category": "Root Finding",               "order": "Quadratic  (p = 2)",        "color": "#48CAE4", "desc": "Uses f(x) and f'(x) to converge very fast.\nMay diverge if f'(x) ~ 0."},
    "Secant":          {"category": "Root Finding",               "order": "Superlinear  (p ~ 1.618)",  "color": "#90E0EF", "desc": "Newton-Raphson without derivative.\nTwo initial guesses required."},
    "Jacobi":          {"category": "Linear Systems - Iterative", "order": "Linear  (spectral radius)", "color": "#00B4D8", "desc": "Updates all variables simultaneously using previous-step values.\nNeeds diagonal dominance to converge."},
    "Gauss-Seidel":    {"category": "Linear Systems - Iterative", "order": "Faster than Jacobi",        "color": "#0096C7", "desc": "Updates variables in-place, reusing newly computed values.\nTypically 2x faster than Jacobi."},
    "Doolittle LU":    {"category": "Linear Systems - Direct",    "order": "O(n³) - exact",             "color": "#48CAE4", "desc": "Factorizes A = L·U, then solves two triangular systems.\nExact result in one pass."},
    "Thomas":          {"category": "Linear Systems - Direct",    "order": "O(n) - tridiagonal special","color": "#90E0EF", "desc": "Optimized LU for tridiagonal A.\nOnly O(n) operations instead of O(n³)."},
    "Newton Forward":  {"category": "Interpolation",              "order": "Polynomial - degree n-1",   "color": "#00B4D8", "desc": "Uses forward difference table.\nBest near the beginning of the data range."},
    "Newton Backward": {"category": "Interpolation",              "order": "Polynomial - degree n-1",   "color": "#0096C7", "desc": "Uses backward difference table.\nBest near the end of the data range."},
    "Stirling":        {"category": "Interpolation",              "order": "Polynomial - degree n-1",   "color": "#48CAE4", "desc": "Central-difference formula.\nBest accuracy near the middle of data range."},
    "Lagrange":        {"category": "Interpolation",              "order": "Polynomial - exact fit",    "color": "#90E0EF", "desc": "Builds basis polynomials for each data point.\nNo equal spacing needed."},
}

LATEX_FORMULAS = {
    "Bisection":       r"c = \frac{a + b}{2}",
    "False Position":  r"x = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)}",
    "Newton-Raphson":  r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}",
    "Secant":          r"x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}",
    "Jacobi":          r"x_i^{k+1} = \frac{b_i - \sum_{j \neq i} a_{ij} x_j^k}{a_{ii}}",
    "Gauss-Seidel":    r"x_i^{k+1} = \frac{b_i - \sum_{j<i} a_{ij} x_j^{k+1} - \sum_{j>i} a_{ij} x_j^k}{a_{ii}}",
    "Doolittle LU":    r"A = L \cdot U \rightarrow Ly = b \rightarrow Ux = y",
    "Thomas":          r"\text{Forward sweep} \rightarrow \text{Back substitution} \quad O(n)",
    "Newton Forward":  r"f(x) = \sum_{k=0}^{n} \binom{p}{k} \Delta^k y_0",
    "Newton Backward": r"f(x) = \sum_{k=0}^{n} (-1)^k \binom{-p}{k} \nabla^k y_n",
    "Stirling":        r"f(x) = y_0 + p \mu \delta y_0 + \frac{p^2}{2!} \delta^2 y_0 + \dots",
    "Lagrange":        r"f(x) = \sum_{i=0}^{n} y_i \prod_{j \neq i} \frac{x - x_j}{x_i - x_j}",
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
#  PLOTLY VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def plotly_root(expr, root, a=None, b=None):
    if a is None or b is None: a, b = root - 2, root + 2
    xs = np.linspace(a, b, 500)
    ys = [_safe_eval(expr, x) for x in xs]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)', line=dict(color='#F0F0FF', width=3)))
    fig.add_hline(y=0, line_dash="dash", line_color="#9090B0", opacity=0.5)
    fig.add_vline(x=root, line_dash="dot", line_color="#00B4D8", opacity=0.8)
    fig.add_trace(go.Scatter(x=[root], y=[_safe_eval(expr, root)], mode='markers',
                             name=f'Root = {root:.6f}',
                             marker=dict(color='#00B4D8', size=14, line=dict(width=3, color='#12121A'))))
    fig.update_layout(plot_bgcolor='#12121A', paper_bgcolor='#0A0A0F',
                      font=dict(color='#F0F0FF', family='JetBrains Mono'),
                      margin=dict(l=20, r=20, t=40, b=20),
                      hoverlabel=dict(bgcolor='#1A1A24', font_color='#F0F0FF'))
    fig.update_xaxes(gridcolor='#252535', zeroline=False, title='x')
    fig.update_yaxes(gridcolor='#252535', zeroline=False, title='f(x)')
    return fig

def plotly_interp(x, y, x_val, y_val):
    xs = np.linspace(min(x), max(x), 300)
    coeffs = np.polyfit(x, y, deg=min(len(x) - 1, 5))
    ys = np.polyval(coeffs, xs)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='Approx Curve',
                             line=dict(color='#9090B0', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data Points',
                             marker=dict(color='#F0F0FF', size=10, line=dict(width=2, color='#12121A'))))
    fig.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers',
                             name=f'f({x_val}) = {y_val:.4f}',
                             marker=dict(color='#00B4D8', size=16,
                                         line=dict(width=3, color='#12121A'), symbol='star')))
    fig.update_layout(plot_bgcolor='#12121A', paper_bgcolor='#0A0A0F',
                      font=dict(color='#F0F0FF', family='JetBrains Mono'),
                      margin=dict(l=20, r=20, t=40, b=20),
                      hoverlabel=dict(bgcolor='#1A1A24', font_color='#F0F0FF'))
    fig.update_xaxes(gridcolor='#252535', zeroline=False, title='x')
    fig.update_yaxes(gridcolor='#252535', zeroline=False, title='y')
    return fig

def plotly_convergence(steps, method):
    errors = [float(row[-1]) for row in steps if isinstance(row[-1], (int, float)) and row[-1] > 0]
    if len(errors) < 2:
        fig = go.Figure()
        fig.update_layout(plot_bgcolor='#12121A', paper_bgcolor='#0A0A0F', title="Not enough iterations")
        return fig
    iters = list(range(1, len(errors) + 1))
    log_errors = [np.log10(e) for e in errors]
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Log10(Error) Convergence", "Error per Iteration"))
    fig.add_trace(go.Scatter(x=iters, y=log_errors, mode='lines+markers', name='Log Error',
                             line=dict(color='#00B4D8', width=3), marker=dict(size=8)), row=1, col=1)
    fig.add_trace(go.Bar(x=iters, y=errors, name='Absolute Error',
                         marker_color='#7B5BFF', marker_line_width=0), row=2, col=1)
    fig.update_layout(plot_bgcolor='#12121A', paper_bgcolor='#0A0A0F',
                      font=dict(color='#F0F0FF', family='JetBrains Mono'),
                      margin=dict(l=20, r=20, t=60, b=20),
                      hoverlabel=dict(bgcolor='#1A1A24', font_color='#F0F0FF'), showlegend=False)
    fig.update_xaxes(gridcolor='#252535', zeroline=False, row=1, col=1)
    fig.update_xaxes(gridcolor='#252535', zeroline=False, row=2, col=1)
    fig.update_yaxes(gridcolor='#252535', zeroline=False, title='log₁₀(|err|)', row=1, col=1)
    fig.update_yaxes(gridcolor='#252535', zeroline=False, title='|Error|', type="log", row=2, col=1)
    return fig

def make_diff_text(diffs, x_vals):
    n = len(x_vals)
    lines = ["\n--- Difference Table ---"]
    headers = f"{'x':>10} {'y':>12}" + "".join(f" {'Δ'+str(k)+'y':>12}" for k in range(1, len(diffs)))
    lines.append(headers)
    lines.append("-" * len(headers))
    for i in range(n):
        row = f"{x_vals[i]:>10.4f} {diffs[0][i]:>12.6f}"
        for k in range(1, len(diffs)):
            row += f" {diffs[k][i]:>12.6f}" if i < len(diffs[k]) else f" {'---':>12}"
        lines.append(row)
    lines.append("-" * len(headers))
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════════
#  CONVERGENCE CHECK
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
            lines.append("→ GUARANTEED to converge." if dd else "→ NOT diagonally dominant. Convergence NOT guaranteed.")
            d = np.diag(a)
            if np.all(np.abs(d) > 1e-14):
                r = a - np.diagflat(d)
                bj = -np.diag(1.0/d) @ r
                eigs = np.linalg.eigvals(bj)
                rho = max(abs(eigs))
                lines.append(f"\nEigenvalues: {eigs}\nSpectral radius (ρ): {rho:.6f}")
                lines.append(f"→ ρ = {rho:.6f} {'< 1 → WILL converge' if rho < 1 else '>= 1 → WILL NOT converge!'}")
            if np.any(np.abs(d) < 1e-14): lines.append("\n⚠ WARNING: Zero diagonal element!")

        elif method == "Doolittle LU":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            lines.append(f"\nMatrix A:\n{a}\ndet(A) = {np.linalg.det(a):.6f}")
            lines.append("→ SINGULAR. LU will fail." if abs(np.linalg.det(a)) < 1e-14 else "→ Non-singular. LU should work.")

        elif method == "Thomas":
            lower = ast.literal_eval(params["lower"])
            diag  = ast.literal_eval(params["diag"])
            upper = ast.literal_eval(params["upper"])
            rhs   = ast.literal_eval(params["rhs"])
            n = len(diag)
            lines.append(f"\nMatrix size: {n}x{n}")
            dim_ok = True
            if len(lower) != n-1: lines.append(f"ERROR: Lower should have {n-1} elems"); dim_ok = False
            if len(upper) != n-1: lines.append(f"ERROR: Upper should have {n-1} elems"); dim_ok = False
            if len(rhs)   != n:   lines.append(f"ERROR: RHS should have {n} elems");     dim_ok = False
            if dim_ok: lines.append("→ Dimensions OK.")

        elif method in {"Bisection", "False Position"}:
            expr = params["expr"]
            a_v, b_v = float(params["a"]), float(params["b"])
            fa, fb = _safe_eval(expr, a_v), _safe_eval(expr, b_v)
            lines.append(f"\nf({a_v}) = {fa:.6f}\nf({b_v}) = {fb:.6f}\nf(a)*f(b) = {fa*fb:.6f}")
            lines.append("→ Sign change: GUARANTEED." if fa*fb < 0 else "→ NO sign change: CANNOT apply!")

        elif method == "Newton-Raphson":
            x0 = float(params["x0"])
            expr   = params["expr"]
            d_expr = params["d_expr"]
            fx0  = _safe_eval(expr, x0)
            dfx0 = _safe_eval(d_expr, x0)
            lines.append(f"\nf({x0}) = {fx0:.6f}\nf'({x0}) = {dfx0:.6f}")
            h = 1e-5
            is_correct_deriv = None
            try:
                num_dfx0 = (_safe_eval(expr, x0 + h) - _safe_eval(expr, x0 - h)) / (2 * h)
                error_margin = abs(num_dfx0) * 0.05 + 0.1
                if abs(dfx0 - num_dfx0) > error_margin:
                    is_correct_deriv = False
                    lines.append(f"→ ❌ WRONG DERIVATIVE: The entered f'(x) does NOT match f(x).")
                    lines.append(f"   Expected numerical f'({x0}) ~ {num_dfx0:.6f}, but you entered {dfx0:.6f}.")
                else:
                    is_correct_deriv = True
                    lines.append(f"→ ✅ CORRECT DERIVATIVE: f'({x0}) matches numerical approximation (~{num_dfx0:.6f}).")
            except Exception:
                pass
            if abs(dfx0) < 1e-10:
                lines.append("→ ⚠️ WARNING: Derivative near zero! Will diverge.")
            elif is_correct_deriv is True:
                lines.append("→ ✅ Good starting point.")
            elif is_correct_deriv is False:
                lines.append("→ ❌ Cannot guarantee convergence with wrong derivative.")

        elif method in {"Newton Forward", "Newton Backward", "Stirling"}:
            x = np.array(ast.literal_eval(params["x"]), dtype=float)
            y = np.array(ast.literal_eval(params["y"]), dtype=float)
            eq = is_equally_spaced(x)
            lines.append(f"\nx: {x}\ny: {y}\nEqually spaced: {eq}")
            lines.append(f"→ Can apply. h = {x[1]-x[0]}" if eq else "→ NOT equally spaced! Use Lagrange.")

        elif method == "Lagrange":
            x = ast.literal_eval(params["x"])
            y = ast.literal_eval(params["y"])
            lines.append(f"\nx: {x}\ny: {y}\nPoints: {len(x)}")
            lines.append("→ OK. Any spacing works." if len(x)==len(y) else "→ ERROR: Different lengths!")

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

with st.sidebar:
    st.markdown('<div style="font-size:32px;font-weight:800;color:#00B4D8;margin-bottom:4px;">Numerical<br>Methods</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#606080;margin-bottom:24px;">Faculty of AI · Horus University</div>', unsafe_allow_html=True)

    method = st.selectbox("Method", list(METHOD_INFO.keys()), index=0)

    info = METHOD_INFO[method]
    st.markdown(f'''
    <div class="info-card">
        <div style="font-size:10px;font-weight:700;color:{info['color']};text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">{info['category']}</div>
        <div style="font-size:14px;font-weight:600;color:#F0F0FF;margin-bottom:4px;">Convergence: {info['order']}</div>
        <div style="font-size:12px;color:#9090B0;line-height:1.7;white-space:pre-line;">{info['desc']}</div>
    </div>
    ''', unsafe_allow_html=True)

    if method in LATEX_FORMULAS:
        st.markdown('<div class="info-card"><div style="font-size:10px;font-weight:700;color:#00B4D8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Formula</div></div>', unsafe_allow_html=True)
        st.latex(LATEX_FORMULAS[method])

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#606080;line-height:1.8;">Competition Mode<br>Cyber Security Department<br><br>Team:<br>' +
                "<br>".join([f"• {m}" for m in TEAM]) + '</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SPLASH SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

if "splash_done" not in st.session_state:
    st.markdown("""
    <style>
        .splash-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            min-height: 80vh; text-align: center; padding: 40px 20px;
        }
        .splash-logo {
            width: 160px; height: 160px; border-radius: 30px; background-color: #ffffff;
            display: flex; align-items: center; justify-content: center; margin-bottom: 40px;
            box-shadow: 0 25px 80px rgba(0, 180, 216, 0.4), 0 0 0 8px rgba(0,180,216,0.1);
            animation: splash-pulse 3s ease-in-out infinite; padding: 20px;
        }
        @keyframes splash-pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 25px 80px rgba(0, 180, 216, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 30px 100px rgba(0, 180, 216, 0.5); }
        }
        .splash-title { font-size: 42px; font-weight: 800; color: #F0F0FF; margin-bottom: 8px; letter-spacing: -0.03em; }
        .splash-subtitle { font-size: 18px; color: #9090B0; margin-bottom: 6px; }
        .splash-uni { font-size: 15px; color: #00B4D8; font-weight: 700; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 0.15em; }
        .splash-divider { width: 80px; height: 4px; background: linear-gradient(90deg, #00B4D8, #7B5BFF); border-radius: 2px; margin: 0 auto 35px; }
        .splash-doctor-label { font-size: 12px; color: #606080; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 10px; }
        .splash-doctor-name { font-size: 20px; font-weight: 700; color: #F0F0FF; margin-bottom: 10px; }
        .splash-team-section { margin-top: 35px; padding-top: 28px; border-top: 1px solid #252535; }
        .splash-team-label { font-size: 12px; color: #606080; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 14px; }
        .splash-team-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 600px; margin: 0 auto; }
        .splash-team-member {
            background: #1A1A24; border: 1px solid #252535; border-radius: 10px; padding: 8px 18px;
            font-size: 13px; color: #9090B0; font-weight: 500;
        }
        .splash-footer { margin-top: 50px; font-size: 12px; color: #404060; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="splash-container">
        <div class="splash-logo">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="Horus Logo" style="width: 100%; height: 100%; object-fit: contain;">
        </div>
        <div class="splash-title">Numerical Methods Calculator</div>
        <div class="splash-subtitle">Competition Edition</div>
        <div class="splash-uni">Horus University · Faculty of AI</div>
        <div class="splash-divider"></div>
        <div class="splash-doctor-label">Under Supervision of</div>
        <div class="splash-doctor-name">Dr. Eman El-Haddiy</div>
        <div class="splash-doctor-name" style="margin-top:-2px;font-size:18px;">Dr. Walaa Farouk</div>
        <div class="splash-doctor-name" style="margin-top:-2px;font-size:18px;">Dr. Mohamed Khaled</div>
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

    enter_clicked = st.button("🚀 Enter App", type="primary", key="splash_btn")
    if enter_clicked:
        st.session_state["splash_done"] = True
        st.rerun()

    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div style="font-size:30px;font-weight:800;color:#F0F0FF;margin-bottom:4px;">Advanced Numerical Calculator</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:14px;color:#9090B0;margin-bottom:28px;">Current Method: <span style="color:#00B4D8;font-weight:700;">{method}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Parameters</div>', unsafe_allow_html=True)

demo   = DEMOS[method]
params = {}

# ── Reset widget values whenever the method changes ──
_RESULT_KEYS = ("summary", "table_headers", "table_rows",
                "plot_fig", "conv_fig", "metrics", "last_error")

if st.session_state.get("_current_method") != method:
    # Write demo values directly into session_state so Streamlit picks them up
    for _k, _v in demo.items():
        st.session_state[_k] = _v
    # Clear results and errors from the old method
    for _k in _RESULT_KEYS:
        st.session_state.pop(_k, None)
    st.session_state["_current_method"] = method


if method in {"Bisection", "False Position"}:
    c1, c2, c3 = st.columns(3)
    c1.markdown("**f(x)**");  params["expr"] = c1.text_input(" ",   value=demo["expr"], key="expr", label_visibility="collapsed")
    c2.markdown("**a**");     params["a"]    = c2.text_input("  ",  value=demo["a"],    key="a",    label_visibility="collapsed")
    c3.markdown("**b**");     params["b"]    = c3.text_input("   ", value=demo["b"],    key="b",    label_visibility="collapsed")
    with st.expander("⚙️ Advanced Settings", expanded=False):
        t1, t2 = st.columns(2)
        params["tol"]      = t1.text_input("Tolerance",      value=demo["tol"],      key="tol")
        params["max_iter"] = t2.text_input("Max Iterations", value=demo["max_iter"], key="max_iter")

elif method == "Newton-Raphson":
    c1, c2, c3 = st.columns(3)
    c1.markdown("**f(x)**");   params["expr"]   = c1.text_input(" ",   value=demo["expr"],   key="expr",   label_visibility="collapsed")
    c2.markdown("**f'(x)**");  params["d_expr"] = c2.text_input("  ",  value=demo["d_expr"], key="d_expr", label_visibility="collapsed")
    c3.markdown("**x₀**");     params["x0"]     = c3.text_input("   ", value=demo["x0"],     key="x0",     label_visibility="collapsed")
    with st.expander("⚙️ Advanced Settings", expanded=False):
        t1, t2 = st.columns(2)
        params["tol"]      = t1.text_input("Tolerance",      value=demo["tol"],      key="tol")
        params["max_iter"] = t2.text_input("Max Iterations", value=demo["max_iter"], key="max_iter")

elif method == "Secant":
    c1, c2, c3 = st.columns(3)
    c1.markdown("**f(x)**"); params["expr"] = c1.text_input(" ",   value=demo["expr"], key="expr", label_visibility="collapsed")
    c2.markdown("**x₀**");   params["x0"]   = c2.text_input("  ",  value=demo["x0"],   key="x0",   label_visibility="collapsed")
    c3.markdown("**x₁**");   params["x1"]   = c3.text_input("   ", value=demo["x1"],   key="x1",   label_visibility="collapsed")
    with st.expander("⚙️ Advanced Settings", expanded=False):
        t1, t2 = st.columns(2)
        params["tol"]      = t1.text_input("Tolerance",      value=demo["tol"],      key="tol")
        params["max_iter"] = t2.text_input("Max Iterations", value=demo["max_iter"], key="max_iter")

elif method in {"Jacobi", "Gauss-Seidel", "Doolittle LU"}:
    c1, c2 = st.columns(2)
    c1.markdown("**A (matrix)**"); params["A"] = c1.text_area(" ",  value=demo["A"], key="A", label_visibility="collapsed", height=100)
    c2.markdown("**b (vector)**"); params["b"] = c2.text_area("  ", value=demo["b"], key="b", label_visibility="collapsed", height=100)
    with st.expander("⚙️ Advanced Settings", expanded=False):
        t1, t2, t3 = st.columns(3)
        params["x0"]       = t1.text_input("x₀",             value=demo["x0"],       key="x0")
        params["tol"]      = t2.text_input("Tolerance",       value=demo["tol"],      key="tol")
        params["max_iter"] = t3.text_input("Max Iterations",  value=demo["max_iter"], key="max_iter")

elif method == "Thomas":
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("**Lower**"); params["lower"] = c1.text_input(" ",    value=demo["lower"], key="lower", label_visibility="collapsed")
    c2.markdown("**Main**");  params["diag"]  = c2.text_input("  ",   value=demo["diag"],  key="diag",  label_visibility="collapsed")
    c3.markdown("**Upper**"); params["upper"] = c3.text_input("   ",  value=demo["upper"], key="upper", label_visibility="collapsed")
    c4.markdown("**RHS**");   params["rhs"]   = c4.text_input("    ", value=demo["rhs"],   key="rhs",   label_visibility="collapsed")

else:  # Interpolation methods
    c1, c2, c3 = st.columns(3)
    c1.markdown("**x values**"); params["x"]     = c1.text_input(" ",   value=demo["x"],     key="x",     label_visibility="collapsed")
    c2.markdown("**y values**"); params["y"]      = c2.text_input("  ",  value=demo["y"],     key="y",     label_visibility="collapsed")
    c3.markdown("**Target x**"); params["x_val"]  = c3.text_input("   ", value=demo["x_val"], key="x_val", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
bc1, bc2, bc3 = st.columns(3)
compute_clicked = bc1.button("⚡ Compute",           type="primary", use_container_width=True)
check_clicked   = bc2.button("🔍 Check Convergence",                 use_container_width=True)
demo_clicked    = bc3.button("🔄 Load Demo",                         use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════

if compute_clicked:
    # ── clear any previous error so a fresh success wipes the banner ──
    st.session_state.pop("last_error", None)

    try:
        sep = "=" * 50
        summary_lines = [sep, f"  {method}", f"  Category: {info['category']}", f"  Order: {info['order']}", sep]
        steps   = []
        headers = []

        if method == "Bisection":
            root, steps = bisection(params["expr"], float(params["a"]), float(params["b"]),
                                    float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
            st.session_state["plot_fig"] = plotly_root(params["expr"], root, float(params["a"]), float(params["b"]))
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "False Position":
            root, steps = false_position(params["expr"], float(params["a"]), float(params["b"]),
                                         float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "a", "b", "x", "f(x)", "Error"]
            st.session_state["plot_fig"] = plotly_root(params["expr"], root, float(params["a"]), float(params["b"]))
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Newton-Raphson":
            root, steps = newton_raphson(params["expr"], params["d_expr"], float(params["x0"]),
                                         float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_i", "f(x_i)", "f'(x_i)", "x_next", "Error"]
            st.session_state["plot_fig"] = plotly_root(params["expr"], root)
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Secant":
            root, steps = secant(params["expr"], float(params["x0"]), float(params["x1"]),
                                  float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Root = {root:.10f}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x0", "x1", "x2", "f(x2)", "Error"]
            st.session_state["plot_fig"] = plotly_root(params["expr"], root)
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Root": f"{root:.8f}", "Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Jacobi":
            a  = np.array(ast.literal_eval(params["A"]),  dtype=float)
            b  = np.array(ast.literal_eval(params["b"]),  dtype=float)
            x0 = np.array(ast.literal_eval(params["x0"]), dtype=float)
            x, steps = jacobi(a, b, x0, float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Solution x = {x}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_vector", "Error"]
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Gauss-Seidel":
            a  = np.array(ast.literal_eval(params["A"]),  dtype=float)
            b  = np.array(ast.literal_eval(params["b"]),  dtype=float)
            x0 = np.array(ast.literal_eval(params["x0"]), dtype=float)
            x, steps = gauss_seidel(a, b, x0, float(params["tol"]), int(params["max_iter"]))
            summary_lines += [f"  Solution x = {x}", f"  Iterations: {len(steps)}", f"  Final error: {steps[-1][-1]:.4e}"]
            headers = ["Iter", "x_vector", "Error"]
            st.session_state["conv_fig"] = plotly_convergence(steps, method)
            st.session_state["metrics"]  = {"Iterations": len(steps), "Final Error": f"{steps[-1][-1]:.2e}"}

        elif method == "Doolittle LU":
            a = np.array(ast.literal_eval(params["A"]), dtype=float)
            b = np.array(ast.literal_eval(params["b"]), dtype=float)
            x, l, u, steps = doolittle_lu(a, b)
            summary_lines += [f"  Solution x = {x}", f"  L:\n{l}", f"  U:\n{u}", f"  Verify A*x=b: {np.allclose(a@x, b)}"]
            headers = ["Step", "L_diag", "U_row"]
            st.session_state["metrics"] = {"Verified": "✓ A*x = b"}

        elif method == "Thomas":
            lower = ast.literal_eval(params["lower"])
            diag  = ast.literal_eval(params["diag"])
            upper = ast.literal_eval(params["upper"])
            rhs   = ast.literal_eval(params["rhs"])
            x, steps = thomas(lower, diag, upper, rhs)
            summary_lines += [f"  Solution x = {x}", f"  Forward sweep steps: {len(steps)}"]
            headers = ["Step", "w_factor", "new_b", "new_d"]
            st.session_state["metrics"] = {"Solution": np.array2string(x, precision=4)}

        elif method == "Newton Forward":
            x   = np.array(ast.literal_eval(params["x"]), dtype=float)
            y   = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv  = float(params["x_val"])
            yv, diffs = newton_forward(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plotly_interp(x, y, xv, yv)
            st.session_state["metrics"]  = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Newton Backward":
            x   = np.array(ast.literal_eval(params["x"]), dtype=float)
            y   = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv  = float(params["x_val"])
            yv, diffs = newton_backward(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plotly_interp(x, y, xv, yv)
            st.session_state["metrics"]  = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Stirling":
            x   = np.array(ast.literal_eval(params["x"]), dtype=float)
            y   = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv  = float(params["x_val"])
            yv, diffs = stirling(x, y, xv)
            mid = len(x) // 2
            p   = (xv - x[mid]) / (x[1] - x[0])
            summary_lines += [f"  f({xv}) = {yv:.10f}",
                               f"  Central point: x_{mid}={x[mid]}, y_{mid}={y[mid]}",
                               f"  p = {p:.4f}"]
            summary_lines.append(make_diff_text(diffs, x))
            st.session_state["plot_fig"] = plotly_interp(x, y, xv, yv)
            st.session_state["metrics"]  = {f"f({xv})": f"{yv:.6f}"}

        elif method == "Lagrange":
            x  = np.array(ast.literal_eval(params["x"]), dtype=float)
            y  = np.array(ast.literal_eval(params["y"]), dtype=float)
            xv = float(params["x_val"])
            yv = lagrange(x, y, xv)
            summary_lines += [f"  f({xv}) = {yv:.10f}"]
            st.session_state["plot_fig"] = plotly_interp(x, y, xv, yv)
            st.session_state["metrics"]  = {f"f({xv})": f"{yv:.6f}"}

        st.session_state["summary"]       = "\n".join(summary_lines)
        st.session_state["table_headers"] = headers
        st.session_state["table_rows"]    = steps
        st.toast("✅ Computed successfully!", icon="✅")

    except Exception as e:
        # ── Save error & clear all previous results ──
        st.session_state["last_error"] = str(e)
        st.session_state.pop("summary",        None)
        st.session_state.pop("table_headers",  None)
        st.session_state.pop("table_rows",     None)
        st.session_state.pop("plot_fig",       None)
        st.session_state.pop("conv_fig",       None)
        st.session_state.pop("metrics",        None)

elif check_clicked:
    st.session_state.pop("last_error", None)
    ok, text = run_check(method, params)
    st.session_state["summary"]       = text
    st.session_state["table_headers"] = []
    st.session_state["table_rows"]    = []
    for key in ("plot_fig", "conv_fig", "metrics"):
        st.session_state.pop(key, None)
    if ok: st.toast("✅ Check completed!", icon="✅")
    else:  st.error("Check found issues!")

elif demo_clicked:
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS SECTION
# ═══════════════════════════════════════════════════════════════════════════════

# ── Show error banner (if any) ABOVE the old results ──
if st.session_state.get("last_error"):
    st.markdown(f"""
    <div class="error-banner">
        <div class="error-banner-title">⛔ Computation Error</div>
        <div class="error-banner-msg">{st.session_state["last_error"]}</div>
        <div class="error-banner-hint">
            ↑ Fix your inputs and press Compute again.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Previous / current results ──
if st.session_state.get("summary"):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    if st.session_state.get("metrics"):
        mc = st.columns(len(st.session_state["metrics"]))
        for i, (k, v) in enumerate(st.session_state["metrics"].items()):
            mc[i].metric(k, v)

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Iterations", "Interactive Plot", "Convergence"])

    with tab1:
        st.markdown(f'<div class="result-box">{st.session_state["summary"]}</div>', unsafe_allow_html=True)

    with tab2:
        if st.session_state.get("table_headers"):
            headers = st.session_state["table_headers"]
            rows    = st.session_state["table_rows"]

            def fmt(v):
                if isinstance(v, float):      return f"{v:.8f}"
                if isinstance(v, np.ndarray): return np.array2string(v, precision=6)
                return str(v)

            data = [[fmt(v) for v in row] for row in rows]
            st.dataframe(pd.DataFrame(data, columns=headers),
                         use_container_width=True, hide_index=True, height=400)
        else:
            st.info("No iteration data for this method.")

    with tab3:
        if st.session_state.get("plot_fig"):
            st.plotly_chart(st.session_state["plot_fig"], use_container_width=True)
        else:
            st.info("No plot for this method.")

    with tab4:
        if st.session_state.get("conv_fig"):
            st.plotly_chart(st.session_state["conv_fig"], use_container_width=True)
        else:
            st.info("No convergence plot for this method.")
