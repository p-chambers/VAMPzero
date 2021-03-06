.. _engine.mEngine:

Parameter: mEngine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The power unit mass definition equals the Airbus weight chapter 20 to 26. The power unit mass 
    includes: engines, nacelles, all systems included in the 
    removable power plant, and residual fluids hydraulic, 
    trapped fuel and oil in lines (not oil in tanks). Also included are aircraft systems 
    associated with engines: engine controls, bleed air and fuel systems. In detail it is broken down as follows:
    
    * equipped engines (complete removable power plant; w/o engine tank oil and electrical generators oil)
    
       * basic engine in manufacturer delivery configuration
       * nacelle structure (inlet cowls, fan cowls, nozzles, centerbody, reversers and engine mounts, ex-ternal paint final coat)
       * nacelle systems (all systems located within the nacelle)
    
    * bleed air system (in pylons, wing and fuselage)
    * engine control system (in pylons, wing and fuselage)
    * fuel system (incl. pipes, couplings, removable brackets, control and monitoring equipment, semi-equipment and their installations; excl. cables, electrical control and monitoring items)
    * inert gas system (incl. inert gas generation, storage, distribution, generation control and generation indicating systems)
    
    The system masses exclude fittings on which they are fixed but include the bolds that are used for fixing the systems.
    
    The mass definition between the Airbus accounting and the DIN 9020 
    (which is normally used within LTH) differs in several points. Differing with 
    the Airbus accounting the DIN 9020 group *propulsion* includes:
    
    * the tank sealant
    * unusable fuel in tanks
    
    and excludes: 
    
    * the engine nacelle structure and engine nacelle systems
    * the bleed air system

	
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Mass.mEngine.mEngine.calc


   :Dependencies: 
   * :ref:`engine.nEngine`
   * :ref:`engine.thrustTO`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Engine.Mass.mEngine.mEngine.calcDorbath


   :Dependencies: 
   * :ref:`engine.thrustTO`
   * :ref:`engine.bypassRatio`
   * :ref:`engine.nEngine`


   :Sensitivities: 
.. image:: calcDorbath.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mEngine are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mPowerUnits>
                              <massDescription>
                                 <mass>

CPACS Export
-------------------
The values for mEngine are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mPowerUnits>
                              <massDescription>
                                 <mass>

