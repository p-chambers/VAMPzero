.. _engine.dEngine:

Parameter: dEngine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The outer diameter of the engine. For simplification this also included the nacelle. 
    
    :Unit: [m]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Geometry.dEngine.dEngine.calc


   :Dependencies: 
   * :ref:`engine.thrustTO`
   * :ref:`engine.bypassRatio`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Engine.Geometry.dEngine.dEngine.calcEU


   :Dependencies: 
   * :ref:`engine.bypassRatio`
   * :ref:`engine.OPR`
   * :ref:`engine.thrustCR`


   :Sensitivities: 
.. image:: calcEU.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for dEngine are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <engines>
            <engine>
               <geometry>
                  <diameter>

CPACS Export
-------------------
The values for dEngine are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <engines>
            <engine>
               <geometry>
                  <diameter>

