.. _sensitivities:


The Sensitivities
=================

At the end of a calculation run, VAMPzero calculates the sensitivities for each parameter. To derive these
results each parameter is recalculated for a change in the imaginary part of its callers values. This is called complex 
step derivative approximation. 

.. note:: 
   
   A well written introduction and some references to complex-step approximation can be found on
   the University of Toronto - Multidisciplinary Optimization Laboratory homepage
   
   http://mdolab.utias.utoronto.ca/resources/complex-step   	
   
The results of the complex step approximation are shown in form of barplots. The barplot always shows the change 
of a parameter relative to change of one of its callees. Below an example for the wing mass is shown.  

Example: Sensitivity for the wing mass 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Component.Wing.Mass.mWing.mWing.calc


   :Dependencies: 
   * :ref:`wing.phi25`
   * :ref:`wing.aspectRatio`
   * :ref:`wing.tcAVG`
   * :ref:`aircraft.mTOM`
   * :ref:`wing.refArea`


   :Sensitivities: 
.. image:: calc.jpg 
   :width: 80% 
 
Each bar shows the change for the wing mass depending on the parameters change. Blue indicates 
that the parameter was increased, red means that the parameter was decreased. In this example this implies
that for a positive change in the wing's reference area the wing mass increases. The same tendency is true for the 
maximum takeoff mass, the aspect ratio and the quarter-chord sweep. Nevertheless, the wing mass reacts more or less
sensitive to these inputs. For the thickness to chord ratio the tendency is mirrored. For a thicker (i.e. greater t/c)
wing we get less wing mass as the thickness of the spars also increases   