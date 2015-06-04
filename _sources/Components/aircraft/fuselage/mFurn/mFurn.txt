.. _fuselage.mFurn:

Parameter: mFurn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The furnishings mass definition equals the Airbus weight chapter 50 to 54. 
    The furnishings mass includes the fixed part of the cabin and cargo arrangement, 
    the external decorative paint, the fixed oxygen, the internal and external 
    lighting and the water installation. Please note, that the formula below is developed 
    for typical passenger aircraft and not for aircraft having a pure business or 
    VIP cabin layout! The mass definition is broken down as follows:
    
    * furnishings

       * insulation
       * trim panels
       * crew seats and fixed crew rests
       * partitions, stowages, doors, monument lining
       * toilets
       * hatracks, bins
       * floor covering
       * cargo linings
       * cargo loading system
       * miscellaneous (door control panel, lifts, emergency ladder, external decorative paint)
       
    * emergency oxygen (in cockpit and cabin)
    * lighting (cockpit, cabin, service area, cargo, external and emergency lighting)
    * water installation (waste water, fresh water and toilet vacuum system; excluding the water itself)
    * liquid cooling (generation, distribution and branches)
    
    The furnishings masses exclude fittings on which they are fixed but include 
    the bolts that are used for fixing the furnishings.
    
    The mass definition between the Airbus accounting and the DIN 9020 
    (which is normally used within LTH) differs in detail. The furnishings weight 
    of the Fokker F100 is ~2% lower according to the DIN 9020 definition than according to the Airbus definition.
    
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuselage.Mass.mFurn.mFurn.calc


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuselage.Mass.mFurn.mFurn.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`
   * :ref:`payload.paxSeats`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mFurn are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mFurnishing>
                              <massDescription>
                                 <mass>

CPACS Export
-------------------
The values for mFurn are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mFurnishing>
                              <massDescription>
                                 <mass>

