# -*- coding: utf-8 -*-
"""
Simulador Didático da Esfera de Bloch
-------------------------------------
Aplicativo em arquivo único para estudar estados puros de um qubit.

Controles didáticos:
1) Ângulos de Bloch: theta, phi e fase global gamma.
2) Probabilidades: P(0), P(1) e fase relativa.
3) Amplitudes: |a|, arg(a), arg(b), mantendo |a|²+|b|²=1.
4) Portas quânticas: X, Y, Z, H, S, T e rotações Rx, Ry, Rz.
5) Resultados simultâneos: vetor de estado, probabilidades, coordenadas de Bloch,
   valores esperados <X>, <Y>, <Z> e probabilidades de medida nas bases X/Y/Z.
6) Trecho Qiskit equivalente ao estado atual.

Observação didática:
- |psi> é o ESTADO, não um ângulo.
- Para um qubit puro, bastam dois parâmetros fisicamente observáveis (theta, phi).
- gamma é uma fase global e não muda a posição na esfera de Bloch.
- Não existe um terceiro coeficiente c para um qubit. Três amplitudes independentes
  corresponderiam a um sistema de três níveis (qutrit), não a um qubit.
"""

from __future__ import annotations

import importlib.util
import math
import os
import subprocess
import sys
import textwrap

APP_TITLE = "Simulador Didático da Esfera de Bloch"


def _show_missing_tkinter_message() -> None:
    msg = (
        "O Python foi encontrado, mas o módulo Tkinter não está disponível.\n\n"
        "Windows/macOS:\n"
        "  reinstale o Python pelo instalador oficial e inclua Tcl/Tk.\n\n"
        "Ubuntu/Debian:\n"
        "  sudo apt install python3-tk\n\n"
        "Fedora:\n"
        "  sudo dnf install python3-tkinter\n"
    )
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, msg, APP_TITLE, 0x10)
            return
        except Exception:
            pass
    print(msg)
    try:
        input("\nPressione Enter para fechar...")
    except Exception:
        pass


try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except Exception:
    _show_missing_tkinter_message()
    raise SystemExit(1)


REQUIRED_MODULES = {
    "numpy": "numpy",
    "matplotlib": "matplotlib",
}


def check_and_offer_dependencies() -> None:
    missing = [
        package
        for module, package in REQUIRED_MODULES.items()
        if importlib.util.find_spec(module) is None
    ]

    if not missing:
        return

    root = tk.Tk()
    root.title("Dependências ausentes")
    root.geometry("620x360")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Algumas bibliotecas necessárias não estão instaladas.",
        font=("TkDefaultFont", 12, "bold"),
    ).pack(anchor="w", pady=(0, 12))

    ttk.Label(frame, text="Faltando: " + ", ".join(missing)).pack(anchor="w", pady=(0, 10))

    command = f'"{sys.executable}" -m pip install ' + " ".join(missing)

    ttk.Label(
        frame,
        text=(
            "Você pode instalar pelo terminal com o comando abaixo "
            "ou clicar em “Instalar agora”."
        ),
        wraplength=560,
        justify="left",
    ).pack(anchor="w", pady=(0, 8))

    cmd_box = tk.Text(frame, height=3, wrap="word")
    cmd_box.pack(fill="x", pady=(0, 14))
    cmd_box.insert("1.0", command)
    cmd_box.configure(state="disabled")

    status = ttk.Label(frame, text="")
    status.pack(anchor="w", pady=(0, 10))

    def install_now():
        status.configure(text="Instalando... aguarde.")
        root.update_idletasks()
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
        except Exception as exc:
            messagebox.showerror(
                "Falha na instalação",
                "Não foi possível instalar automaticamente.\n\n"
                f"Execute manualmente:\n{command}\n\n"
                f"Detalhe técnico:\n{exc}",
            )
            status.configure(text="Instalação não concluída.")
            return

        messagebox.showinfo(
            "Instalação concluída",
            "As bibliotecas foram instaladas. O aplicativo será reiniciado.",
        )
        root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    buttons = ttk.Frame(frame)
    buttons.pack(fill="x", pady=(5, 0))
    ttk.Button(buttons, text="Instalar agora", command=install_now).pack(side="left")
    ttk.Button(buttons, text="Fechar", command=root.destroy).pack(side="right")

    root.mainloop()
    raise SystemExit(0)


check_and_offer_dependencies()

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

EPS = 1e-12


def wrap_angle(angle: float) -> float:
    value = (angle + math.pi) % (2 * math.pi) - math.pi
    if value <= -math.pi + 1e-12:
        return math.pi
    return value


def normalize_state(state: np.ndarray) -> np.ndarray:
    state = np.asarray(state, dtype=complex).reshape(2)
    norm = np.linalg.norm(state)
    if norm < EPS:
        return np.array([1.0 + 0j, 0.0 + 0j])
    return state / norm


def state_from_bloch(theta: float, phi: float, gamma: float = 0.0) -> np.ndarray:
    return np.exp(1j * gamma) * np.array(
        [
            np.cos(theta / 2),
            np.exp(1j * phi) * np.sin(theta / 2),
        ],
        dtype=complex,
    )


def state_to_parameters(state: np.ndarray):
    state = normalize_state(state)
    a, b = state
    p0 = float(abs(a) ** 2)
    p1 = float(abs(b) ** 2)
    theta = 2 * math.atan2(abs(b), abs(a))

    if abs(a) > EPS:
        gamma = float(np.angle(a))
        phi = float(np.angle(b) - gamma) if abs(b) > EPS else 0.0
    else:
        gamma = float(np.angle(b)) if abs(b) > EPS else 0.0
        phi = 0.0

    gamma = wrap_angle(gamma)
    phi = wrap_angle(phi)

    x = float(2 * np.real(np.conjugate(a) * b))
    y = float(2 * np.imag(np.conjugate(a) * b))
    z = float(p0 - p1)

    return theta, phi, gamma, p0, p1, x, y, z


def format_complex(z: complex, digits: int = 4) -> str:
    r = 0.0 if abs(z.real) < 10 ** (-(digits + 1)) else z.real
    i = 0.0 if abs(z.imag) < 10 ** (-(digits + 1)) else z.imag
    if abs(i) < EPS:
        return f"{r:.{digits}f}"
    sign = "+" if i >= 0 else "-"
    return f"{r:.{digits}f} {sign} {abs(i):.{digits}f}i"


X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)


def rx(alpha: float) -> np.ndarray:
    c = np.cos(alpha / 2)
    s = np.sin(alpha / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def ry(alpha: float) -> np.ndarray:
    c = np.cos(alpha / 2)
    s = np.sin(alpha / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(alpha: float) -> np.ndarray:
    return np.array(
        [[np.exp(-1j * alpha / 2), 0], [0, np.exp(1j * alpha / 2)]],
        dtype=complex,
    )


class BlochApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1510x900")
        self.minsize(1260, 780)
        self._updating = False
        self.state = np.array([1.0 + 0j, 0.0 + 0j])
        self._configure_style()
        self._build_layout()
        self._build_plot()
        self.set_state(self.state)

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            if "vista" in style.theme_names():
                style.theme_use("vista")
            elif "clam" in style.theme_names():
                style.theme_use("clam")
        except Exception:
            pass
        style.configure("Title.TLabel", font=("TkDefaultFont", 15, "bold"))

    def _build_layout(self):
        outer = ttk.Frame(self, padding=8)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=0)
        outer.columnconfigure(1, weight=1)
        outer.columnconfigure(2, weight=0)
        outer.rowconfigure(0, weight=1)

        self.left = ttk.Frame(outer, width=390)
        self.left.grid(row=0, column=0, sticky="nsw", padx=(0, 8))

        self.center = ttk.Frame(outer)
        self.center.grid(row=0, column=1, sticky="nsew", padx=4)
        self.center.rowconfigure(0, weight=1)
        self.center.columnconfigure(0, weight=1)

        self.right = ttk.Frame(outer, width=400)
        self.right.grid(row=0, column=2, sticky="nse", padx=(8, 0))

        self._build_controls()
        self._build_results()

    def _build_controls(self):
        ttk.Label(self.left, text="Controles do estado", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            self.left,
            text=(
                "Um qubit puro tem dois parâmetros físicos independentes: θ e φ. "
                "A fase global γ é mostrada porque é matematicamente útil, mas não move o ponto na esfera."
            ),
            wraplength=370,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        info = ttk.LabelFrame(self.left, text="Nota didática", padding=8)
        info.pack(fill="x", pady=(0, 10))
        ttk.Label(
            info,
            text=(
                "• |ψ⟩ é o estado, não um ângulo.\n"
                "• a e b são amplitudes complexas.\n"
                "• P(0)=|a|² e P(1)=|b|².\n"
                "• Não usamos c: três amplitudes descrevem um qutrit, não um qubit."
            ),
            wraplength=350,
            justify="left",
        ).pack(anchor="w")

        self.notebook = ttk.Notebook(self.left)
        self.notebook.pack(fill="x", pady=(0, 10))

        self.tab_angles = ttk.Frame(self.notebook, padding=10)
        self.tab_probs = ttk.Frame(self.notebook, padding=10)
        self.tab_amp = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_angles, text="θ, φ, γ")
        self.notebook.add(self.tab_probs, text="Probabilidades")
        self.notebook.add(self.tab_amp, text="Amplitudes")

        self.theta_var = tk.DoubleVar(value=0.0)
        self.phi_var = tk.DoubleVar(value=0.0)
        self.gamma_var = tk.DoubleVar(value=0.0)

        self._make_slider(self.tab_angles, "θ — ângulo polar", self.theta_var, 0.0, math.pi, self._on_angles)
        self._make_slider(self.tab_angles, "φ — fase relativa / azimute", self.phi_var, -math.pi, math.pi, self._on_angles)
        self._make_slider(self.tab_angles, "γ — fase global", self.gamma_var, -math.pi, math.pi, self._on_angles)

        self.p0_var = tk.DoubleVar(value=1.0)
        self.prob_phi_var = tk.DoubleVar(value=0.0)
        self._make_slider(self.tab_probs, "P(0)", self.p0_var, 0.0, 1.0, self._on_probabilities)
        self.p1_label = ttk.Label(self.tab_probs, text="P(1) = 0.000")
        self.p1_label.pack(anchor="w", pady=(0, 8))
        self._make_slider(self.tab_probs, "fase relativa φ", self.prob_phi_var, -math.pi, math.pi, self._on_probabilities)
        ttk.Label(
            self.tab_probs,
            text=(
                "A probabilidade sozinha não determina um qubit: estados com as mesmas "
                "P(0), P(1) podem ter fases relativas diferentes."
            ),
            wraplength=340,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        self.a_mag_var = tk.DoubleVar(value=1.0)
        self.a_phase_var = tk.DoubleVar(value=0.0)
        self.b_phase_var = tk.DoubleVar(value=0.0)
        self._make_slider(self.tab_amp, "|a|", self.a_mag_var, 0.0, 1.0, self._on_amplitudes)
        self.b_mag_label = ttk.Label(self.tab_amp, text="|b| = 0.000")
        self.b_mag_label.pack(anchor="w", pady=(0, 8))
        self._make_slider(self.tab_amp, "arg(a)", self.a_phase_var, -math.pi, math.pi, self._on_amplitudes)
        self._make_slider(self.tab_amp, "arg(b)", self.b_phase_var, -math.pi, math.pi, self._on_amplitudes)
        ttk.Label(
            self.tab_amp,
            text="|b| é calculado automaticamente por |a|²+|b|²=1, garantindo sempre um estado válido.",
            wraplength=340,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        presets = ttk.LabelFrame(self.left, text="Estados notáveis", padding=8)
        presets.pack(fill="x", pady=(0, 10))
        preset_buttons = [
            ("|0⟩", np.array([1, 0], complex)),
            ("|1⟩", np.array([0, 1], complex)),
            ("|+⟩", np.array([1, 1], complex) / np.sqrt(2)),
            ("|−⟩", np.array([1, -1], complex) / np.sqrt(2)),
            ("|+i⟩", np.array([1, 1j], complex) / np.sqrt(2)),
            ("|−i⟩", np.array([1, -1j], complex) / np.sqrt(2)),
        ]
        for idx, (name, state) in enumerate(preset_buttons):
            ttk.Button(presets, text=name, command=lambda s=state: self.set_state(s), width=8).grid(
                row=idx // 3, column=idx % 3, padx=3, pady=3, sticky="ew"
            )
        for i in range(3):
            presets.columnconfigure(i, weight=1)

        gates = ttk.LabelFrame(self.left, text="Aplicar portas ao estado atual", padding=8)
        gates.pack(fill="x", pady=(0, 10))
        fixed_gates = [("X", X), ("Y", Y), ("Z", Z), ("H", H), ("S", S), ("T", T)]
        for idx, (name, matrix) in enumerate(fixed_gates):
            ttk.Button(
                gates,
                text=name,
                command=lambda m=matrix, n=name: self.apply_gate(m, n),
                width=7,
            ).grid(row=idx // 3, column=idx % 3, padx=3, pady=3, sticky="ew")
        for i in range(3):
            gates.columnconfigure(i, weight=1)

        self.gate_angle_var = tk.DoubleVar(value=math.pi / 4)
        self._make_slider(
            gates,
            "α — ângulo das rotações",
            self.gate_angle_var,
            -math.pi,
            math.pi,
            lambda *_: None,
            row_mode=True,
            row=2,
            columnspan=3,
        )

        rotation_row = ttk.Frame(gates)
        rotation_row.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(4, 0))
        for label, fn in [("Rx(α)", rx), ("Ry(α)", ry), ("Rz(α)", rz)]:
            ttk.Button(
                rotation_row,
                text=label,
                command=lambda f=fn, n=label: self.apply_gate(f(self.gate_angle_var.get()), n),
            ).pack(side="left", fill="x", expand=True, padx=2)

        actions = ttk.Frame(self.left)
        actions.pack(fill="x")
        ttk.Button(
            actions,
            text="Reiniciar em |0⟩",
            command=lambda: self.set_state(np.array([1, 0], complex)),
        ).pack(side="left", fill="x", expand=True, padx=(0, 3))
        ttk.Button(actions, text="Sobre", command=self._show_about).pack(
            side="left", fill="x", expand=True, padx=(3, 0)
        )

    def _make_slider(self, parent, label, variable, vmin, vmax, command, row_mode=False, row=0, columnspan=1):
        container = ttk.Frame(parent)
        if row_mode:
            container.grid(row=row, column=0, columnspan=columnspan, sticky="ew", pady=(8, 2))
        else:
            container.pack(fill="x", pady=(0, 8))

        top = ttk.Frame(container)
        top.pack(fill="x")
        ttk.Label(top, text=label).pack(side="left")
        value_label = ttk.Label(top, text=f"{variable.get():.3f}", width=9, anchor="e")
        value_label.pack(side="right")

        scale = ttk.Scale(container, from_=vmin, to=vmax, orient="horizontal", variable=variable)
        scale.pack(fill="x", pady=(3, 0))

        def callback(value):
            value_label.configure(text=f"{float(value):.3f}")
            command(value)

        scale.configure(command=callback)
        return scale

    def _build_results(self):
        ttk.Label(self.right, text="Resultados simultâneos", style="Title.TLabel").pack(anchor="w", pady=(0, 6))
        self.result_text = tk.Text(self.right, width=52, height=24, wrap="word", font=("Consolas", 10))
        self.result_text.pack(fill="x", pady=(0, 10))
        self.result_text.configure(state="disabled")

        code_frame = ttk.LabelFrame(self.right, text="Circuito Qiskit equivalente", padding=8)
        code_frame.pack(fill="both", expand=True)
        ttk.Label(
            code_frame,
            text=(
                "O código abaixo prepara o mesmo estado. Rz(φ)Ry(θ)|0⟩ é equivalente até fase global; "
                "global_phase torna a igualdade exata."
            ),
            wraplength=380,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))
        self.qiskit_text = tk.Text(code_frame, width=52, height=12, wrap="none", font=("Consolas", 9))
        self.qiskit_text.pack(fill="both", expand=True)
        self.qiskit_text.configure(state="disabled")

    def _build_plot(self):
        self.figure = Figure(figsize=(7.2, 7.2), dpi=100)
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.center)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.ax.set_title("Esfera de Bloch — estado puro")

        u = np.linspace(0, 2 * np.pi, 48)
        v = np.linspace(0, np.pi, 26)
        xs = np.outer(np.cos(u), np.sin(v))
        ys = np.outer(np.sin(u), np.sin(v))
        zs = np.outer(np.ones_like(u), np.cos(v))
        self.ax.plot_wireframe(xs, ys, zs, rstride=3, cstride=3, linewidth=0.45, alpha=0.2)

        t = np.linspace(0, 2 * np.pi, 250)
        self.ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), linewidth=0.8, alpha=0.5)
        self.ax.plot(np.cos(t), np.zeros_like(t), np.sin(t), linewidth=0.8, alpha=0.5)
        self.ax.plot(np.zeros_like(t), np.cos(t), np.sin(t), linewidth=0.8, alpha=0.5)

        self.ax.plot([-1.15, 1.15], [0, 0], [0, 0], linewidth=0.8)
        self.ax.plot([0, 0], [-1.15, 1.15], [0, 0], linewidth=0.8)
        self.ax.plot([0, 0], [0, 0], [-1.15, 1.15], linewidth=0.8)

        self.ax.text(1.23, 0, 0, "+x  |+⟩")
        self.ax.text(-1.33, 0, 0, "−x  |−⟩")
        self.ax.text(0, 1.24, 0, "+y  |+i⟩")
        self.ax.text(0, -1.38, 0, "−y  |−i⟩")
        self.ax.text(0, 0, 1.24, "+z  |0⟩")
        self.ax.text(0, 0, -1.34, "−z  |1⟩")

        (self.vector_line,) = self.ax.plot([0, 0], [0, 0], [0, 1], linewidth=3.0)
        (self.vector_point,) = self.ax.plot([0], [0], [1], marker="o", markersize=8)

        self.ax.set_xlim(-1.35, 1.35)
        self.ax.set_ylim(-1.35, 1.35)
        self.ax.set_zlim(-1.35, 1.35)
        self.ax.set_box_aspect((1, 1, 1))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.view_init(elev=22, azim=38)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _on_angles(self, *_):
        if self._updating:
            return
        self.set_state(
            state_from_bloch(self.theta_var.get(), self.phi_var.get(), self.gamma_var.get())
        )

    def _on_probabilities(self, *_):
        if self._updating:
            return
        p0 = min(1.0, max(0.0, self.p0_var.get()))
        theta = 2 * math.acos(math.sqrt(p0))
        phi = self.prob_phi_var.get()
        gamma = state_to_parameters(self.state)[2]
        self.set_state(state_from_bloch(theta, phi, gamma))

    def _on_amplitudes(self, *_):
        if self._updating:
            return
        a_mag = min(1.0, max(0.0, self.a_mag_var.get()))
        b_mag = math.sqrt(max(0.0, 1.0 - a_mag ** 2))
        a = a_mag * np.exp(1j * self.a_phase_var.get())
        b = b_mag * np.exp(1j * self.b_phase_var.get())
        self.set_state(np.array([a, b]))

    def set_state(self, state):
        self.state = normalize_state(state)
        theta, phi, gamma, p0, p1, x, y, z = state_to_parameters(self.state)

        self._updating = True
        try:
            self.theta_var.set(theta)
            self.phi_var.set(phi)
            self.gamma_var.set(gamma)
            self.p0_var.set(p0)
            self.prob_phi_var.set(phi)
            self.p1_label.configure(text=f"P(1) = {p1:.3f}")

            a, b = self.state
            self.a_mag_var.set(abs(a))
            self.a_phase_var.set(wrap_angle(float(np.angle(a))) if abs(a) > EPS else 0.0)
            self.b_phase_var.set(wrap_angle(float(np.angle(b))) if abs(b) > EPS else 0.0)
            self.b_mag_label.configure(text=f"|b| = {abs(b):.3f}")
        finally:
            self._updating = False

        self._update_plot(x, y, z)
        self._update_results(theta, phi, gamma, p0, p1, x, y, z)
        self._update_qiskit_code(theta, phi, gamma)

    def apply_gate(self, matrix: np.ndarray, name: str = ""):
        self.set_state(matrix @ self.state)
        if name:
            self.ax.set_title(f"Esfera de Bloch — após {name}")
            self.canvas.draw_idle()

    def _update_plot(self, x, y, z):
        self.vector_line.set_data_3d([0, x], [0, y], [0, z])
        self.vector_point.set_data_3d([x], [y], [z])
        self.canvas.draw_idle()

    def _update_results(self, theta, phi, gamma, p0, p1, x, y, z):
        a, b = self.state
        px_plus, px_minus = (1 + x) / 2, (1 - x) / 2
        py_plus, py_minus = (1 + y) / 2, (1 - y) / 2
        radius = math.sqrt(x*x + y*y + z*z)

        content = f"""
ESTADO ATUAL

|ψ⟩ = a|0⟩ + b|1⟩

a = {format_complex(a)}
b = {format_complex(b)}

Normalização:
|a|² + |b|² = {abs(a)**2:.6f} + {abs(b)**2:.6f}
             = {abs(a)**2 + abs(b)**2:.6f}

PROBABILIDADES NA BASE Z

P(0) = |a|² = {p0:.6f}
P(1) = |b|² = {p1:.6f}

ÂNGULOS

θ = {theta:.6f} rad = {math.degrees(theta):.2f}°
φ = {phi:.6f} rad = {math.degrees(phi):.2f}°
γ = {gamma:.6f} rad = {math.degrees(gamma):.2f}°

γ é fase global: alterá-la não move o ponto na esfera.

VETOR DE BLOCH

x = 2 Re(a* b) = {x:.6f}
y = 2 Im(a* b) = {y:.6f}
z = |a|²-|b|² = {z:.6f}

r = sqrt(x²+y²+z²) = {radius:.6f}

Para um estado puro ideal, r = 1.

VALORES ESPERADOS

⟨X⟩ = {x:.6f}
⟨Y⟩ = {y:.6f}
⟨Z⟩ = {z:.6f}

MEDIÇÕES EM OUTRAS BASES

Base X:
P(+x) = {px_plus:.6f}
P(−x) = {px_minus:.6f}

Base Y:
P(+y) = {py_plus:.6f}
P(−y) = {py_minus:.6f}

Base Z:
P(0) = {p0:.6f}
P(1) = {p1:.6f}
""".strip()

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", content)
        self.result_text.configure(state="disabled")

    def _update_qiskit_code(self, theta, phi, gamma):
        code = f"""from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

theta = {theta:.12f}
phi   = {phi:.12f}
gamma = {gamma:.12f}

qc = QuantumCircuit(1)
qc.ry(theta, 0)
qc.rz(phi, 0)

# Ajusta a fase global para reproduzir
# exatamente a mesma representação vetorial:
qc.global_phase = gamma + phi/2

psi = Statevector(qc)

print(psi)
print(psi.probabilities_dict())
"""
        self.qiskit_text.configure(state="normal")
        self.qiskit_text.delete("1.0", "end")
        self.qiskit_text.insert("1.0", code)
        self.qiskit_text.configure(state="disabled")

    def _show_about(self):
        messagebox.showinfo(
            "Sobre o simulador",
            textwrap.dedent(
                """
                Simulador Didático da Esfera de Bloch

                Objetivo:
                relacionar simultaneamente quatro representações de um qubit puro:

                1. |ψ⟩ = a|0⟩ + b|1⟩
                2. probabilidades P(0) e P(1)
                3. ângulos θ e φ
                4. vetor de Bloch (x,y,z)

                Escolhas didáticas:
                • γ é mostrado separadamente porque a fase global não é observável.
                • P(0) sozinho não define o estado; φ também é necessário.
                • a e b são amplitudes, não probabilidades.
                • não há coeficiente c em um qubit de dois níveis.
                • o programa representa estados puros; estados mistos ocupariam o interior
                  da esfera e exigiriam uma matriz densidade.

                As portas são aplicadas diretamente ao vetor de estado e a esfera é
                atualizada em tempo real.
                """
            ).strip(),
        )


def main():
    app = BlochApp()
    app.mainloop()


if __name__ == "__main__":
    main()
