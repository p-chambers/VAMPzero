.. _aircraft.wsTO:

Parameter: wsTO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The wing loading for take-off
    
    In aerodynamics, wing loading is the loaded weight of the aircraft divided 
    by the area of the wing. The faster an aircraft flies, the more lift is produced 
    by each unit area of wing, so a smaller wing can carry the same weight in 
    level flight, operating at a higher wing loading. Correspondingly, the landing 
    and take-off speeds will be higher. The high wing loading also decreases 
    maneuverability. The same constraints apply to birds and bats.
    
    :Unit: [kg/m2]
    :Wiki: http://en.wikipedia.org/wiki/Wing_loading 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Main.Sizing.wsTO.wsTO.calc


   :Dependencies: 
   * :ref:`aircraft.mTOM`
   * :ref:`aircraft.mLM`
   * :ref:`aircraft.wsL`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Sizing.wsTO.wsTO.calcmTOM


   :Dependencies: 
   * :ref:`aircraft.mTOM`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calcmTOM.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Sizing.wsTO.wsTO.calcwsL


   :Dependencies: 
   * :ref:`aircraft.mTOM`
   * :ref:`aircraft.mLM`
   * :ref:`aircraft.wsL`


   :Sensitivities: 
.. image:: calcwsL.jpg 
   :width: 80% 


