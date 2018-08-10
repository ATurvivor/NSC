from graph_tool.all import *
from properties.properties import *
from networks.generate_network import *

import random

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib

S = [1, 1, 1, 1]            # White color
I = [0, 0, 0, 1]            # Black color
R = [0.5, 0.5, 0.5, 1.]     # Grey color

def update_state(g, win, newly_infected, state, off_screen, count, max_count):
    if g.gp['model'] == 'SIRS':
        g.update_recovered_time()
        g.set_vertex_filter(g.vp['susceptible'])
        susceptible_vertices = g.vertices()
        for v in susceptible_vertices:
            state[v] = S
        g.clear_filters()


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
                # infect new node
                if g.infect_vertex(u):
                    newly_infected[u] = True
                    state[u] = I

    g.update_infectious_time()
    g.set_vertex_filter(g.vp['recovered'])
    recovered_vertices = g.vertices()
    for v in recovered_vertices:
        state[v] = R
    g.clear_filters()

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
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
    if off_screen:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/sirs%06d.png' % count, 'png', [], [])
        if count > max_count:
            sys.exit(0)
        count += 1

    # We need to return True so that the main loop will call this function more
    # than once.
    return True

def animate(g, init_infections, off_screen):
    pos = sfdp_layout(g)

    # initialisation
    newly_infected = g.new_vertex_property("bool")
    newly_infected.a = False

    state = g.new_vertex_property("vector<double>")
    for vertex in g.vertices():
        state[vertex] = S

    max_count = 500
    count = 0

    # initial infection
    infect_idx = random.sample(range(g.num_vertices()), init_infections)
    infectious_vertices = [g.vertex(idx) for idx in infect_idx]
    for vertex in infectious_vertices:
        state[vertex] = I
        g.vp['infectious'][vertex] = 1
        newly_infected[vertex] = True

    if not off_screen:
        win = GraphWindow(g, pos, geometry=(1200, 1000), edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=state, vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
    else:
        win = Gtk.OffscreenWindow()
        win.set_default_size(500, 400)
        win.graph = GraphWidget(g, pos, edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=state, vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
        win.add(win.graph)

    # bind the function above as an 'idle' callback
    cid = GLib.idle_add(update_state, g, win, newly_infected, state, off_screen, count, max_count)
    win.connect("delete_event", Gtk.main_quit)

    # show the window and start main loop
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    properties = read_properties('../properties/test.properties')
    set_properties(properties)

    n, m = 1000, 1
    ps = pt = lambda : random.randint(1,m)
    output_size, bg_color = (1500, 1500), [1,1,1,1]

    g = barabasi_albert_model(n, m)
    g.gp['model'] = 'SIRS'
    animate(g, 1, False)

































