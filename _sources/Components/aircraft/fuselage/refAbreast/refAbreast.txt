.. _fuselage.refAbreast:

Parameter: refAbreast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The reference number of pax abreast describing the layout of the cabin. 
    
    In a two-aisle aircraft with seven passengers abreast this may result in a value of 232,
    meaning that there are two passengers in the outer seatings and three in the middle  
    
    :Unit: [ ] 
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Fuselage.Cabin.refAbreast.refAbreast.calc


   :Dependencies: 
   * :ref:`fuselage.nPaxR`
   * :ref:`fuselage.nAisle`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


