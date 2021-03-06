.. _aircraft.wsL:

Parameter: wsL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The wing loading for the landing
    
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
.. automethod:: VAMPzero.Component.Main.Sizing.wsL.wsL.calc


   :Dependencies: 
   * :ref:`aircraft.sLFL`
   * :ref:`aircraft.cLL`
   * :ref:`atmosphere.rhoAP`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Sizing.wsL.wsL.calcSizing


   :Dependencies: 
   * :ref:`aircraft.sLFL`
   * :ref:`aircraft.cLL`
   * :ref:`atmosphere.rhoAP`


   :Sensitivities: 
.. image:: calcSizing.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Main.Sizing.wsL.wsL.calcWsTO


   :Dependencies: 
   * :ref:`aircraft.mTOM`
   * :ref:`aircraft.mLM`
   * :ref:`aircraft.wsTO`


   :Sensitivities: 
.. image:: calcWsTO.jpg 
   :width: 80% 


