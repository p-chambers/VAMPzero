.. _discipline:

Discipline
==========

.. image:: discipline.jpg
   :width: 80%
   :align: center
   
Disciplines are implemented in VAMPzero implicitly by structuring the parameters within their
respective component. During the initialization of the code during runtime the discipline is found
from the folder structure of the code. 

For running splitted calculations it is possible to give a *disicipline* argument to the calc function
of a component. Only the defined discipline of this component and all its nested components will be calculated. 
