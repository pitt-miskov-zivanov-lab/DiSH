############
Installation
############
DiSH requires local python compiler. To run the DiSH simulator, we recommand users to setup the virtual environment (Python version >3.6, <3.9) in the their computer. 

1. Clone the repository:

.. code-block:: bash

  mkdir DiSH
  git clone https://github.com/pitt-miskov-zivanov-lab/DiSH.git

2. Install the DiSH simulator:

.. code-block:: bash

  cd DiSH
  python setup.py install  

Users could also use pip to install:

.. code-block:: bash
  
  pip install -e .

3. To test the local DiSH, you could use the Bash command to run the example file:

.. code-block:: bash
  
  cd src
  python simulator_interface.py ~/.../DiSH/example/input/Tcell_N5_PTEN4_bio.xlsx ~/.../DiSH/example/output/trace.txt

after finishing simulation, output folder could get a trace text file if the installation is complete.
User also could use the Jupyter notebook we provide.

.. code-block:: bash
  
  jupyter notebook example/use_simulation.ipynb

