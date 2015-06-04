.. _htp.reynoldsNr:

Parameter: reynoldsNr
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    In fluid mechanics, the Reynolds number Re is a dimensionless number 
    that gives a measure of the ratio of inertial forces to viscous forces 
    and consequently quantifies the relative importance of these two types 
    of forces for given flow conditions.    
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Reynolds_number   
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Aerodynamic.reynoldsNr.reynoldsNr.calc


   :Dependencies: 
   * :ref:`atmosphere.nyCR`
   * :ref:`atmosphere.TASCR`
   * :ref:`htp.cMAC`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


