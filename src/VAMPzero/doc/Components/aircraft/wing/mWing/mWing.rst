.. _wing.mWing:

Parameter: mWing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The wing mass definition equals the Airbus weight chapter 10. The wing mass includes the complete wing structure
    from tip to tip including centre wing box, broken down as follows:

    * skins (including stringers)
    * spars
    * ribs
    * pylon attachments (front and rear attachment, fairing attachments, spigot attachment)
    * landing gear support (gear beam and ribs, attachments and fittings)
    * fixed leading edge (ribs, panels, movable support structures)
    * movable leading edge (slat, droop nose, krueger flaps, slat tracks)
    * fixed trailing edges (panels, falsework, flap tracks and attachments, spoiler and aileron support)
    * movable trailing edges (flaps including flap track rear link and carriages, ailerons and spoiler)
    * miscellaneous (external paint final coat, wing tips, winglets, sealant, fairings, fittings and supports)

    The wing mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators are fixed are included
    into wing mass but not the bolts, that are used for fixing the actuator.

    The main differences between the DIN 9020 (which is normally used within LTH) and the Airbus definition is
    that the wing-fuselage (belly) fairing as well as the landing gear doors in the belly fairing area is not
    accounted within the wing chapter. On the other hand the tank sealant, wing landing gear and pylon fittings and
    fittings of subsystems is accounted within the wing chapter.
    The wing weight of Airbus aircraft is ~1% lighter according to the Airbus weight chapter definition and
    the Fokker F100 is ~2% heavier.

    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calc


   :Dependencies: 
   * :ref:`wing.phi25`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.tcAVG`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`wing.phi25`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.tcAVG`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcEureqa


   :Dependencies: 
   * :ref:`wing.phi25`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.tcAVG`
   * :ref:`wing.taperRatio`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calcEureqa.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcRaymer


   :Dependencies: 
   * :ref:`wing.refArea`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.tcAVG`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.phi25`
   * :ref:`wing.taperRatio`


   :Sensitivities: 
.. image:: calcRaymer.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcShevell


   :Dependencies: 
   * :ref:`wing.refArea`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.tcAVG`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.phi50`
   * :ref:`wing.taperRatio`
   * :ref:`aircraft.mZFW`


   :Sensitivities: 
.. image:: calcShevell.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcToreenbeek


   :Dependencies: 
   * :ref:`wing.refArea`
   * :ref:`wing.tcAVG`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.phi50`
   * :ref:`aircraft.mZFW`


   :Sensitivities: 
.. image:: calcToreenbeek.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calcXX


   :Dependencies: 
   * :ref:`wing.refArea`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.tcAVG`
   * :ref:`wing.span`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.phi25`
   * :ref:`wing.taperRatio`
   * :ref:`fuel.mFM`
   * :ref:`engine.mEngine`
   * :ref:`engine.yEngine`



CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.cpacsImport

CPACS Export
-------------------
The values for mWing are exported to:

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
                              <mWingsStructure>
                                 <mWingStructure[1]>
                                    <massDescription>
                                       <mass>

