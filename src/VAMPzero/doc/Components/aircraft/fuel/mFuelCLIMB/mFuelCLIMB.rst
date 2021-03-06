.. _fuel.mFuelCLIMB:

Parameter: mFuelCLIMB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The fuel used in the climb segment
    
    :Unit: [kg] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuel.Mass.mFuelCLIMB.mFuelCLIMB.calc


   :Dependencies: 
   * :ref:`atmosphere.rhoCR`
   * :ref:`atmosphere.rhoFL1500`
   * :ref:`atmosphere.sigmaFL1500`
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.IASCLIMB`
   * :ref:`aircraft.timeCLIMB`
   * :ref:`aircraft.gammaCLIMB`
   * :ref:`aircraft.cD0`
   * :ref:`aircraft.oswald`
   * :ref:`wing.refArea`
   * :ref:`wing.aspectRatio`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`fuel.mFM`
   * :ref:`fuel.mFuelTO`



