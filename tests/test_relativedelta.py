import pytest
from src.relativedelta import relativedelta, MO

def test_basic():
    rd = relativedelta(days=1)
    assert rd.days == 1
