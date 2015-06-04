.. _engine.massIZ:

Parameter: massIZ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Mass moment of inertia along the z-axis

    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Intertia.massIZ.massIZ.calc


   :Dependencies: 
   * :ref:`engine.mEngine`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for massIZ are imported from:

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
                                 <massInertia>
                                    <Jzz>

CPACS Export
-------------------
The values for massIZ are exported to:

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
                                 <massInertia>
                                    <Jzz>

