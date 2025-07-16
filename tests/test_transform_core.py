import ast
import math
from pathlib import Path
import pytest


def load_function(path: Path, name: str, inject_globals=None):
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            mod = ast.Module(body=[node], type_ignores=[])
            ns = {} if inject_globals is None else dict(inject_globals)
            exec(compile(mod, filename=str(path), mode='exec'), ns)
            return ns[name]
    raise RuntimeError(f"{name} not found in {path}")


def load_voltodB():
    path = Path(__file__).resolve().parents[1] / 'Native Instruments' / 'script' / 'device_setup' / 'NILA_transform.py'
    return load_function(path, 'VolTodB', {'math': math})


def load_timeConvert():
    path = Path(__file__).resolve().parents[1] / 'Native Instruments' / 'script' / 'device_setup' / 'NILA_core.py'
    return load_function(path, 'timeConvert')


@pytest.mark.parametrize("value,expected", [
    (0, "- oo"),
    (1.0, 5.6),
    (0.5, -9.2),
])
def test_voltodB(value, expected):
    func = load_voltodB()
    assert func(value) == expected


class PlaylistStub:
    def __init__(self, bar, step):
        self.bar = bar
        self.step = step

    def getVisTimeBar(self):
        return self.bar

    def getVisTimeStep(self):
        return self.step


class UIStub:
    def __init__(self, min_display):
        self._min_display = min_display

    def getTimeDispMin(self):
        return self._min_display


@pytest.mark.parametrize(
    "bar,step,min_flag,expected",
    [
        (3, "5", False, ("Beats:Bar", "3:05")),
        (2, "12", True, ("Min:Sec", "2:12")),
        (4, "Precount", False, ("REC in...", "Precount")),
    ],
)
def test_timeConvert(bar, step, min_flag, expected):
    func = load_timeConvert()
    func.__globals__['playlist'] = PlaylistStub(bar, step)
    func.__globals__['ui'] = UIStub(min_flag)
    assert func("", "") == expected
