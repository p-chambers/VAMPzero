.. _aircraft.loDLOI:

Parameter: loDLOI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The lift-over-drag ratio for loiter condition 

    In aerodynamics, the lift-to-drag ratio, or L/D 
    ratio ("ell-over-dee"), is the amount of lift generated 
    by a wing or vehicle, divided by the drag it creates by 
    moving through the air. 
    
    :Wiki: http://en.wikipedia.org/wiki/Lift-to-drag_ratio
    :Unit: [ ]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Aerodynamic.loDLOI.loDLOI.calc


   :Dependencies: 
   * :ref:`wing.aspectRatio`
   * :ref:`aircraft.cD0`
   * :ref:`aircraft.oswald`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


