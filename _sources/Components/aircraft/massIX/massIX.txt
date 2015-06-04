.. _aircraft.massIX:

Parameter: massIX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The mass moment of inertia along the x-axis 
    
    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Inertia.massIX.massIX.calc


   :Dependencies: 
   * :ref:`wing.span`
   * :ref:`aircraft.mTOM`
   * :ref:`aircraft.oEM`
   * :ref:`fuel.mFM`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for massIX are imported from:

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
                              <Jxx>

CPACS Export
-------------------
The values for massIX are exported to:

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
                              <Jxx>

