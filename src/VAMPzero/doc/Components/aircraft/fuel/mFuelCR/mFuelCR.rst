.. _fuel.mFuelCR:

Parameter: mFuelCR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The fuel used in the cruise segment
    
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelCR.mFuelCR.calc


   :Dependencies: 
   * :ref:`fuel.mFuelCLIMB`
   * :ref:`fuel.mFuelTO`
   * :ref:`fuel.mFM`
   * :ref:`aircraft.distCR`
   * :ref:`engine.sfcCR`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`atmosphere.qCR`
   * :ref:`atmosphere.TASCR`
   * :ref:`wing.cDw`
   * :ref:`aircraft.cD0`
   * :ref:`aircraft.oswald`
   * :ref:`wing.refArea`
   * :ref:`wing.aspectRatio`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelCR.mFuelCR.calcFixFuel


   :Dependencies: 
   * :ref:`fuel.mFuelCLIMB`
   * :ref:`fuel.mFuelTO`
   * :ref:`fuel.mFuelRES`
   * :ref:`fuel.mFuelDESCENT`
   * :ref:`fuel.mFM`


   :Sensitivities: 
.. image:: calcFixFuel.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelCR.mFuelCR.calcFixRange


   :Dependencies: 
   * :ref:`fuel.mFuelCLIMB`
   * :ref:`fuel.mFuelTO`
   * :ref:`fuel.mFM`
   * :ref:`aircraft.distCR`
   * :ref:`engine.sfcCR`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`atmosphere.qCR`
   * :ref:`atmosphere.TASCR`
   * :ref:`wing.cDw`
   * :ref:`aircraft.cD0`
   * :ref:`aircraft.oswald`
   * :ref:`wing.refArea`
   * :ref:`wing.aspectRatio`


   :Sensitivities: 
.. image:: calcFixRange.jpg 
   :width: 80% 


