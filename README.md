# Fracktory3 5.1 setup file documentaion 

## step-by-step documentation on compiling , configuring and setting up  Fracktory3 5.1 setup file 

###Softwares figured out & used to compile and build the **Fracktory 5.1** software files to **setup.exe** file

### 1. [NSIS software](https://nsis.sourceforge.io/Download)
> The **NSIS** package includes a basic compiler interface. If you work frequently with NSIS scripts you might want to download a more complete development environment.

### 2. [Inno Setup](https://jrsoftware.org/isdl.php)
> **Inno Setup** is a free software script-driven installation system created by Jordan Russell.The installer has the ability to compare file version info, replace in-use files, use shared file counting, register DLL/OCXs and type libraries, and install fonts, Creation of shortcuts, including in the Start Menu and on the desktop

### 3. **[Install forge](https://installforge.net)** **(This is the software used to create setup file.exe)**
> **Install forge** has easy to use The wizard-driven interface allows you to create your installation packages without any scripting knowledge. All you need to do is to fill out the forms and attach the documents that you want the end-user to read. Building your own installation packages can be achieved with a few clicks only, making InstallForge a superior setup builder.

## Setting up the Install forge software
- The official download link for the Install forge software is here [Install Forge](https://installforge.net/download/)

- After it gets downloaded run the setup file i.e, executable .exe file 

- Go through the installation steps and finish the process

## Step-by-step procedure to create the setup.exe (Fracktory.exe ) setup file 

* Open the **Install Forge** software ,click on the new file or Ctrl + N to get the new file to setup

### There are 5 main sections

### General 
> In general tab there are 3 windows General , User Interfae , Languages 

#### General 

> This has sections
#### Production Information : 

- Product Name : Fracktory
- Product Version : 5.1
- Company Name : Fracktal Works
- Website URL : https://www.fracktal.in
- Support Operating systems : Supported all Windows Operating systems

- User Interface :

Wizard Image : located the image of our 3D printer from website in 162 X 300 pixel 
Header Image : located the logo

- Languages :enable the required languages

- Setup 

Files : located the files and folders individually 

Uninstallation : enabled include uninstaller 

> remaining are not needed in the section but can be used according to the requirements 

- Dialogs
splash screen not needed but play sound file  can be enabled for good installation experience & delay time can be mentioned as per the requirement (for this case I used 2 seconds)

- Licensce :

Enable Show License Agreement Dialog Box

>  GNU LESSER GENERAL PUBLIC LICENSE Version 3, 29 June 2007

```  Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.
  0. Additional Definitions.
  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.
  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.
  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.
  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".
  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.
  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.

This software is made available under the terms of *either* of the licenses
found in LICENSE.APACHE or LICENSE.BSD. Contributions to cryptography are made
under the terms of *both* these licenses.

The code used in the OS random engine is derived from CPython, and is licensed      

``` 



- Serial validation Not required for now can be enabled for the future requirements.

- Finish : Run Application   ``` < InstallPath > \ Fracktory.exe  ```

### System

- Registry : not needed for present requiremnts 

- ShortCuts :
> we can add desktop and start menu short cutsclick on ADD button a dialog box appears 
 - Destination : Desktop/ start menu
 
 - short cut Name : Fracktory 5.1 
 
 - Target File : ``` < InstallPath > \ Fracktory.exe ```
 
 - Icon file : locate the .ico file 
 
 # how to make **Icon file** (.ico) 
 
 > we can use [Gconvert 5 ](https://www.gdgsoft.com/gconvert/download) or [Resource Hacker](http://www.angusj.com/resourcehacker/) and can follow the steps in the mentioned [steps-to-setup icon to setupfile](https://www.wikihow.com/Change-the-Icon-for-an-Exe-File#:~:text=Select%20the%20current%20icon%20and,file%20browser%20window%20will%20expand.&text=Select%20your%20ICO%20file%20and,now%20see%20the%20replacement%20icon.)
 
 now add the location of the icon file to the dialog box argument 
 
 - can make the Icon index to required (in my case 1)
 
 
 


##Build
> This is the main step where we get the output as setup.exe file. 
- locate the setupfile location where you wanted it to be saved (**note**: not to the main.exe file (fracktory.exe) this will spoil the entire process (*in my case it happened 😅*)) 
-setup icon & uninstaller icon are to be located as per the custom requirements (cura-icon.ico)

- Compression : 
Compression method : Deflate ot LZMA
Compression Level : MAX






