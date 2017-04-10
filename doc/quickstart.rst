Quickstart
**********

Installation
============

To install Effective automatically using `pip`_ do::

  pip install effective

The source can be downloaded from the `GitHub repository`_.

.. _pip: https://pypi.python.org/pypi/pip/

.. _GitHub repository: https://github.com/jccriado/effective

A simple example
================

In this section we will be creating a simple model to show
some of the features of Effective. This example and more,
involving more complex cases that make use of the `extras`
package can be found in the `examples folder`_ at the
GitHub repository of the project.

.. _examples folder: https://github.com/jccriado/effective/tree/master/examples

The model  is described as follows: symmetry
:math:`SU(2)\times U(1)` containing a complex scalar doublet
:math:`\phi` (the Higgs) with hypercharge :math:`1/2` and a real
scalar triplet :math:`\Xi` with zero hypercharge that couple as:

.. math::
   \mathcal{L}_{int} = - \kappa\Xi^a\phi^\dagger\sigma^a\phi
   - \lamb \Xi^a \Xi^a \phi^\dagger\phi,

where :math:`\kappa` and :math:`\lamb` are a coupling constants
and :math:`\sigma^a` are the Pauli matrices. We will then integrate
out the heavy scalar :math:`\Xi` to obtain an effective Lagrangian
which we will finally write in terms of the operators.

.. math::
   \mathcal{O}_\phi=(\phi^\dagger\phi)^3,\;
   \mathcal{O}_{\phi 4}=(\phi^\dagger\phi)^2

Creation of the model
---------------------

The imports that we will need are::

  from effective.operators import (
      TensorBuilder, FieldBuilder, Op, OpSum,
      number_op, tensor_op, boson, fermion, kdelta)

  from effective.integration import RealScalar, integrate

  from effective.transformations import apply_rules

  from effective.output import Writer

The basic building blocks of our model are **tensors** and **fields**.
For our example, we will need three tensors, the Pauli matrices and the
coupling constants::
   
   sigma = TensorBuilder("sigma")
   kappa = TensorBuilder("kappa")
   lamb = TensorBuilder("lamb")

We will also use three fields: the Higgs doublet, its conjugate and the
new scalar::
   
   phi = FieldBuilder("phi", 1, boson)
   phic = FieldBuilder("phic", 1, boson)
   Xi = FieldBuilder("Xi", 1, boson)

The second argument of ``FieldBuilder`` represent the energy dimensions
of the field, and the third corresponds its the statistics and can either
be ``boson`` or ```fermion``.

Now we are ready to write the interaction Lagrangian::
  
   interaction_lagrangian = -OpSum(
        Op(kappa(), Xi(0), phic(1), sigma(0, 1, 2), phi(2)),
	Op(lamb(), Xi(0), Xi(0), phic(1), phi(1)))

Integration
-----------

Before doing the integration of the heavy fields, we must specify who they are. 
To integrate out the heavy :math:`\Xi` we do::
  
  heavy_Xi = RealScalar("Xi", 1)

Now it is ready to be integrated out::

  heavy_fields = [heavy_Xi]
  max_dim = 6
  effective_lagrangian = integrate(
      heavy_fields, interaction_lagrangian, max_dim)

Transformations of the effective Lagrangian
-------------------------------------------

After the integration we get operators that contain
:math:`(\phi^\dagger\sigma^a\phi)(\phi^\dagger\sigma^a\phi)`.
This product can be rewritten in terms of the operator
:math:`(\phi^\dagger\phi)^2`. To do this, we can use the
:math:`SU(2)` Fierz identity:

.. math::
   \sigma^a_{ij}\sigma^a_{kl}=2\delta_{il}\delta_{kj}-\delta_{ij}\delta_{kl}.

We can define a rule to transform everything that matches the
left-hand side of the equality into the right-hand with the code::

  fierz_rule = (
      Op(sigma(0, -1, -2), sigma(0, -3, -4)),
      OpSum(number_op(2) * Op(kdelta(-1, -4), kdelta(-3, -2)),
            -Op(kdelta(-1, -2), kdelta(-3, -4))))
	      
Notice the use of the function ``number_op``. Observe also the
appearance of negative indices to represent free (not contracted)
indices and how those of the replacement match the ones in the
pattern.

We should now define the operators in terms of which we want to
express the effective Lagrangian::

  Ophi = tensor_op("Ophi")
  Ophi4 = tensor_op("Ophi4")

and then use some rules to express them in terms of the fields and
tensors that appear in the effective Lagrangian::

  definition_rules = [
      (Op(phic(0), phi(0), phic(1), phi(1), phic(2), phi(2)),
       OpSum(Ophi)),
      (Op(phic(0), phi(0), phic(1), phi(1)),
       OpSum(Ophi4))]

To apply the Fierz identity to every operator until we get to the
chosen operators, we do::

  rules = [fierz_rule] + definition_rules
  max_iterations = 2
  transf_eff_lag = apply_rules(
      effective_lagrangian, rules, max_iterations)

Output
------

The class ``Writer`` can be used to represent the coefficients
of the operators of a Lagrangian as plain text and write it to a file::

  final_op_names = ["Ophi", "Ophi4"]
  eff_lag_writer = Writer(trasnf_eff_lag, final_op_names)
  eff_lag_writer.write_text_file("simple_example")

It can also to write a LaTeX file with the representation of these
coefficients and export it to pdf to show it directly. For this to
be done, we should define how the objects that we are using have to
be represented in LaTeX code and the symbols we want to be used as
indices::

  latex_tensor_reps = {"kappa": r"\kappa",
                       "lamb": r"\lambda",
                       "MXi": r"M_{{\Xi}}",
                       "phi": r"\phi_{}",
                       "phic": r"\phi^*_{}"}

  latex_op_reps = {"Ophi": r"\frac{{\alpha_{{\phi}}}}{{\Lambda^2}}",
                   "Ophi4": r"\mathcal{{O}}_{{\phi 4}}"}
		   
  latex_indices = ["i", "j", "k", "l"]
  
  eff_lag_writer.write_pdf(
      "simple_example", latex_tensor_reps, 
      latex_op_reps, latex_indices)

Double curly brackets are used when one curly bracket should be
present in the LaTeX code and simple curly brackes are used as
placeholders for indices.

The expected result is a pdf file containing the coefficients
for the operators we defined plus some other operators with
covariant derivatives of the Higgs.