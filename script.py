import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print ("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    systems = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    step = 40
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # print (symbols)
    # copy = symbols.keys()
    # for d in copy:
    #     print(symbols[d][1])

    ARG_COMMANDS = set([ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus', 'display' , 'constants',"push","pop" ])
    
    for command in commands:
        # print("current command is " + command["op"])
        # print (command.keys())
        if command["op"] not in ARG_COMMANDS:
            print("Invalid op in command list: " + command["op"])
            return
        if command["op"] == "constants":
            continue
        if command["op"] == 'sphere':
            #print 'SPHERE\t' + str(args)
            args = command["args"]
            reflect = command["constants"]
            
            if reflect == None:
                reflect = ".white"
            # if not (len(symbols[reflect]) > 0 and symbols[reflect][1] != None):
            #     reflect = '.white'

            add_sphere(coords1,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( systems[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []

        elif command["op"] == 'torus':
            #print 'TORUS\t' + str(args)
            args = command["args"]
            reflect = command["constants"]
            
            if reflect == None:
                reflect = ".white"
            # if not (len(symbols[reflect]) > 0 and symbols[reflect][1] != None):
            #     reflect = '.white'

            add_torus(coords1,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( systems[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []

        elif command["op"] == 'box':
            #print 'BOX\t' + str(args)
            args = command["args"]
            reflect = command["constants"]
            if reflect == None:
                reflect = ".white"
            # if not (len(symbols[reflect]) > 0 and symbols[reflect][1] != None):
            #     reflect = '.white'

            add_box(coords1,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( systems[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols,reflect)
            coords1 = []

        elif command["op"] == 'circle':
            #print 'CIRCLE\t' + str(args)
            args = command["args"]
            add_circle(coords,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( systems[-1], coords )
            draw_lines(coords, screen, zbuffer, color)
            coords = []

        # elif line == 'hermite' or line == 'bezier':
        #     #print 'curve\t' + line + ": " + str(args)
        #     add_curve(edges,
        #               float(args[0]), float(args[1]),
        #               float(args[2]), float(args[3]),
        #               float(args[4]), float(args[5]),
        #               float(args[6]), float(args[7]),
        #               step, line)
        #     matrix_mult( systems[-1], edges )
        #     draw_lines(edges, screen, zbuffer, color)
        #     edges = []

        elif command["op"] == 'line':
            #print 'LINE\t' + str(args)
            args = command["args"]
            add_edge( coords,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( systems[-1], coords )
            draw_lines(coords, screen, zbuffer, color)
            coords = []

        elif command["op"] == 'scale':
            #print 'SCALE\t' + str(args)
            args = command["args"]
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command["op"] == 'move':
            #print 'MOVE\t' + str(args)
            args = command["args"]
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command["op"] == 'rotate':
            #print 'ROTATE\t' + str(args)
            args = command["args"]
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command["op"] == 'push':
            systems.append( [x[:] for x in systems[-1]] )

        elif command["op"] == 'pop':
            systems.pop()

        elif command["op"] == 'display' or command["op"] == 'save':
            
            if command["op"] == 'display':
                display(screen)
            else:
                # print("reached here")
                # print(command["args"])
                save_extension(screen, command["args"][0]+".png")

    return
