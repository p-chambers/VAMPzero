.. _aircraft.posCoG:

Parameter: posCoG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The x position of the center of gravity of the aircraft
    
    :Unit: [m]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.CoG.posCoG.posCoG.calc


   :Dependencies: 
   * :ref:`aircraft.mTOM`
   * :ref:`pylon.mPylon`
   * :ref:`systems.mSystems`
   * :ref:`landingGear.mLandingGear`
   * :ref:`wing.xMAC`
   * :ref:`wing.cMAC`
   * :ref:`engine.posCoG`
   * :ref:`engine.mEngine`
   * :ref:`wing.posCoG`
   * :ref:`wing.mWing`
   * :ref:`htp.posCoG`
   * :ref:`htp.mHtp`
   * :ref:`vtp.posCoG`
   * :ref:`vtp.mVtp`
   * :ref:`fuselage.posCoG`
   * :ref:`fuselage.mFuselage`
   * :ref:`systems.posCoG`
   * :ref:`fuel.mFM`
   * :ref:`payload.posCoG`
   * :ref:`payload.mPayload`
   * :ref:`aircraft.oIM`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for posCoG are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <designMasses>
                        <mTOM>
                           <location>
                              <x>

CPACS Export
-------------------
The values for posCoG are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <designMasses>
                        <mTOM>
                           <location>
                              <x>

