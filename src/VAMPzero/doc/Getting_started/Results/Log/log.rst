.. _logfile:

The Log File
============

.. note::

   There are two different types of logs in VAMPzero. During the execution print statements are shown in the **commandline** prompt. 
   This output is on **info** level meaning, that only some elementary processes are documented. In this way it easy to track what happens
   during the calculation run without looking at too much detail. 
   
   In the **VAMPzero.log** file the output is on **debug** level. There is a lot more information! This is mostly useful for developers or if
   you run into an error during the calculation. If you need to ask for help is probably best to attach the log file and send it to me.

VAMPzero documents most of its actions in a log. For the binary version of VAMPzero there is a fixed order of actions 
that will occur in the log. These include:

* **Header**
  
  Information about the current version and license. 

* **GUI Import**

  Information about the values retrieved from the graphical user interface. These include the values for a parameter as well as technology factors  

* **CPACS Import**

  After the values are imported from the graphical user interface VAMPzero will look for further information according to the CPACS schema in the *./ToolInput/toolInput.xml* file. 
  If there is any information available it will be imported. This means that values previously imported from the graphical user interface will be overwritten!

* **Input Listing**

  A list of all parameters with the status == fix is given. You can control whether the import routines were successful.   

* **Calculation**

  In this section the calculation run is logged. VAMPzero checks each parameter for convergence. Therefore an arbitrary number (max. 2000) iterations will be documented. 
  The check for convergence is made componentwise and converged components will be listed even if not all parameters are converged.
    
  .. warning::
     It is likely that errors will occur in this section! Overflow or value errors are a good indication that your calculation did not converge! 
  

* **Inits**

  A list of all parameters with the status == init is given. These parameters were not touched by any calculation method. In most cases this means 
  that there is not yet a calculation method for this parameter or it is a default value. 

* **Export of Mind Maps**

  For each parameter a mind map is generated. See :ref:`mindmap` for further information. 

* **Export to CPACS**

  The aircraft is exported to CPACS. See :ref:`knowledgebase` for further information
  
* **Check**

  All parameters in VAMPzero are linked via their calc methods. 
  If all parameters that are called by the calc 
  method of a parameter that is fixed are fixed as well this will produce a warning. 
    
  For example: If the reference area of the wing is fixed and the span and the aspect ratio 
  are fixed as well a warning will be given because the inputs may be inconsistent. 

* **Creating Plots**

  The plots are created. See :ref:`plot` for further information. 
  
  The payload range calculation will trigger another three calc runs don't get confused.  

* **Footer**
  
  The footer of VAMPzero and a guess on the runtime. 



   
     
