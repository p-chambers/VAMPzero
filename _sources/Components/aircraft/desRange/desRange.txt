.. _aircraft.desRange:

Parameter: desRange
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The design range for the aircraft. 
    
    This is the range that will be used together with the specified payload to size the aircraft.
    
    :Unit: [m] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Performance.desRange.desRange.calc


   :Dependencies: 
   * :ref:`aircraft.distCLIMB`
   * :ref:`aircraft.distDESCENT`
   * :ref:`aircraft.distCR`
   * :ref:`aircraft.distRES`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Performance.desRange.desRange.calcBreguet


   :Dependencies: 
   * :ref:`atmosphere.TASCR`
   * :ref:`aircraft.loDCR`
   * :ref:`engine.sfcCR`
   * :ref:`aircraft.oEM`
   * :ref:`payload.mPayload`
   * :ref:`fuel.mFM`
   * :ref:`aircraft.timeRES`
   * :ref:`aircraft.loDLOI`
   * :ref:`engine.sfcLOI`


   :Sensitivities: 
.. image:: calcBreguet.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Performance.desRange.desRange.calcSum


   :Dependencies: 
   * :ref:`aircraft.distCLIMB`
   * :ref:`aircraft.distDESCENT`
   * :ref:`aircraft.distCR`
   * :ref:`aircraft.distRES`


   :Sensitivities: 
.. image:: calcSum.jpg 
   :width: 80% 


