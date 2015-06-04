.. _aircraft.costDepreciation:

Parameter: costDepreciation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The depreciation costs per flight hour
    
    :Unit: [EU/h]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.DOC.costDepreciation.costDepreciation.calc


   :Dependencies: 
   * :ref:`aircraft.priceAircraft`
   * :ref:`aircraft.tFlight`
   * :ref:`aircraft.tBlock`
   * :ref:`aircraft.utilization`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.DOC.costDepreciation.costDepreciation.calcKundu


   :Dependencies: 
   * :ref:`aircraft.priceAircraft`
   * :ref:`aircraft.utilization`
   * :ref:`aircraft.USDexchangeEURO`


   :Sensitivities: 
.. image:: calcKundu.jpg 
   :width: 80% 


