"""
This module defines tensors related to the
group :math:`SU(3)`.
"""

from efttools.operators import TensorBuilder, Op, OpSum, kdelta

epsSU3 = TensorBuilder("epsSU3")
r"""
Totally antisymmetric tensor :math:`\epsilon_{ABC}` with three
:math:`SU(3)` triplet indices such that :math:`\epsilon_{123}=1`.
"""

TSU3 = TensorBuilder("TSU3")
r"""
:math:`SU(3)` generators :math:`(T_A)_{BC}` (half of the Gell-Mann matrices).
"""

fSU3 = TensorBuilder("fSU3")
r"""
:math:`SU(3)` structure constants :math:`f_{ABC}`.
"""

rule_SU3_eps = (
    Op(epsSU3(0, -1, -2), epsSU3(0, -3, -4)),
    OpSum(-Op(kdelta(-1, -4), kdelta(-3, -2)),
          Op(kdelta(-1, -3), kdelta(-2, -4))))

rules_SU3 = [rule_SU3_eps]

latex_SU3 = {
    "epsSU3": r"\epsilon_{{{}{}{}}}",
    "TSU3": r"(T_{})_{{{}{}}}",
    "fSU3": r"f_{{{}{}{}}}"}
