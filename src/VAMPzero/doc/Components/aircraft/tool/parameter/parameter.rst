.. _tool.parameter:

Parameter: parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **Superclass for all Parameters**
    
    A parameter holds the design knowledge in VAMPzero. All parameters in the model need to inherit this class.
    
    Each parameter holds several attributes: 
    
    * value
      
      The value of the parameter in the corresponding unit. 
      
    * factor
    
      Each parameter can hold a factor. These technology 
      factors can be used to 
      calibrate the calculation or introduce technologies 
      not directly modelled in VAMPzero.
      
    * unit
    
      The unit of the parameter. Although units can be arbitrary strings, VAMPzero tries to stick to SI-units.
      
    * status
    
      The status of a parameter influences the actions taken during the calculation. It can have different values: 
      
        * **fixed** by user input, may not be changed during the calculation 
        * *init* the parameter was not altered during the calculation
        * calc the parameter was calculated 
      
    * cpacsPath
    
      The cpacsPath is an optional attribute. If it is given value will be imported/exported to the respective location in CPACS. 
    
    For the methods of parameter see the following documentation. Please note that some of these routines maybe overwritten.  
    

Calculation Methods
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. automethod:: VAMPzero.Handler.Parameter.parameter.calc


CPACS Import
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
The values for parameter are imported from:

.. code-block:: xml

   <cpacs>
      <header>
         <version>

CPACS Export
-------------------
The values for parameter are exported to:

.. code-block:: xml

   <cpacs>
      <header>
         <version>

