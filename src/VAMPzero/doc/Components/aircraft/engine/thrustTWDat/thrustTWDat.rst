.. _engine.thrustTWDat:

Parameter: thrustTWDat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Scaling factor for TWDat derived from current thrust00 in CPACS and current thrustTO from VAMPzero 	
    
    :Unit: [ ]
	
    .. todo::
	
       Move this one to Tool

    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Propulsion.thrustTWDat.thrustTWDat.calc


   :Dependencies: 
   * :ref:`engine.thrustTO`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Engine.Propulsion.thrustTWDat.thrustTWDat.cpacsImport

CPACS Export
-------------------
The values for thrustTWDat are exported to:

.. code-block:: xml

   <cpacs>
      <toolspecific>
         <tWDat>
            <thrust00Scaling>

