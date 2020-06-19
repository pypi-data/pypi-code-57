from dataclasses import dataclass

import ppb
from ppb.utils import get_time
from ppb.systemslib import System

import easing_functions 


def ilerp(f1, f2, t):
    return int(f1 + t * (f2 - f1))

def flerp(f1, f2, t):
    return f1 + t * (f2 - f1)

def vlerp(v1, v2, t):
    return ppb.Vector(
        v1.x + t * (v2.x - v1.x),
        v1.y + t * (v2.y - v1.y),
    )

def tlerp(t1, t2, t):
    assert len(t1) == len(t2)
    return tuple(
        lerp(i1, i2, t)
        for (i1, i2) in zip(t1, t2)
    )

def lerp(a, b, t):
    if isinstance(a, tuple):
        value = tlerp(a, b, t)
    elif isinstance(a, ppb.Vector):
        value = vlerp(a, b, t)
    elif isinstance(a, int):
        value = ilerp(a, b, t)
    else:
        value = flerp(a, b, t)
    return value


EASING = {
    'back_in': easing_functions.BackEaseIn().ease,
    'back_in_out': easing_functions.BackEaseInOut().ease,
    'back_out': easing_functions.BackEaseOut().ease,
    'bounce_in': easing_functions.BounceEaseIn().ease,
    'bounce_in_out': easing_functions.BounceEaseInOut().ease,
    'bounce_out': easing_functions.BounceEaseOut().ease,
    'circ_in': easing_functions.CircularEaseIn().ease,
    'circ_in_out': easing_functions.CircularEaseInOut().ease,
    'circ_out': easing_functions.CircularEaseOut().ease,
    'cubic_in': easing_functions.CubicEaseIn().ease,
    'cubic_in_out': easing_functions.CubicEaseInOut().ease,
    'cubic_out': easing_functions.CubicEaseOut().ease,
    'elastic_in': easing_functions.ElasticEaseIn().ease,
    'elastic_in_out': easing_functions.ElasticEaseInOut().ease,
    'elastic_out': easing_functions.ElasticEaseOut().ease,
    'exp_in': easing_functions.ExponentialEaseIn().ease,
    'exp_in_out': easing_functions.ExponentialEaseInOut().ease,
    'exp_out': easing_functions.ExponentialEaseOut().ease,
    'linear': easing_functions.LinearInOut().ease,
    'quad_in': easing_functions.QuadEaseIn().ease,
    'quad_in_out': easing_functions.QuadEaseInOut().ease,
    'quad_out': easing_functions.QuadEaseOut().ease,
    'quartic_in': easing_functions.QuarticEaseIn().ease,
    'quartic_in_out': easing_functions.QuarticEaseInOut().ease,
    'quartic_out': easing_functions.QuarticEaseOut().ease,
    'quint_in': easing_functions.QuinticEaseIn().ease,
    'quint_in_out': easing_functions.QuinticEaseInOut().ease,
    'quint_out': easing_functions.QuinticEaseOut().ease,
    'sine_in': easing_functions.SineEaseIn().ease,
    'sine_in_out': easing_functions.SineEaseInOut().ease,
    'sine_out': easing_functions.SineEaseOut().ease,
}


@dataclass
class Tween:
    start_time: float
    end_time: float
    obj: object
    attr: str
    start_value: object
    end_value: object
    easing: str = "linear"


class Tweener:
    """A controller of object transitions over time.
    
    A Tweener has to be added to a scene in order to work! After creating it,
    make multiple calls to tween() to set transitions of object members over
    time. Callbacks may be added to the Tweener with when_done() and all
    callbacks will be invoked when the final transition ends.

    Example:

        t = Tweener()
        t.tween(bomb, 'position', v_target, 1.0)
        t.when_done(play_sound("BOOM"))
    """

    size = 0

    def __init__(self, name=None):
        self.name = name or f"tweener-{id(self)}"
        self.tweens = []
        self.callbacks = []
        self.last_frame = get_time()
        # self.used = False
        # self.done = False

    def __hash__(self):
        return hash(id(self))

    @property
    def is_tweening(self):
        return bool(self.tweens)

    def tween(self, entity, attr, *args, **kwargs):
        if len(args) == 2:
            end_value, duration = args
            start_value = getattr(entity, attr)
        elif len(args) == 3:
            start_value, end_value, duration = args
        delay = kwargs.pop('delay', 0)
        self.used = True
        start_time = get_time() + delay
        self.tweens.append(Tween(
            start_time=start_time,
            end_time=start_time + duration,
            obj=entity,
            attr=attr,
            start_value=start_value,
            end_value=end_value,
            **kwargs,
        ))
    
    def cancel(self):
        self.tweens[:] = []
        self.callbacks[:] = []
    
    def when_done(self, func):
        self.callbacks.append(func)

    def on_pre_render(self, update, signal):
        t = get_time()
        d = update.time_delta
        self.last_frame = t
        clear = []

        for i, tween in enumerate(self.tweens):
            if tween.start_time > t:
                continue
            if tween.start_value is None:
                tween.start_value = getattr(tween.obj, tween.attr)
            tr = (t - tween.start_time) / (tween.end_time - tween.start_time)
            tr = min(1.0, max(0.0, tr))
            tr = EASING[tween.easing](tr)
            value = lerp(tween.start_value, tween.end_value, tr)
            setattr(tween.obj, tween.attr, value)
            if tr >= 1.0:
                clear.append(i)

        for i in reversed(clear):
            del self.tweens[i]
        
        if not self.is_tweening:
            callbacks = self.callbacks[:]
            self.callbacks.clear()
            for func in callbacks:
                func()


class Tweening(System):
    scene = None
    current_tweener = None

    @classmethod
    def on_scene_started(cls, ev, signal):
        cls.scene = ev.scene
        cls.current_tweener = Tweener()
        cls.scene.add(cls.current_tweener, tags=['tweener'])
    
    @classmethod
    def on_scene_continued(cls, ev, signal):
        cls.scene = ev.scene
        cls.current_tweener = list(cls.scene.get(tag='tweener'))[0]
    

def tween(*args, **kwargs):
    Tweening.current_tweener.tween(*args, **kwargs)
