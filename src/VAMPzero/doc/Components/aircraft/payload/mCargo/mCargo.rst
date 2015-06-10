.. _payload.mCargo:

Parameter: mCargo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The mass of additional cargo
    
    :Unit: [kg] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Payload.Mass.mCargo.mCargo.calc


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mCargo are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <payload>
                        <mCargo>
                           <massDescription>
                              <mass>

CPACS Export
-------------------
The values for mCargo are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <payload>
                        <mCargo>
                           <massDescription>
                              <mass>

