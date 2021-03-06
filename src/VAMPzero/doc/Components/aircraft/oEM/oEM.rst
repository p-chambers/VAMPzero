.. _aircraft.oEM:

Parameter: oEM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The max operating empty mass
    
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Mass.oEM.oEM.calc


   :Dependencies: 
   * :ref:`wing.mWing`
   * :ref:`htp.mHtp`
   * :ref:`vtp.mVtp`
   * :ref:`engine.mEngine`
   * :ref:`fuselage.mFuselage`
   * :ref:`aircraft.oIM`
   * :ref:`landingGear.mLandingGear`
   * :ref:`pylon.mPylon`
   * :ref:`systems.mSystems`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for oEM are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <massDescription>
                           <mass>

CPACS Export
-------------------
The values for oEM are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <massDescription>
                           <mass>

