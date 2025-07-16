import ast
from pathlib import Path
import pytest


def load_format_param_name():
    fp = Path(__file__).resolve().parents[1] / 'Native Instruments' / 'script' / 'screen_writer' / 'NILA_OLED.py'
    tree = ast.parse(fp.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'format_param_name':
            mod = ast.Module(body=[node], type_ignores=[])
            namespace = {}
            exec(compile(mod, filename=str(fp), mode='exec'), namespace)
            return namespace['format_param_name']
    raise RuntimeError('format_param_name not found')


format_param_name = load_format_param_name()


@pytest.mark.parametrize(
    "input_name,expected",
    [
        ("CutoffFreq1", "Cutoff Freq 1"),
        ("FilterQ2", "Filter Q2"),
        ("Pan12Gain", "Pan 12 Gain"),
    ],
)
def test_format_param_name_spacing(input_name, expected):
    assert format_param_name(input_name) == expected
