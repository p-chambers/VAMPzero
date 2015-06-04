.. _aircraft.costMisc:

Parameter: costMisc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The miscellaneous costs per block hour
    
    :Unit: [EU/bh]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.DOC.costMisc.costMisc.calc


   :Dependencies: 
   * :ref:`aircraft.PriceAircraft`
   * :ref:`engine.PriceEngine`
   * :ref:`engine.nEngine`
   * :ref:`aircraft.USDexchangeEURO`
   * :ref:`aircraft.tBlock`
   * :ref:`aircraft.desRange`
   * :ref:`aircraft.mLM`
   * :ref:`aircraft.mTOM`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


