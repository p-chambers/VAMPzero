.. _aircraft.oIM:

Parameter: oIM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The operator's mass definition equals the Airbus weight 
    chapter 60 and 61. The operator's items mass includes the removable part of 
    the cabin arrangement, the emergency equipment, catering, fluids aircraft 
    documents, tool kit and the crew. Please note, that the formula below is developed 
    for typical passenger aircraft and not for aircraft having a pure business 
    or VIP cabin layout! The mass definition is broken down as follows:
    
    * standard items

       * unusable fuel
       * A/C documents and tool kit
       * galley structure
       * passenger seats
       * removable crew rest
       * additional center tank (in the cargo compartment)
       * seat mounted electronical system (in-flight entertainment)
       
    * operational items 

       * emergency equipment 
       * water for galleys and toilets (incl. the water in the tanks)
       * fluid for toilets (waste tank precharge)
       * (usable) engine and APU oil
       * catering
       * crew
    
    The mass definition between the Airbus accounting and the 
    DIN 9020 (which is normally used within LTH) is similar to 
    the sum of the DIN9020 chapters 40, 18 and 20, but 
    differs in several points. The operators items weight 
    of the Fokker F100 is ~4.5% higher according to the DIN 
    9020 definition than according to the Airbus definition.

    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Mass.oIM.oIM.calc


   :Dependencies: 
   * :ref:`payload.paxSeats`
   * :ref:`fuselage.nClasses`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Mass.oIM.oIM.calcDorbath


   :Dependencies: 
   * :ref:`payload.paxSeats`
   * :ref:`aircraft.rangeType`


   :Sensitivities: 
.. image:: calcDorbath.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for oIM are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mOperatorItems>
                           <massDescription>
                              <mass>

CPACS Export
-------------------
The values for oIM are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mOperatorItems>
                           <massDescription>
                              <mass>

