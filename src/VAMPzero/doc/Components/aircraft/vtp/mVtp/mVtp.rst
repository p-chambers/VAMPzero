.. _vtp.mVtp:

Parameter: mVtp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The vertical tail plane (VTP) mass definition equals the Airbus weight chapter 14. 
    The VTP mass includes the complete VTP structure, broken down as follows:
    
    * torsion box (skins, spars, ribs, sealants, fuselage attachment)
    * leading edge (dorsal fin, skins, ribs, panes)
    * fixed trailing edge (panels, ribs, hinge and actuator fittings)
    * rudders (complete rudder body, hinge and actuator fittings)
    * tips and fairings (tips, fairing supports and fairings)
    * miscellaneous (external paint final coat, VTP-fuselage bolts, torsion box-leading edge and torsion box-trailing edge bolts )
    
    The VTP mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators 
    are fixed are included into wing mass but not the bolts that are used for fixing the actuator.
    
    The difference between the DIN 9020 (which is normally used within LTH) and the Airbus 
    definition is small. In the DIN 9020 definition actuator fittings are excluded in the VTP 
    structure weight but therefore flutter dampers are included into the VTP structural weight. 
    The VTP weight difference of the Fokker F100 is <2% between the two weight breakdowns.

    :Unit: [kg]
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Vtp.Mass.mVtp.mVtp.calc


   :Dependencies: 
   * :ref:`vtp.refArea`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 


.. automethod:: VAMPzero.Component.Vtp.Mass.mVtp.mVtp.calcDorbathPraktikum


   :Dependencies: 
   * :ref:`vtp.refArea`


   :Sensitivities: 
.. image:: calcDorbathPraktikum.jpg 
   :width: 80% 


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for mVtp are imported from:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mStructure>
                              <mWingsStructure>
                                 <mWingStructure[3]>
                                    <massDescription>
                                       <mass>

CPACS Export
-------------------
The values for mVtp are exported to:

.. code-block:: xml

   <cpacs>
      <vehicles>
         <aircraft>
            <model>
               <analyses>
                  <massBreakdown>
                     <mOEM>
                        <mEM>
                           <mStructure>
                              <mWingsStructure>
                                 <mWingStructure[3]>
                                    <massDescription>
                                       <mass>

