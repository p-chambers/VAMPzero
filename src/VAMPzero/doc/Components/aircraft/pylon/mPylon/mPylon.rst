.. _pylon.mPylon:

Parameter: mPylon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The under wing engine pylon mass definition equals the Airbus weight chapter 16. The 
    pylon mass includes the complete pylon structure between the wing and 
    the removable power plant, broken down as follows:
    
    * primary structure
    
       * pylon box (ribs, spars, upper and lower panel, stringers, access doors)
       * forward and rear engine mount (mount fittings, link assy , pin, nut, bearing, thrust rod)
       * forward and rear wing interfaces (link assy, pin, bearing, nut)
       * spigot fittings, fixed support, spar splice
    
    *    secondary structure
    
       * fairings, fairing ribs, sealant, external paint final coat, firewalls, soft mounts
    
    The pylon mass excludes systems (e.g. actuators) but fittings on which e.g. 
    the actuators are fixed are included into the pylon mass but not the 
    bolts that are used for fixing the actuator.
    
    The main difference between the DIN 9020 (which is normally used within LTH) 
    and the Airbus definition is, that pylons and nacelles are accounted within 
    the chapter *nacelle and engine installation* in DIN 9020, while the engine 
    nacelle is accounted within the equipped engine weight (Ch. 20) according to the Airbus accounting.
    
    For the Fokker F100, the pylon mass (according to the Airbus 
    definition) is ~28% of the *nacelle and engine installation* -mass of the 
    DIN 9020 accounting. Pleas note, that the fuselage pylon mass of the F100 is nameable lighter, compared with an under wing pylon.
    
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Pylon.Mass.mPylon.mPylon.calc


   :Dependencies: 
   * :ref:`engine.nEngine`
   * :ref:`engine.thrustTO`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Pylon.Mass.mPylon.mPylon.calcBoxBeam


   :Dependencies: 
   * :ref:`engine.nEngine`
   * :ref:`engine.thrustTO`


   :Sensitivities: 
.. image:: calcBoxBeam.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Pylon.Mass.mPylon.mPylon.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`engine.mEngine`
   * :ref:`aircraft.mTOM`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Pylon.Mass.mPylon.mPylon.calcDragStrut


   :Dependencies: 
   * :ref:`engine.nEngine`
   * :ref:`engine.thrustTO`


   :Sensitivities: 
.. image:: calcDragStrut.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mPylon are imported from:

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
                              <mPylons>
                                 <massDescription>
                                    <mass>

CPACS Export
-------------------
The values for mPylon are exported to:

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
                              <mPylons>
                                 <massDescription>
                                    <mass>

