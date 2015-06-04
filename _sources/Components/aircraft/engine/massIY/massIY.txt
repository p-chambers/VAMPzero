.. _engine.massIY:

Parameter: massIY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The mass moment of inertia along the y-axis

    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Intertia.massIY.massIY.calc


   :Dependencies: 
   * :ref:`engine.mEngine`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for massIY are imported from:

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
                                    <Jyy>

CPACS Export
-------------------
The values for massIY are exported to:

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
                                    <Jyy>

