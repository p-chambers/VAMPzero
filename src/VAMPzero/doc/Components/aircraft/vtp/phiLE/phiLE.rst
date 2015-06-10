.. _vtp.phiLE:

Parameter: phiLE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The angle of sweep which characterizes a swept wing is 
    conventionally measured along the 25% chord line. If 
    the 25% chord line varies in sweep angle, the leading edge is used; 
    if that varies, the sweep is expressed in sections (e.g., 25 degrees 
    from 0 to 50% span, 15 degrees from 50% to wingtip).
    
    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Swept_wing
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Geometry.phiLE.phiLE.calc


   :Dependencies: 
   * :ref:`vtp.aspectRatio`
   * :ref:`vtp.phi25`
   * :ref:`vtp.taperRatio`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


