### Hey ho!

A ray-tracer written entirely in python with entirely no other dependencies.

![some demo image](imgs/image.png)


Actually, it's deploying *sphere-tracing*, or *ray-marching* as it's
called in the *[shadertoy](https://www.shadertoy.com/) community*, where
a [signed distance field](https://en.wikipedia.org/wiki/Signed_distance_function) 
is calculated for the whole scene and the ray does incremental 
steps to reach a surface. The method got incredibly famous through
availability of programmable graphic cards and the 
[articles](https://iquilezles.org/www/index.htm) and work of Inigo Quilez.
At least that's what fans of him tend to think. 

I'm running this with [pypy](https://www.pypy.org/) and it's still super
slow. Above image (512² * 2² sub-sampling) took about 10 minutes or so.

A lot of bugs are lurking in the corners and they are not rendered with 
fancy glow or anything...

Actually i just followed a Friday's thought that one could do ray-tracing 
with python *generators* and building some 
[ambient occlusion](https://en.wikipedia.org/wiki/Ambient_occlusion) 
matrix while collecting and issuing new rays. 

Soon recovered that ... yes, there where a couple of complicated layers 
until there is a decent ray-tracer. Vector algebra, scene management,
light sources, reflection and transparency, necessary optimization tricks. 
No generator hacking so far...
