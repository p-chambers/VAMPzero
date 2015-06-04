.. _systems.mSystems:

Parameter: mSystems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The systems mass definition, which is used in this paper, equals the Airbus weight 
    chapter 30 to 42. The system mass includes all following systems:
    
    * auxiliary power unit (APU)
    * hydraulic generation
    * hydraulic distribution
    * air conditioning (generation, distribution, ventilation, pressure control)
    * de-icing and anti-icing (at wing, tail, air intake, windscreen and propellers)
    * fire protection (engine, APU, cargo and landing gear bay fire protection, smoke detection)
    * flight controls (incl. mechanical flight controls (e.g. actuators) and cockpit control mechanisms; excl. cables, electrical control and monitoring items)
    * instrument panels (in the cockpit)
    * automatic flight system
    * navigation (incl. cables, brackets semi-equipment and mountings)
    * communication (incl. cables, brackets semi-equipment and mountings)
    * electrical generation
    * electrical distribution
    
    The system masses exclude fittings on which they are fixed but include the bolts that are used for fixing the systems.
    
    The mass definition between the Airbus accounting and the DIN 9020 (which is normally used within LTH) differs in several points. 
    As first approximation the system mass of the Airbus accounting equals the sum of the following DIN 9020 groups:

    * surface control
    * auxiliary power
    * instruments
    * hydraulic and pneumatic
    * electrical 
    * electronical
    * air-condition and anti-icing (without the bleed air system, which is accounted for in *power units* according to Airbus definition)
    
    Using this approach the difference between both accounting systems is 1.5% for 
    the Fokker F100. Please note, that several detailed differences are not considered in this approach.

    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Systems.Mass.mSystems.mSystems.calc


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Systems.Mass.mSystems.mSystems.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`
   * :ref:`aircraft.mTOM`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mSystems are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mSystems>
                              <massDescription>
                                 <mass>

CPACS Export
-------------------
The values for mSystems are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mSystems>
                              <massDescription>
                                 <mass>

