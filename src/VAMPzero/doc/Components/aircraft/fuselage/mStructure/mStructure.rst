.. _fuselage.mStructure:

Parameter: mStructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The fuselage mass definition equals the Airbus weight chapter 11. The fuselage mass includes the complete fuselage structure, broken down as follows:
    
    * panels (skin shell panels, stringer, doubler, window frames)
    * frames (frames, pressure bulkheads, clips, frame junction fittings)
    * doors (doors, locking mechanism, hinge arm and fittings, door seal)
    * windscreens and windows
    * windscreen and opening frames
    * cabin floor structure
    * cargo compartment floor structure
    * special structures (landing gear bays, keel beam, VTP and HTP attachment, APU attachment)
    * fillet and fairings (belly fairing, leading edge root fillets, upper/lower wing fairing, APU fairing)
    * miscellaneous (external paint final coat, stairs, barrier wall, installation parts)
    
    The fuselage mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators are fixed are included into wing mass but not the bolts, that are used for fixing the actuator.
    
    The main differences between the DIN 9020 (which is normally used within LTH) and the Airbus defini-tion is that all wing-fuselage fairings, landing gear fittings and fittings of subsystems are accounted within the fuselage chapter. 
    The fuselage weight of Airbus aircraft is between 0% and 3.4% heavier according to the airbus weight chapter definition and the Fokker F100 is ~6% heavier.

    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuselage.Mass.mStructure.mStructure.calc


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Fuselage.Mass.mStructure.mStructure.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`fuselage.dfus`
   * :ref:`fuselage.lfus`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mStructure are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mStructure>
                              <mFuselagesStructure>
                                 <massDescription>
                                    <mass>

CPACS Export
-------------------
The values for mStructure are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mStructure>
                              <mFuselagesStructure>
                                 <massDescription>
                                    <mass>

