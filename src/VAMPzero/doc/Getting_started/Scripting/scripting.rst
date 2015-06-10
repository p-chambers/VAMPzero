.. _scripting

Scripting
=========

.. admonition:: If it comes with a GUI, it can't be science!!!
	
	This section will give some ideas on putting VAMPzero in a loop and use it for design studies


Depending on the version of VAMPzero you are working with there are
of course different ways to handle scripting. I will explain some simple approaches on how to do this both
for the binary and the source version. I am highly interested in any results that you could obtain (and of course all
the bugs that you found)

Binary Version
--------------

If you are unfamiliar with Python (it's a great language) you will prefer working with the binary version
of VAMPzero. I assume that you were already sucessful in downloading it and running some first calculations
with the GUI. The GUI is a very simple tool. It doesn't do anything else than creating the toolInput.xml file 
in the ToolInput folder and then runs VAMPzeroCPACS.exe. This is something you can do from any other tool as well. 

No matter what environment you are working in, be it Matlab or C++, by modifiying the toolInput.xml and executing VAMPzero
you can put VAMPzero in a loop easily. Results can either be obtained from the stdout or from a file called VAMPzero.res that
can be found in the folder ReturnDirectory.

If you are working from an engineering framework like RCE or ModelCenter toolInput.xml and VAMPzero.res are again the files 
that should be covered by your wrappers. You might as well conctact me, as I might have some wrappers at hand.  

Source Version
--------------

For the source version scripting can be quite simple. If you take a look into the VAMPzero.py  you are almost there. 
Putting values into VAMPzero is shown in the upper lines of code by executing something like::

   myAircaft.component.parameter.setValueFix(0.)

The one import line of code is then::

   myAircraft.calcAuto()

If you put the calcAuto routine into a loop or optimizer you are already there. Any values that you are interested in can be optained
by runnning a getValue() command on any parameter. 
