.. _wing.aspectRatio:

Parameter: aspectRatio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    In aerodynamics, the aspect ratio of a wing is essentially the ratio of its length to its breadth (chord). 
    A high aspect ratio indicates long, narrow wings, whereas a low aspect ratio indicates short, stubby wings.
    For most wings the length of the chord is not a a constant but varies along the wing, so the aspect ratio AR 
    is defined as the square of the wingspan b divided by the area refArea of the wing planform - this is equal to 
    the length-to-breadth ratio for constant breadth.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Aspect_ratio_(wing) 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Geometry.aspectRatio.aspectRatio.calc


   :Dependencies: 
   * :ref:`wing.phi25`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Geometry.aspectRatio.aspectRatio.calcAirbus


   :Dependencies: 
   * :ref:`wing.phi25`


   :Sensitivities: 
.. image:: calcAirbus.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Wing.Geometry.aspectRatio.aspectRatio.calcDefinition


   :Dependencies: 
   * :ref:`wing.span`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calcDefinition.jpg 
   :width: 80% 


