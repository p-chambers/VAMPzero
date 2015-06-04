.. _fuel.mFuelMAX:

Parameter: mFuelMAX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The maximum fuel mass that can be stored in the tanks
    
    :Unit: [kg] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelMAX.mFuelMAX.calc


   :Dependencies: 
   * :ref:`wing.taperRatio`
   * :ref:`wing.span`
   * :ref:`wing.cRoot`
   * :ref:`wingrootairfoil.tc`
   * :ref:`wingtipairfoil.tc`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelMAX.mFuelMAX.calcFLOPS


   :Dependencies: 
   * :ref:`wing.refArea`
   * :ref:`wing.taperRatio`
   * :ref:`wing.span`
   * :ref:`wing.tcAVG`


   :Sensitivities: 
.. image:: calcFLOPS.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelMAX.mFuelMAX.calcHeinze


   :Dependencies: 
   * :ref:`wing.taperRatio`
   * :ref:`wing.span`
   * :ref:`wing.cRoot`
   * :ref:`wingrootairfoil.tc`
   * :ref:`wingtipairfoil.tc`


   :Sensitivities: 
.. image:: calcHeinze.jpg 
   :width: 80% 


