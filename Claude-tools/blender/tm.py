"""Shared tone mapping for the sheets and the HTML mixer (the page uses the same numbers)."""
import numpy as np
WB = np.array([0.62, 1.0, 1.75], 'float32')     # white balance: the eye half-adapts to warm lamps
EV = 5.0                                        # one fixed camera exposure for every picture
def curve(x): return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1) ** (1 / 2.2)
def tone(lin, ev=EV): return (curve(np.maximum(lin.astype('float32') * WB * ev, 0)) * 255 + 0.5).astype('uint8')
