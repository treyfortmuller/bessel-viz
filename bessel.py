import plotly.graph_objects as go
import numpy as np
from scipy import special

t = np.linspace(0, 10, 1000)

fig = go.Figure()

RADIUS = 3
MODE = 2


def compute_modal_freq(boundary, order, mode):
    # grab the zero for the mode and order that we care about
    zero = special.jn_zeros(order, mode)[mode - 1]
    return zero / boundary


# of the first kind
for n in range(0, 5):
    freq = compute_modal_freq(RADIUS, n, MODE)

    fig.add_trace(
        go.Scatter(x=t, y=special.jv(n, freq * t), name=f"j_{n}", mode="lines")
    )

# of the second kind
# for n in range(0, 5):
#     fig.add_trace(go.Scatter(
#         x=t, y=special.yn(n, t),
#         name=f'y_{n}',
#         mode="lines"
#     ))

fig.update_layout(
    title=f"Bessel Functions of the First Kind, boundary: {RADIUS}, mode: {MODE}",
    yaxis_zeroline=False,
    xaxis_zeroline=False,
)

fig.show()
