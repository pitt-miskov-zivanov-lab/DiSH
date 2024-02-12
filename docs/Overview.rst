

Overview
========

Modeling aids scientists in understanding system behavior and predicting future states via expert knowledge, literature, and experimental data. Large biological networks may pose challenges in determining all kinetic parameters, leading to qualitative, logical, and discrete modeling approaches. Logical models utilize Boolean variables with two discrete levels (1 for high concentration/active and 0 for low concentration/inactive) and logic operators to represent element concentration or activity. However, this restricts scenarios involving diverse effects, such as multiple drug doses or protein activity levels. Discrete models with more than two distinct levels address this limitation while avoiding the need for all kinetic parameters found in continuous models. In discrete models, the change in an element's value is determined by the difference between its positive and negative regulation scores. If the difference is non-zero, the element's value changes in the same direction as the difference, typically by one level.

Model introduction
===================

The DiSH2.0 (Discrete, Stochastic, Heterogeneous) modeling and simulation framework combines the advantages of logical and discrete modeling while accommodating varying degrees of information precision. It allows for hybrid models incorporating both logical and algebraic update functions, enabling optimal utilization of qualitative and quantitative information. Unlike previous approaches that used Boolean variables for discrete element values, DiSH2.0 employs discrete variables with any necessary number of levels, simplifying model creation and verification.

Key features of DiSH2.0 include:

1. **Memory**: Element update rules consider the previous value of an element when calculating its change.

2. **Regulation Weights**: Specialized notation accounts for varying effects across different regulators and levels.

3. **Spontaneous Increase and Decrease Behaviors**: Introduces flexibility in response to the balance between negative and positive regulators, with varying increment/decrement amounts.

4. **Simulation Compatibility**: The simulator supports deterministic and stochastic simulation schemes, expanding capabilities to hybrid models.

DiSH2.0 is demonstrated to improve accuracy and precision, offering compatibility with previously published logical models and other simulation tools. It utilizes the BioRECIPE representation format for models and interactions, facilitating human and machine readability and enabling full automation of the modeling pipeline, including interaction extraction, filtering, assembly, verification, and validation.

The method of DiSH2.0 involves the creation of hybrid models with logical and algebraic update functions, enabling the incorporation of qualitative and quantitative information. These models facilitate memory, regulation weights, and spontaneous behaviors, enhancing accuracy and flexibility in response to available information. The framework also includes a simulator supporting deterministic and stochastic simulation schemes, expanding the capabilities of hybrid modeling.


Simulation features
====================

- DiSH2.0 employs discrete variables to represent element values.
- Features memory in element update rules.
- Supports regulation weights to account for varying effects across regulators and levels.
- Compatible with deterministic and stochastic simulation schemes.
- Seamless integration into existing workflows for interaction extraction, filtering, network assembly, model verification, and validation.

