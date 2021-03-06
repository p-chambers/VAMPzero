.. _fuel.mFuelDESCENT:

Parameter: mFuelDESCENT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The fuel used in the descent segment
    
    :Unit: [kg] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelDESCENT.mFuelDESCENT.calc


   :Dependencies: 
   * :ref:`atmosphere.rhoCR`
   * :ref:`atmosphere.rhoFL1500`
   * :ref:`atmosphere.sigmaFL1500`
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.IASDESCENT`
   * :ref:`aircraft.timeDESCENT`
   * :ref:`aircraft.cD0`
   * :ref:`aircraft.oswald`
   * :ref:`wing.refArea`
   * :ref:`wing.aspectRatio`
   * :ref:`engine.sfcLOI`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`fuel.mFuelCLIMB`
   * :ref:`fuel.mFuelCR`
   * :ref:`fuel.mFuelTO`
   * :ref:`fuel.mFM`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


