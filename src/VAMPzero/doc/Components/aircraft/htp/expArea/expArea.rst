.. _htp.expArea:

Parameter: expArea
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The exposed area of the wing
    
    :Unit: [m2] 
    :Wiki: http://adg.stanford.edu/aa241/wingdesign/winggeometry.html
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Geometry.expArea.expArea.calc


   :Dependencies: 
   * :ref:`htp.refArea`
   * :ref:`htp.cRoot`
   * :ref:`fuselage.dfus`
   * :ref:`htp.phiLE`
   * :ref:`htp.phiTE`
   * :ref:`htp.zRoot`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


