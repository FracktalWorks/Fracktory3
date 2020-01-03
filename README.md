# Fracktory3
Slicer for Fracktal Works 3D Printers, heavily optimized for dual extrusion and support material removal

## important Features:
1. Slow down on overhangs above certain angle
2. Slow down overhanging features over soluable support
3. Dynamic Prime Tower Volume calculation based on Nozzle size and Layer height
4. Optimised same material and dual material support settings


## Future Features/Ideas:
1. For same material support, keep support_z_dist=0 and lower the flow rate of the skin over the support, extra flow rate to compensate on the second skin to have consistant results across layer heights and nozzle diameters

## TODO:
1. Test Same material support for each nozzle x layer height x material
2. Test Soluable supports for each nozzle x layer height x material


## Utility to batch rename files:

https://github.com/vjvarada/FileRenamer
