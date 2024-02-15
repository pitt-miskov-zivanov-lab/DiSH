Tutorial
========
This is a tutorial for DiSH simulator. The simulation typically involves in two steps, model creation and simulation setups. 

I/O
---------
Input includes: 

- a .xlsx file containing the model to simulate, in the BioRECIPES tabular format, `see input example`_

.. _see input example: https://github.com/pitt-miskov-zivanov-lab/DiSH/blob/main/example/input/Tcell_N5_PTEN4_bio.xlsx


- Simulation `setups <https://github.com/pitt-miskov-zivanov-lab/DiSH/blob/main/docs/Tutorial.rst>`_

Output includes:

- a .txt file containing all the trace of every element at each run, `see output example`_

.. _see output example: https://github.com/pitt-miskov-zivanov-lab/DiSH/blob/main/example/output/trace.txt


output file could export with different formats. Users could choose specific format before simulation.

.. list-table:: Output Trace File Formats
  :widths: 10, 30
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

DiSH supports BioRECIPE model file that includes element, regulation, and DiSH simulation parameters parts. For element and regulation parts, please check `BioRECIPE doc`_ for more information.
The model contains the following required elements:

.. _BioRECIPE doc: https://melody-biorecipe.readthedocs.io/en/latest/model_representation.html

- Variable
- Positive Regulation Rule
- Negative Regulation Rule
- State List
- Element Name
- Element IDs
- Element Type

Regulation Rule
~~~~~~~~~~~~~~~~~~~
The level of elements are all updated by corresponding regulation rules, users should define the regulation rule in the `Positive Regulation Rule` and `Negative Regulation Rule` column.
Regulation rule are consisted of `variable name` and `operator`, every `variable name` in the regulation rule is the level of the element.
DiSH2.0 offers several operators for representation of `Regulation Rule`.


- Logical representation:

    - logical OR: A,B, which is `:math: max(A, B)` for discrete variables

    - logical AND: (A,B), which is `:math: min(A, B)` for discrete variables

    - logical Not: !A, which is n's complement for discrete variables


- Arithmetic representation:

    - summation: A+B

    - multiplication: c*A, c could be a constant or the level of the element (except for the weight of necessary and enhance elements)

- Truth table representation:

    - Truth table sheet should be included in the same model file. `see example <https://github.com/pitt-miskov-zivanov-lab/DiSH/tree/main/example/input>`_
    - The first cell of the sheet is the regulated element, The following cells in the first row indicate whether reset the level of the element for each update, otherwise, use `un-reset` to keep the value of the element
    - The second is the regulators for the element, to be noticeably, the last three column should be always 'element name', 'Value', and 'regulation delays'.

.. list-table:: Example of truth table of A with (A,B)+C, for which the level of A, B, C are all 2.
    :widths: 7, 7, 7, 7, 10
    :header-rows: 1

    * - A
      - reset
      -
      -
      -

    * - B
      - C
      - A
      - Value
      - regulations delays

    * - 0
      - 0
      - 0
      - 0
      - 0

    * - 0
      - 0
      - 1
      - 1
      - 0

    * - 0
      - 1
      - 0
      - 0
      - 0

    * - 0
      - 1
      - 1
      - 1
      - 0

    * - 1
      - 0
      - 0
      - 0
      - 0

    * - 1
      - 0
      - 1
      - 1
      - 0

    * - 1
      - 1
      - 0
      - 1
      - 0

    * - 1
      - 1
      - 1
      - 1
      - 0

- Delay representation

    - Timing delay: this setting is located in `Delay` column, the input is a list of steps for every level changing. For example,
      if the level is 3, then delay will be set as time from 0 to 1, time from 1 to 2, time from 2 to 1, and time from 1 to 0. The figure demonstrates the delay settings.
      Users could also input only one steps, DiSH would automatically delay updating the element with that steps for every level changing.

    - Propagation delay: propagation delay is the time of effect to travel from regulator to regulated element. It could be set either in regulation rule columns or in the truth table.
      To present propagation delay, use `time~regulator_name`. In the truth table, users could add them in the header row.

    - Spontaneous delay: spontaneous delay corresponds to spontaneous behavior.

    - Balancing delay: balancing delay is represented as 'decrease/increase, delay_time` in the `Balancing` column.

.. list-table:: example: element A is impacted by signal B, and the propagation delay is 5 steps

    * - Variable
      - Positive Regulation Rule
      - Negative Regulation Rule

    * - A
      - 5~B
      -

- Regulator representation

    - Initializer: represented as `{regulator_name}`, which means that the element could be updated if regulator's level is nonzero.

    - Necessary pair: represented as `{Necessary_element}[Enhance_element]`, it returns the summation of the score by necessary and enhance elements or the max value of them.

    - Value regulator: `regulator=value`, it represents regulator affects this element when the level of regulator equal to value. If this regulator affects the element, the regulatory score is the maximum value otherwise, is 0.

    - Highest-value regulator: `regulator^`, which means that this regulator has a effect when regulator's value is in its full level. If this regulator affects the element, the regulatory score is the maximum value otherwise, is 0.


Create and Parse Rule
~~~~~~~~~~~~~~~~~~~~~~~~
A regulation rule could represent multiple events and reactions, which are called groups, in a single line. all the events and reaction rules are connected with either a comma outside of brackets or a plus sign.
For every group, they could be a single regulator or a expression consisted by the representation we listed above.

For comma outside of the brackets, the representations could be used in group are:

- binary logical AND(,)
- logical NOT '!'
- arithmetic multiplication '*'
- initializer{}, necessary element, enhance element{}[], they could be multiple regulators splitting by commas
- propagation delay '~'
- Highest-value regulator '^'

For plus sign connector, the usable representations are:

- arithmetic multiplication '*'
- logical NOT '!'
- initializer{}, necessary and enhance element{}[], they should all be a single regulator
- propagation delay '~'
- Highest-value regulator '^'

DiSH recursively parses the regulation rule with depth-first searching.
The mixed representation between logical and arithmetic expression is not allowed, for example, (A,B)+C is invalid, since regulator or regulatory subexpression should be separated by either `+` or `comma`.
Instead, users could use truth table to get their desired functions. We also provide the `example <https://github.com/pitt-miskov-zivanov-lab/DiSH/tree/main/example/input>`_ for this.


.. Attention::

    - Regulation Rules are parsed recursively. However, initializer is not allowed to be embedded by another initializer (e.g. `{Akt{CD4}}+CD28` is invalid for regulation rule parser).

    - Weight of initializer, necessary element, and enhance element should be a constant


Optional Columns
~~~~~~~~~~~~~~~~~~~

In simulation parameter, except for the required inputs `Regulation Rule`, `State List`, it also supports following optional parameter setting:

.. list-table:: Simulation Parameters Settings
    :widths: 6, 15, 8
    :header-rows: 1

    * - Column Name
      - Description
      - Default Value

    * - Level
      - number of discrete variable levels for that element
      - 3

    * - Increment
      - specify a number greater than 0 to set the increment as proportional to the difference between positive and negative regulation scores, multiplied by the input number. if set to 0, the increment when an element is updated is always 1 or -1 level depending on whether positive or negative regulation is greater, respectively
      - 1

    * - Delay
      - state transition delays in the format delay01,delay12,delay21,delay10 for 3 states. If only one delay is listed it will be used for all state transitions
      - Empty

    * - Balancing
      - specifies what happens when positive and negative regulation scores are equal, with optional delay
      - decrease,0

    * - Spontaneous
      - specifies spontaneous behavior for elements with either no positive or no negative regulators. input as an integer specifying delay in spontaneous behavior: "0" specifies spontaneous behavior with no delay
      - 0

    * - Update Groups
      - for group-based simulation schemes, elements in the same group will be updated in the same simulation step
      - Empty

    * - Update Rate
      - for Random Asynchronous simulation,
      - Empty

    * - Update Rank
      - For round based simulation. Elements with higher update rank will be run before elements with lower update rank.
      - 0



Simulation Setups
---------------------
DiSH could interact with either `bash` command or Python code. Users could use either interface to setup their simulations, here we provide several parameters description:

bash command
~~~~~~~~~~~~~~

- ``Schemes`` (default value: ra):
  DiSH support various simulation schemes, which can be categarized simultaneous and randomly update.
  To check the descriptions of schemes, you could use:

  .. code-block:: bash

    python simulator_interface.py -h

  .. image:: DiSH_schemes.png
    :width: 600
    :alt: Simulation Schemes

- ``Run and Steps`` (default value: 100 and 1000):
  DiSH simulator could simulate multiple runs with fixed time period. Typically, simulation time depends on the setting of steps, runs, and model size.
  To setup the runs and steps, please use following bash command:

  .. code-block:: bash

    python simulator_interface.py [model_filename] [output trace file] --runs [time] --steps [time period]

  We also provide the [jupyter notebook] interface for visualization.

- ``Increment`` (default value: proportional to regulation scores):
  DiSH simulator provides two types of increment, unit increment and proportional increment(default).
  If you want to set your increment as unit, please fill 0 in the column 'Increment'.

- ``Output Format`` (default value: 0):
  The output of simulator is a text file of trace file, it includes the trace of every element at each run. 

- ``Normalize Output`` (default value: True):
  The level of trace could be either integers or float number from 0 to 1. 

The model filename, output_trace_filename, and simulation scheme are required to provide by the users. Users could tune the above parameters by themselves as well. For example, this is a command for simulating a T cell model by setting 50 runs, 200 steps, simultaneously updating scheme.

.. code-block:: bash 

  python simulator_interface.py [T cell model filename] [output trace file] --sim_scheme sync --runs 50 --steps 200

Python code
~~~~~~~~~~~~~
Except for terminal interface, we also provide function for your script.
import simulator interface:

.. code-block:: Python

    import os
    import simulator_interface as sim

input your BioRECIPE model filename and output directory

.. code-block:: Python

    model = 'example/input/model.xlsx'
    output_dir = 'example/output/'

make your setups for simulation:

.. code-block:: Python

    steps = ..
    runs = ..
    scenarios = ['0', '1', '2', ...]
    output_format = 1 # all runs and frequency summaries
    scheme = 'ra' # random scheme

    # set up output paths
    if not os.path.exists(output_dir):
        os.mkdir(output_path)
    output_basename = os.path.join(output_path, 'example_traces_test')
    scenarios_sorted = [str(x) for x in scenarios]

Finally, your simulation are good to go! Summarize the setups in the function and run your script!:

.. code-block:: Python

    sim.setup_and_run_simulation(
        model_file,
        output_basename + '.txt',
        steps,
        runs.
        scheme,
        output_format,
        ','.join(scenarios_sorted))

For more information about Python API and visualization, please check our function `reference page <https://melody-dish.readthedocs.io/en/latest/Overview.html#method>`_.

