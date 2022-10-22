import cadquery as cq
from cadquery import exporters
#####
#
# Cup-Ganizer
# parametric semi complex cup generator
#
#####

# adjust either the multiplier or the base value
h_w=80 # 80 is just about right (most of time)
h_l=110*2 # 1 is compact, 2 is still printable (no brim, no skirt)
h_h=30*2 # 2 is deep, 3 is very deep, 1 is nice shallow

# how thick the walls need be (1-2 mm)
offset=1.5

#number of smaller cups (how many times to split one half)
cups=4

#buttom radius 
#(for getting out small parts with a figer from the bottom)
cup_bottom_radius=((h_w/2)-offset*3)/6

#the vertical edge radius
overal_edge_radius=2

### past here you're on your own - varranty's void:
rotation = 90


#small cup dimensions
c_x=h_w/2-offset*2
c_y=((h_l-offset*2)/(cups*2))-offset
c_z=h_h-1.5

#cup hole(s)
cup=cq.Workplane("front",origin=(0,0,h_h/2+(h_h-c_z)/2))
# reuse small cup's workplane
cupXX=cup.box((offset+c_x)*2,h_l/2-offset*3,c_z)
#filet the outer bottom edges
cupXX=cupXX.edges('<Z and |Y').fillet(offset*cup_bottom_radius)

#smaller cup hole
cup=cup.box(c_x,c_y,c_z)
#pre rotate for array placement
cup=cup.rotate([0,0,0],[0,0,1],rotation)
#fillet the "front" edges (will get rotated outward)
cup=cup.edges('<Z and <Y').fillet(offset*cup_bottom_radius)

#holder body
holder=cq.Workplane("front",origin=(0,0,0))
holder=holder.box(h_w,h_l,h_h)
#rise it to the zero plane
holder=holder.translate([0,0,h_h/2])
# array of small cups (two rows)
for v in [-1,1]:
    for h in range(1,cups+1):
        rotation = 90*v # v decides the direction here
        holder=holder \
                     .cut(cup.rotate([0,0,0],[0,0,1],rotation) \
                     .translate([v*h_w/4,(h*(h_l)/(cups*2)-(c_y+offset*2)/2)-offset/2,0]))
#place bigger hole
holder=holder.cut(cupXX.translate([0,-(h_l/4+offset/2),0]))
#fillet the (many) vertical corners
holder=holder.edges('|Z exc %CIRCLE').fillet(offset*overal_edge_radius)

#preview for feedback:
show_object(holder)

#the name holds height and cup number only
exporters.export(
    holder,
    'cupholder_'+str(h_h)+'-'+str(cups)+'.stl',
    tolerance=0.1,
    angularTolerance=0.125
    )
