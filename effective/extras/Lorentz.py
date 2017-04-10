"""
This module defines rules related to the Lorentz group.
"""

from effective.operators import (
    TensorBuilder, Op, OpSum, number_op, kdelta,
    epsUp, epsUpDot, epsDown, epsDownDot, sigma4, sigma4bar)

eps4 = TensorBuilder("eps4")
r"""
Totally antisymmetric tensor with four Lorentz vector indices
:math:`\epsilon_{\mu\nu\rho\sigma}` where :math:`\epsilon_{0123}=1`.
"""

sigmaTensor = TensorBuilder("sigmaTensor")
r"""
Lorentz tensor 
:math:`\sigma^{\mu\nu}=\frac{i}{4}\left(
\sigma^\mu_{\alpha\dot{\gamma}}\bar{\sigma}^{\nu\dot{\gamma}\beta}-
\sigma^\nu_{\alpha\dot{\gamma}}\bar{\sigma}^{\mu\dot{\gamma}\beta}
\right)`.
"""

rule_Lorentz_free_epsUp = (
    Op(epsUp(-1, -2), epsUpDot(-3, -4)),
    OpSum(-number_op(0.5) * Op(sigma4bar(0, -3, -1), sigma4bar(0, -4, -2))))
r"""
Substitute :math:`\epsilon^{\alpha\beta}\epsilon^{\dot{\alpha}\dot{\beta}}`
by

.. math::
    -\frac{1}{2} \bar{\sigma}^{\mu,\dot{\alpha}\alpha}
    \bar{\sigma}^{\dot{\beta}\beta}_\mu
"""

rule_Lorentz_free_epsDown = (
    Op(epsDown(-1, -2), epsDownDot(-3, -4)),
    OpSum(-number_op(0.5) * Op(sigma4(0, -1, -3), sigma4(0, -2, -4))))
r"""
Substitute :math:`\epsilon_{\alpha\beta}\epsilon_{\dot{\alpha}\dot{\beta}}`
by

.. math::
    -\frac{1}{2} \bar{\sigma}^\mu_{\alpha\dot{\alpha}}
    \bar{\sigma}_{\mu,\beta\dot{\beta}}
"""

rules_Lorentz_eps_cancel = [
    (Op(epsUp(0, -1), epsDown(0, -2)), -OpSum(Op(kdelta(-1, -2)))),
    (Op(epsDown(-1, 0), epsUp(0, -2)), -OpSum(-Op(kdelta(-1, -2)))),
    (Op(epsUp(-1, 0), epsDown(-2, 0)), -OpSum(Op(kdelta(-1, -2))))]
r"""
Substitute contracted :math:`\epsilon` tensors with undotted indices
by the corresponding Kronecker delta.
"""

rules_Lorentz_epsDot_cancel = [
    (Op(epsUpDot(-1, 0), epsDownDot(0, -2)), -OpSum(-Op(kdelta(-1, -2)))),
    (Op(epsUpDot(-1, 0), epsDownDot(-2, 0)), -OpSum(Op(kdelta(-1, -2)))),
    (Op(epsDownDot(-1, 0), epsUpDot(0, -2)), -OpSum(-Op(kdelta(-1, -2))))]
r"""
Substitute contracted :math:`\epsilon` tensors with dotted indices
by the corresponding Kronecker delta.
"""

rules_Lorentz_free_eps = [
    (Op(epsUp(-1, -2), epsDown(-3, -4)),
     OpSum(-Op(kdelta(-1, -3), kdelta(-2, -4)),
           Op(kdelta(-1, -4), kdelta(-2, -3)))),

    (Op(epsUpDot(-1, -2), epsDownDot(-3, -4)),
     OpSum(-Op(kdelta(-1, -3), kdelta(-2, -4)),
           Op(kdelta(-1, -4), kdelta(-2, -3))))]

rules_Lorentz = ([rule_Lorentz_free_epsUp, rule_Lorentz_free_epsDown] +
                 rules_Lorentz_eps_cancel + rules_Lorentz_epsDot_cancel +
                 rules_Lorentz_free_eps)
r"""All the rules defined in :mod:`effective.extras.Lorentz` together"""


latex_Lorentz = {
    "eps4": r"\epsilon_{{{}{}{}{}}}",

    "epsUp": r"\epsilon^{{{}{}}}",
    "epsUpDot": r"\epsilon^{{\dot{{{}}}\dot{{{}}}}}",
    "epsDown": r"\epsilon_{{{}{}}}",
    "epsDownDot": r"\epsilon_{{\dot{{{}}}\dot{{{}}}}}",
    "sigma4bar": r"\bar{{\sigma}}_{{4{}}}^{{\dot{{{}}}{}}}",
    "sigma4": r"\sigma^{{4{}}}_{{{}\dot{{{}}}}}",
    "deltaUpDown": r"\delta^{}_{}",
    "deltaUpDownDot": r"\delta_{{\dot{{{}}}}}^{{\dot{{{}}}}}"}
r"""
LaTeX code representation of the Lorentz tensors.
"""