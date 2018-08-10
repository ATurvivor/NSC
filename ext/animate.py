from graph_tool.all import *
from properties.properties import *
from networks.generate_network import *

import random
from properties import globals

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

S = [1, 1, 1, 1]            # White color
I = [0, 0, 0, 1]            # Black color
R = [0.5, 0.5, 0.5, 1.]     # Grey color

def update_state(g, win, newly_infected):
    newly_infected.a = False
    infectious = False

    g.set_vertex_filter(g.vp['infectious'])
    infectious_vertices = g.vertices()
    g.clear_filters()

    for v in infectious_vertices:
        infectious = True
        for u in g.vertex(v).all_neighbors():
            if g.vp['infectious'][u] or g.vp['recovered'][u]:
                continue
            if random.random() < g.get_transmissibility(v, u):
                newly_infected[u] = g.infect_vertex(u)

    if g.gp['model'] == 'SIRS':
        g.update_recovered_time()
    g.update_infectious_time()

    win.graph.regenerate_surface()
    win.graph.queue_draw()

    if not infectious:
        g.set_vertex_filter(g.vp['infectious'])
        if not g.num_vertices():
            if globals.gDebug:
                print('Total nodes recovered nodes : {}/{}'.format(g.compute_final_size(), g.num_vertices()))
            return False
        g.clear_filters()

    # if doing an offscreen animation, dump frame to disk
    if globals.gSaveImages:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/sirs%06d.png' % globals.gCount, 'png', [], [])
        if globals.gCount > globals.gMaxCount:
            sys.exit(0)
        globals.gCount += 1

    return True

def animate(g, init_infections):
    pos = sfdp_layout(g)

    # initialisation
    newly_infected = g.new_vertex_property("bool")
    newly_infected.a = False

    infect_idx = random.sample(range(g.num_vertices()), init_infections)
    infectious_vertices = [g.vertex(idx) for idx in infect_idx]
    for vertex in infectious_vertices:
        g.vp['state'][vertex] = I
        g.vp['infectious'][vertex] = 1
        newly_infected[vertex] = True

    if not globals.gSaveImages:
        win = GraphWindow(g, pos, geometry=(1200, 1000), edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=g.vp['state'], vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
    else:
        win = Gtk.OffscreenWindow()
        win.set_default_size(500, 400)
        win.graph = GraphWidget(g, pos, vertex_label=g.vp['security'], edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=g.vp['state'], vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
        win.add(win.graph)

    cid = GLib.idle_add(update_state, g, win, newly_infected)
    win.connect("delete_event", Gtk.main_quit)

    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    properties = read_properties('../properties/test.properties')
    set_properties(properties)

    n, m = 1000, 1
    ps = pt = lambda : random.randint(1,m)
    output_size, bg_color = (1500, 1500), [1,1,1,1]

    g = barabasi_albert_model(n, m, model='SIRS')
    animate(g, init_infections=1)

































