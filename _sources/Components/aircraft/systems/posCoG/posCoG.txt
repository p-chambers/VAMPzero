.. _systems.posCoG:

Parameter: posCoG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    X Position of the center of gravity of the systems
	
    :Unit: [m]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Systems.CoG.posCoG.posCoG.calc


   :Dependencies: 
   * :ref:`fuselage.lfus`


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
                     <mOEM>
                        <mEM>
                           <mSystems>
                              <massDescription>
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
                     <mOEM>
                        <mEM>
                           <mSystems>
                              <massDescription>
                                 <location>
                                    <x>

