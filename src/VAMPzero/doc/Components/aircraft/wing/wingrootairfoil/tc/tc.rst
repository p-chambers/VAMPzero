.. _wingrootairfoil.tc:

Parameter: tc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The thickness to chord ratio of the airfoil. Default value is set to 0.1
    
    :Unit: [ ]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Airfoil.Aerodynamic.tc.tc.calc


   :Dependencies: 
   * :ref:`wing.tcAVG`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Airfoil.Aerodynamic.tc.tc.calcWingRootTC


   :Dependencies: 
   * :ref:`wing.tcAVG`


   :Sensitivities: 
.. image:: calcWingRootTC.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Airfoil.Aerodynamic.tc.tc.calcWingTipTC


   :Dependencies: 
   * :ref:`wing.tcAVG`


   :Sensitivities: 
.. image:: calcWingTipTC.jpg 
   :width: 80% 


