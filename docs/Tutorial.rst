Tutorial
========
This is a tutorial for DiSH simulator.

I/O
---------
Input includes: 
- a .xlsx file containing the model to simulate, in the BioRECIPES tabular format, `see example`_

.. _see example: https://github.com/pitt-miskov-zivanov-lab/DiSH/blob/main/example/input/Tcell_N5_PTEN4_bio.xlsx

- simulation `setup`_

.. _setup: 

Simulation Setups
------------------

Output includes:
- a .txt file containing all the trace of every element at each run, `see example`_

.. _see example: https://github.com/pitt-miskov-zivanov-lab/DiSH/blob/main/example/output/trace.txt

output file could export with different formats. Users could choose specific format before simulation.

.. list-table:: Output Trace File Formats
  :widths: 20, 30
  :header-rows: 1

  * - # of format
    - Description
  * - 1
    - traces for all runs and frequency summary (default for sync)
  * - 2
    - traces for all runs in transpose format
  * - 3
    - trace file with frequency summary only (default for ra scheme)
  * - 4 
    - model rules and truth tables
  * - 5
    - model rules
  * - 6
    - truth tables
  * - 7
    - event traces including elements updated at each step

Model Creation
--------------

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

Simulation Setups
---------------------
DiSH could interact with either `bash` command or Jupyter Notebook. Users could use either interface to setup their simulations, here we provide several parameters description:

- Schemes (default value: ra):
  DiSH support various simulation schemes, which can be categarized simultaneous and randomly update.
  To check the descriptions of schemes, you could use:

  .. code-block:: bash

    python simulator_interface.py -h


- Run and Steps (default value: 100 and 1000):
  DiSH simulator could simulate multiple runs with fixed time period. Typically, simulation time depends on the setting of steps, runs, and model size.
  To setup the runs and steps, please use following bash command:

  .. code-block:: bash

    python simulator_interface.py [model_filename] [output trace file] --runs [time] --steps [time period]

  We also provide the [jupyter notebook] interface for visualization.

- Increment (default value: proportional to regulation scores):
  DiSH simulator provides two types of increment, unit increment and proportional increment(default).
  If you want to set your increment as unit, please fill 0 in the column 'Increment'.

- Output Format (default value: 0):
  The output of simulator is a text file of trace file, it includes the trace of every element at each run. 

- Normalize Output(default value: True):
  The level of trace could be either integers or float number from 0 to 1. 

The model filename, output_trace_filename, and simulation scheme are required to provide by the users. Users could tune the above parameters by themselves as well. For example, this is a command for simulating a T cell model by setting 50 runs, 200 steps, simultaneously updating scheme.

.. code-block:: bash 

  python simulator_interface.py [T cell model filename] [output trace file] --sim_scheme sync --runs 50 --steps 200


