.. _fuselage.nAisle:

Parameter: nAisle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The number of aisles in the cabin.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Wide-body_aircraft
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuselage.Cabin.nAisle.nAisle.calc


   :Dependencies: 
   * :ref:`payload.paxSeats`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuselage.Cabin.nAisle.nAisle.calcDfus


   :Dependencies: 
   * :ref:`fuselage.dfus`


   :Sensitivities: 
.. image:: calcDfus.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuselage.Cabin.nAisle.nAisle.calcPax


   :Dependencies: 
   * :ref:`payload.paxSeats`


   :Sensitivities: 
.. image:: calcPax.jpg 
   :width: 80% 


