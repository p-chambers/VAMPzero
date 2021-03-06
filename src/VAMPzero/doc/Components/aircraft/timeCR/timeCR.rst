.. _aircraft.timeCR:

Parameter: timeCR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The time during the cruise segment
    
    :Unit: [s] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Performance.timeCR.timeCR.calc


   :Dependencies: 
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.distCR`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Performance.timeCR.timeCR.calcFixFuel


   :Dependencies: 
   * :ref:`fuel.mFuelCLIMB`
   * :ref:`fuel.mFuelTO`
   * :ref:`fuel.mFuelCR`
   * :ref:`fuel.mFM`
   * :ref:`engine.sfcCR`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`atmosphere.qCR`
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.cD0`
   * :ref:`wing.cDw`
   * :ref:`wing.oswald`
   * :ref:`wing.refArea`
   * :ref:`wing.aspectRatio`


   :Sensitivities: 
.. image:: calcFixFuel.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Performance.timeCR.timeCR.calcFixRange


   :Dependencies: 
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.distCR`


   :Sensitivities: 
.. image:: calcFixRange.jpg 
   :width: 80% 


