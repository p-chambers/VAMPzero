.. _engine.thrustCR:

Parameter: thrustCR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Thrust per engine at the beginning of the cruise segment
	
    :Unit: [N]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Propulsion.thrustCR.thrustCR.calc


   :Dependencies: 
   * :ref:`aircraft.loDCR`
   * :ref:`engine.nEngine`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`fuel.mFM`
   * :ref:`fuel.mFuelCLIMB`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


