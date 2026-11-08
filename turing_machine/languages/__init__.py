"""
Módulo de linguagens pré-configuradas para a Máquina de Turing.
"""

from turing_machine.languages.an_bn_cn import create_an_bn_cn_machine
from turing_machine.languages.ww import create_ww_machine

__all__ = ["create_an_bn_cn_machine", "create_ww_machine"]
