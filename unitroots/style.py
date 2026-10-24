"""Figure style shared by every figure of this repository.

The style is the one used for the charts on muhammedikbalyilmaz.com: Latin Modern Roman, no grid, no top or right
spine, ticks pointing outwards, series in black and deep blue (red marks dates and reference values), labels at
the end of the lines where a legend would cover data, panel titles in bold at the left.

Axis rule (checked when a figure is saved): every value axis starts and ends at a labelled major tick, so that the
axis line never runs past its last tick, and no axis has minor ticks. Value axes are set with `value_axis` (linear)
or `log_axis` (logarithmic); `save_figure` refuses to write a figure in which an axis of a panel was not set this
way, in which a limit is not a tick, in which minor ticks are drawn, or in which two pieces of text overlap.

Every figure is saved as PDF (used by the project note) and as PNG with a heading (used by the README).

Author: Muhammed Ikbal Yilmaz
"""

import logging
import math
import os
import sys
from pathlib import Path

import matplotlib

if "ipykernel" not in sys.modules:   # scripts and tests draw to files; inside Jupyter the notebook's backend is kept
    matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager, ticker  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FONT_DIR = ROOT / "fonts"

INK, MUTED, BAND = "#000000", "#7a7a7a", "#c9d4ec"
BLUE, RED = "#0033a0", "#d7191c"     # BLUE is the deep blue of the site; RED marks dates and reference values

# Up to six series in one panel: colour, line style and marker together tell them apart, so that no series is
# identified by colour alone. Red is kept for dates and reference values.
SERIES = [(INK, "-", "o"), (BLUE, "-", "s"), (MUTED, "-", "D"), (INK, "--", "^"), (BLUE, "--", "v"), (MUTED, "--", "P")]

_EPS = 1e-9


def num(value, fmt="{:g}"):
    """Format a number for a tick label, with a typographic minus sign."""
    return fmt.format(value).replace("-", "−")


def use_style():
    logging.getLogger("fontTools").setLevel(logging.ERROR)   # silences font-subsetting notices
    for path in list(FONT_DIR.glob("*.otf")) + list(FONT_DIR.glob("*.ttf")):
        font_manager.fontManager.addfont(str(path))
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Latin Modern Roman", "DejaVu Serif"], "mathtext.fontset": "cm",
        "font.size": 7.5, "axes.labelsize": 7.5, "axes.titlesize": 8, "axes.titlelocation": "left",
        "axes.titleweight": "bold", "axes.edgecolor": INK, "axes.linewidth": 0.7, "axes.labelcolor": INK,
        "text.color": INK, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
        "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "xtick.major.width": 0.7, "ytick.major.width": 0.7, "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.direction": "out", "ytick.direction": "out", "xtick.minor.visible": False,
        "ytick.minor.visible": False, "lines.linewidth": 1.4, "lines.solid_capstyle": "butt",
        "legend.frameon": False, "legend.fontsize": 7.5, "legend.handlelength": 1.8,
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 3,
        # Latin Modern is a CFF font; Type 3 embedding keeps every PDF viewer happy
    })


def _register(ax, which, free=False):
    key = "_free_axes" if free else "_value_axes"
    ax.figure.__dict__.setdefault(key, set()).add((id(ax), which))


def value_axis(ax, which, lo, hi, step, fmt="{:g}"):
    """Linear value axis from `lo` to `hi` with a labelled tick every `step`, both ends included."""
    n = (hi - lo) / step
    if abs(n - round(n)) > 1e-6:
        raise ValueError(f"({hi} - {lo}) is not a multiple of {step}")
    ticks = [lo + i * step for i in range(int(round(n)) + 1)]
    axis = ax.yaxis if which == "y" else ax.xaxis
    (ax.set_ylim if which == "y" else ax.set_xlim)(lo, hi)
    axis.set_ticks(ticks)
    axis.set_minor_locator(ticker.NullLocator())
    axis.set_major_formatter(ticker.FuncFormatter(lambda v, _: num(round(v, 10), fmt)))
    _register(ax, which)
    return ticks


def log_axis(ax, which, lo, hi, every=1):
    """Logarithmic value axis from `lo` to `hi` (powers of ten), labelled 10^k every `every` decades."""
    a, b = math.log10(lo), math.log10(hi)
    if abs(a - round(a)) > 1e-9 or abs(b - round(b)) > 1e-9 or (round(b) - round(a)) % every:
        raise ValueError(f"log axis {lo}..{hi} must run between powers of ten, a multiple of {every} decades apart")
    ticks = [10.0 ** k for k in range(round(a), round(b) + 1, every)]
    axis = ax.yaxis if which == "y" else ax.xaxis
    (ax.set_yscale if which == "y" else ax.set_xscale)("log")
    (ax.set_ylim if which == "y" else ax.set_xlim)(lo, hi)
    axis.set_ticks(ticks)
    axis.set_minor_locator(ticker.NullLocator())
    axis.set_major_formatter(ticker.LogFormatterMathtext())
    _register(ax, which)
    return ticks


def fit_axis(ax, which, values, step, fmt="{:g}"):
    """Linear value axis running from the multiple of `step` at or below the smallest value to the multiple at or
    above the largest one."""
    import numpy as np
    v = np.asarray(values, dtype=float).ravel()
    v = v[np.isfinite(v)]
    lo = round(math.floor(v.min() / step + 1e-9) * step, 10)
    hi = round(math.ceil(v.max() / step - 1e-9) * step, 10)
    if hi == lo:
        hi = lo + step
    return value_axis(ax, which, lo, hi, step, fmt)


def nice_limits(lo, hi, intervals=(2, 6)):
    """Limits and step for the data range [lo, hi]: the step is 1, 2, 2.5 or 5 times a power of ten, the axis has
    between intervals[0] and intervals[1] intervals, and the space left empty beyond the data is the smallest."""
    span = hi - lo if hi > lo else (abs(hi) or 1.0)
    best = None
    k0 = math.floor(math.log10(span / intervals[1])) - 1
    for k in range(k0, k0 + 4):
        for m in (1, 2, 2.5, 5):
            step = m * 10.0 ** k
            a = math.floor(lo / step + 1e-9) * step
            b = math.ceil(hi / step - 1e-9) * step
            if b <= a:
                b = a + step
            n = round((b - a) / step)
            if not intervals[0] <= n <= intervals[1]:
                continue
            key = (round((b - a) / span, 9), abs(n - 4))
            if best is None or key < best[0]:
                best = (key, round(a, 10), round(b, 10), step)
    if best is None:
        raise ValueError(f"no step for [{lo}, {hi}]")
    return best[1], best[2], best[3]


def auto_axis(ax, which, values, intervals=(2, 6), fmt="{:g}"):
    """Linear value axis over the data in `values`, with limits and step from `nice_limits`."""
    import numpy as np
    v = np.asarray(values, dtype=float).ravel()
    v = v[np.isfinite(v)]
    lo, hi, step = nice_limits(float(v.min()), float(v.max()), intervals)
    return value_axis(ax, which, lo, hi, step, fmt)


def fit_log_axis(ax, which, values, every=1):
    """Logarithmic value axis from the power of ten at or below the smallest positive value to the one at or
    above the largest."""
    import numpy as np
    v = np.asarray(values, dtype=float).ravel()
    v = v[np.isfinite(v) & (v > 0)]
    a = math.floor(math.log10(v.min()) + 1e-9)
    b = math.ceil(math.log10(v.max()) - 1e-9)
    b = max(b, a + every)
    b = a + every * math.ceil((b - a) / every)
    return log_axis(ax, which, 10.0 ** a, 10.0 ** b, every)


def tick_axis(ax, which, ticks, log=False, fmt="{:,.0f}"):
    """Value axis with the given ticks (for example 1,000, 2,000, 3,000, 5,000 and 10,000 on a log scale); the limits
    are the first and the last tick."""
    axis = ax.yaxis if which == "y" else ax.xaxis
    if log:
        (ax.set_yscale if which == "y" else ax.set_xscale)("log")
    (ax.set_ylim if which == "y" else ax.set_xlim)(ticks[0], ticks[-1])
    axis.set_ticks(list(ticks))
    axis.set_minor_locator(ticker.NullLocator())
    axis.set_major_formatter(ticker.FuncFormatter(lambda v, _: num(v, fmt)))
    _register(ax, which)
    return list(ticks)


def free_axis(ax, which):
    """Mark an axis that is not a value axis (dates, categories, lags, an axis without ticks). It keeps its own
    ticks; only the minor-tick and overlap checks apply."""
    axis = ax.yaxis if which == "y" else ax.xaxis
    axis.set_minor_locator(ticker.NullLocator())
    _register(ax, which, free=True)


def event_line(ax, x, label, y=0.98, ha="left"):
    """Red dotted vertical line with a bold red label at the top of the panel."""
    ax.axvline(x, color=RED, ls=(0, (1, 1.4)), lw=1.4, zorder=1)
    ax.annotate(label, xy=(x, y), xycoords=("data", "axes fraction"), xytext=(3 if ha == "left" else -3, 0),
                textcoords="offset points", ha=ha, va="top", color=RED, fontweight="bold", fontsize=7.5)


def end_label(ax, x, y, text, color, dx=4, dy=0, va="center"):
    """Label written at the end of a line, in the colour of the line."""
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", color=color, fontweight="bold",
                fontsize=7.5, va=va, ha="left", annotation_clip=False)


def source_note(ax, text, x=0.03, y=0.03, ha="left", va="bottom"):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=6.6, ha=ha, va=va, color=INK)


def panel_name(ax, text, x=0.97, y=0.06):
    """Large bold name inside a small-multiple panel."""
    ax.text(x, y, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, fontweight="bold")


# ---------------------------------------------------------------------------------------------- checks
def _axis_problems(ax, which):
    """Limits that are not labelled ticks."""
    axis = ax.yaxis if which == "y" else ax.xaxis
    lo, hi = sorted(ax.get_ylim() if which == "y" else ax.get_xlim())
    log = (ax.get_yscale() if which == "y" else ax.get_xscale()) == "log"
    f = (lambda v: math.log10(v)) if log else (lambda v: v)
    span = abs(f(hi) - f(lo)) or 1.0
    ticks = [t for t in axis.get_majorticklocs() if (t > 0 or not log)
             and f(lo) - _EPS * span <= f(t) <= f(hi) + _EPS * span]
    if not ticks:
        return ["no major ticks"]
    out = []
    if abs(f(ticks[0]) - f(lo)) > 1e-7 * span:
        out.append(f"lower limit {lo:g} is not a tick")
    if abs(f(ticks[-1]) - f(hi)) > 1e-7 * span:
        out.append(f"upper limit {hi:g} is not a tick")
    return out


def _texts(fig, renderer):
    """Every piece of text that is drawn: tick labels only for the ticks inside the view."""
    ticklabels, drawn = set(), []
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                ticklabels.update({id(tick.label1), id(tick.label2)})
            if ax.get_visible() and ax.axison and axis.get_visible():
                for tick in axis._update_ticks():
                    drawn += [lab for lab in (tick.label1, tick.label2) if lab.get_visible()]
    texts = [t for t in fig.findobj(matplotlib.text.Text) if id(t) not in ticklabels] + drawn
    out = []
    for t in texts:
        if t.get_visible() and t.get_text().strip() and t.figure is fig:
            bb = t.get_window_extent(renderer)
            if bb.width > 0 and bb.height > 0:
                out.append((t, bb))
    return out


def _is_free_text(t):
    """Annotations, legends and plain text inside a panel: these must not sit on a data line."""
    ax = t.axes
    if ax is None or getattr(t, "_may_touch", False):
        return False
    if t in (ax.title, ax._left_title, ax._right_title, ax.xaxis.label, ax.yaxis.label):
        return False
    if t in ax.xaxis.get_ticklabels(which="both") or t in ax.yaxis.get_ticklabels(which="both"):
        return False
    return True


def may_touch(*texts):
    """Allow these texts to touch data lines (e.g. a value written on its own reference line)."""
    for t in texts:
        t._may_touch = True
    return texts[0] if len(texts) == 1 else texts


def check(fig):
    """Raise SystemExit listing every violation of the axis rule, every overlap between two pieces of text and
    every piece of text (annotation, legend, note) drawn across a data line."""
    from matplotlib.path import Path as MPath
    msgs = []
    value = fig.__dict__.get("_value_axes", set())
    free = fig.__dict__.get("_free_axes", set())
    for k, ax in enumerate(fig.axes):
        if not ax.get_visible() or not ax.axison:
            continue
        name = ax.get_title() or f"panel {k + 1}"
        for which, axis in (("x", ax.xaxis), ("y", ax.yaxis)):
            if len(axis.get_minorticklocs()):
                msgs.append(f"{name} [{which}]: minor ticks")
            if (id(ax), which) in value:
                msgs += [f"{name} [{which}]: {m}" for m in _axis_problems(ax, which)]
            elif (id(ax), which) not in free:
                msgs.append(f"{name} [{which}]: axis not set with value_axis, log_axis or free_axis")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts = _texts(fig, renderer)
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            (a, ba), (b, bb) = texts[i], texts[j]
            if ba.shrunk(0.96, 0.85).overlaps(bb.shrunk(0.96, 0.85)):
                msgs.append(f"text overlap: {a.get_text()[:40]!r} / {b.get_text()[:40]!r}")
    for t, bb in texts:     # notes placed in axes coordinates must stay inside their panel
        ax = t.axes
        if ax is not None and _is_free_text(t) and t.get_transform() == ax.transAxes \
                and not isinstance(t, matplotlib.text.Annotation):
            box = ax.get_window_extent(renderer)
            if bb.x0 < box.x0 - 1 or bb.x1 > box.x1 + 1 or bb.y0 < box.y0 - 1 or bb.y1 > box.y1 + 1:
                msgs.append(f"text outside its panel: {t.get_text()[:40]!r}")
    boxes = [(t.get_text()[:40], bb) for t, bb in texts if _is_free_text(t)]
    for ax in fig.axes:
        leg = ax.get_legend()
        if leg is not None and leg.get_visible():
            boxes.append(("legend", leg.get_window_extent(renderer)))
    for label, bb in boxes:
        box = bb.padded(1.0)
        for ax in fig.axes:
            if not ax.get_window_extent(renderer).overlaps(box):
                continue
            for line in ax.get_lines():
                if not line.get_visible() or getattr(line, "_may_touch", False) or len(line.get_xdata()) < 2:
                    continue
                xy = line.get_transform().transform(line.get_xydata())
                path = MPath(xy[~(~(xy == xy)).any(axis=1)])
                if len(path.vertices) > 1 and path.intersects_bbox(box, filled=False):
                    msgs.append(f"text on a line: {label!r} ({line.get_label()})")
                    break
    if msgs:
        raise SystemExit("Figure check failed:\n  " + "\n  ".join(dict.fromkeys(msgs)))


def _checked(fig, tag):
    """check(fig); with FIGURE_DEBUG set to a folder, a rejected figure is saved there for inspection."""
    try:
        check(fig)
    except SystemExit:
        if os.environ.get("FIGURE_DEBUG"):
            fig.savefig(Path(os.environ["FIGURE_DEBUG"]) / f"{tag}_rejected.png")
        raise


def _heading(fig, text):
    """Bold heading above the panels, broken into lines so that it is no wider than the panels."""
    fig.canvas.draw()
    fig.set_layout_engine("none")          # the heading goes above the panels and does not move them
    renderer = fig.canvas.get_renderer()
    tight = fig.get_tightbbox(renderer)    # inches
    width = tight.width * fig.dpi * 0.99
    words, lines = text.replace("\n", " ").split(" "), []
    t = fig.suptitle("", x=tight.x0 / fig.get_figwidth(), y=tight.y1 / fig.get_figheight() + 0.03, ha="left",
                     va="bottom", fontsize=9.5, fontweight="bold")
    for w in words:
        trial = (lines[-1] + " " + w) if lines else w
        t.set_text(trial)
        if lines and t.get_window_extent(renderer).width > width:
            lines.append(w)
        elif lines:
            lines[-1] = trial
        else:
            lines.append(w)
    t.set_text("\n".join(lines))
    return t


def save_figure(name, draw, heading=None, out_dir=None):
    """`draw()` returns a figure; `heading()` returns its title, which is shown in the PNG only (in the note the
    caption carries the title). The figure is checked before anything is written."""
    out = Path(out_dir) if out_dir is not None else FIG_DIR
    out.mkdir(parents=True, exist_ok=True)
    fig = draw()
    _checked(fig, name)
    fig.savefig(out / f"{name}.pdf")
    if heading is not None:
        _heading(fig, heading())
        _checked(fig, name + "_heading")
    fig.savefig(out / f"{name}.png")
    plt.close(fig)
