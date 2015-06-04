.. _aircraft.mTOM:

Parameter: mTOM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The maximum take-off mass for the aircraft
    
    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Mass.mTOM.mTOM.calc


   :Dependencies: 
   * :ref:`aircraft.oEM`
   * :ref:`fuel.mFM`
   * :ref:`payload.mPayload`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mTOM are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <designMasses>
                        <mTOM>
                           <mass>

CPACS Export
-------------------
The values for mTOM are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <designMasses>
                        <mTOM>
                           <mass>

