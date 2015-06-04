.. _wing.formFactor:

Parameter: formFactor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The form factor for the wing
    
    The parasite drag associated with skin friction and pressure drag is determined 
    by incrementing the flat plate results by a factor, to account for 
    pressure drag and the higher-than-freestream surface velocities:

    :Unit: [ ]
    :Wiki: http://adg.stanford.edu/aa241/drag/formfactor.html     
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Aerodynamic.formFactor.formFactor.calc


   :Dependencies: 
   * :ref:`aircraft.machCR`
   * :ref:`wing.tcAVG`
   * :ref:`wingrootairfoil.ctm`
   * :ref:`wing.phi25`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


