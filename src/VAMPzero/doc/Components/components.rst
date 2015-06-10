.. _documentation:


**************
Documentation
**************

A component is the highest level class in VAMPzero. 
A :ref:`component` will hold several disciplines, where as each :ref:`discipline` is then 
grouped into different parameters. 
Components and disciplines are mostly used for the management of the code. 
The design knowledge itself is captured in the respective :ref:`parameter`. If you want to 
have an overview on all design knowledge used in VAMPzero you can go to the :ref:`sources` section. 
For the export to CPACS, components (e.g. wing) can hold additional methods

.. image:: structure.jpg
   :width: 80%
   :align: center
   
The aircraft is the top level class. It holds several disciplines and nested 
components. You will find an overview on the following pages. 

.. toctree::
   :maxdepth: 1
   
   Aircraft<aircraft/aircraft>
