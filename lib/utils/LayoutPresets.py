from lib.object.visual.Layout import Layout
from pygame import (K_DELETE, K_DOWN, K_END, K_HOME, K_INSERT, K_LEFT,
                    K_PAGEDOWN, K_PAGEUP, K_RCTRL, K_RIGHT, K_RSHIFT, K_SPACE,
                    K_UP, K_a, K_d, K_h, K_i, K_j, K_k, K_l, K_n, K_s, K_w,
                    K_x)


class LayoutPresets:
    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RCTRL)
    EXTRA1_KB_LAYOUT = Layout(K_i, K_k, K_j, K_l, K_n, K_h)
    EXTRA2_KB_LAYOUT = Layout(K_HOME, K_END, K_DELETE, K_PAGEDOWN, K_INSERT, K_PAGEUP)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT, EXTRA1_KB_LAYOUT, EXTRA2_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(-0.2, 0.2, -0.2, 0.2, 2, 10)
    XBOX_CONTROLLER_LAYOUT = Layout(-0.2, 0.2, -0.2, 0.2, 2, 5)
