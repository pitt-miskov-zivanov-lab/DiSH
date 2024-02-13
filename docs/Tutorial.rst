

Model Creation
===================

All columns names
--------------
- '#'
- 'Element Name'
- 'Element Type'
- 'Element Subtype'
- 'Element HGNC Symbol'
- 'Element Database'
- 'Element IDs'
- 'Compartment'
- 'Compartment ID'
- 'Cell Line'
- 'Cell Type'
- 'Tissue Type'
- 'Organism'
- 'Positive Regulator List'
- 'Positive Connection Type List'
- 'Positive Mechanism List'
- 'Positive Site List'
- 'Negative Regulator List'
- 'Negative Connection Type List'
- 'Negative Mechanism List'
- 'Negative Site List'
- 'Score List'
- 'Source List'
- 'Statements List'
- 'Paper IDs List'
- 'Positive Regulation Rule'
- 'Negative Regulation Rule'
- 'Variable'
- 'Value Type'
- 'Levels'
- 'State List 0'
- 'State List 1'
- 'Const OFF'
- 'Const ON'
- 'Increment'
- 'Spontaneous'
- 'Balancing'
- 'Delay'
- 'Update Group'
- 'Update Rate'
- 'Update Rank'

The model contains the following required elements:

+------------------------+-----------------------------------+----------------------------------------------------+
| Variable               | Positive Regulation Rule         | Negative Regulation Rule                         |
+========================+===================================+====================================================+
| State List             | Element Name                      | Element IDs                                        |
+------------------------+-----------------------------------+----------------------------------------------------+
| Element Type           |                                   |                                                    |
+------------------------+-----------------------------------+----------------------------------------------------+

Element Types
--------------

Valid types of elements include:

- protein
- protein family
- protein complex
- RNA
- mRNA
- gene
- chemical
- biological process

Simulation Parameters
---------------------

Schemes
~~~~~~~
DiSH support various simulation schemes, which can be categarized simultaneous and randomly update.
To check the descriptions of schemes, you could use:

.. code-block:: bash

  python simulator_interface.py -h


run and steps
~~~~~~~~~~~~~
DiSH simulator could simulate multiple runs with fixed time period. Typically, simulation time depends on the setting of steps, runs, and model size.
To setup the runs and steps, please use following bash command:

.. code-block:: bash

  python simulator_interface.py [model_filename] --runs [time] --steps [time period]

We also provide the [jupyter notebook] interface for visualization.

Increment
~~~~~~~~~
DiSH simulator provides two types of increment, unit increment and proportional increment(default).
If you want to set your increment as unit, please fill 0 in the column 'Increment'.

