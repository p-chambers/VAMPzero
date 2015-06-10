.. _payload.paxSeats:

Parameter: paxSeats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The max number of available Seats depending on the class layout
    
    :Unit: [ ] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Payload.Mass.paxSeats.paxSeats.calc


   :Dependencies: 
   * :ref:`aircraft.rangeType`
   * :ref:`fuselage.lcabin`
   * :ref:`fuselage.nPaxR`
   * :ref:`fuselage.nClasses`
   * :ref:`fuselage.dfus`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for paxSeats are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <global>
                  <paxSeats>

CPACS Export
-------------------
The values for paxSeats are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <global>
                  <paxSeats>

