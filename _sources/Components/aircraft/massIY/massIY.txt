.. _aircraft.massIY:

Parameter: massIY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The mass moment of inertia along the y-axis 
    
    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Inertia.massIY.massIY.calc


   :Dependencies: 
   * :ref:`fuselage.lfus`
   * :ref:`aircraft.mTOM`
   * :ref:`aircraft.oEM`
   * :ref:`fuel.mFM`


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
                     <designMasses>
                        <mTOM>
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
                     <designMasses>
                        <mTOM>
                           <massInertia>
                              <Jyy>

