import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from graph_tool.all import *
from networks.generate_network import *

S = [1, 1, 1, 1]            # White color
I = [0, 0, 0, 1]            # Black color
R = [0.5, 0.5, 0.5, 1]      # Grey color
init_color = [0.6, 0, 0, 1]

def update_state(g, win, newly_infected, complex=False, f=sigmoid):
    """
    Update state of nodes
    :param g: graph
    :param win: window
    :param newly_infected: newly infected nodes property map
    :param complex: if true, run complex contagion
    :param f: probability function
    :return:
    """
    newly_infected.a = False
    infectious = False

    g.set_vertex_filter(g.vp['infectious'])
    infectious_vertices = g.vertices()
    if globals.gDebug:
        print('Number of active infectors : {}'.format(g.num_vertices()))
    g.clear_filters()

    if complex: # complex contagion
        if list(infectious_vertices):
            infectious = True
            for v in g.vertices():
                if g.vp['infectious'][v] or g.vp['recovered'][v]:
                        continue
                newly_infected[v] = g.infect_vertex(v, complex=True)

    else: # simple contagion
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
        if globals.gDebug:
            print('Final epidemic size : {}/{}'.format(g.compute_final_size(), g.num_vertices()))
        return False

    # if doing an offscreen animation, dump frame to disk
    if globals.gSaveImages:
        pixbuf = win.get_pixbuf()
        pixbuf.savev('frames/sirs%06d.png' % globals.gCount, 'png', [], [])
        if globals.gCount > globals.gMaxCount:
            sys.exit(0)
        globals.gCount += 1

    return True


def animate(g, init_infections=1, complex=False, f=sigmoid):
    """
    Run animation
    :param g: graph
    :param init_infections: number of initial infections
    :param complex: if true, run complex contagion
    :return:
    """
    pos = sfdp_layout(g)

    # initialisation
    newly_infected = g.new_vertex_property("bool")
    newly_infected.a = False

    if complex:
        seed = random.choice(range(g.num_vertices()))
        infectious_vertices = [g.vertex(seed)] + list(g.vertex(seed).out_neighbors())
    else:
        infect_idx = random.sample(range(g.num_vertices()), init_infections)
        infectious_vertices = [g.vertex(idx) for idx in infect_idx]

    for vertex in infectious_vertices:
        g.vp['infectious'][vertex] = True
        g.vp['susceptible'][vertex] = False
        g.vp['state'][vertex] = init_color
        newly_infected[vertex] = True

    if not globals.gSaveImages:
        win = GraphWindow(g, pos, geometry=(1200, 1000), edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=g.vp['state'], vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
    else:
        win = Gtk.OffscreenWindow()
        win.set_default_size(500, 400)
        win.graph = GraphWidget(g, pos, vertex_label=g.vp['security'], edge_color=[0.6, 0.6, 0.6, 1], vertex_fill_color=g.vp['state'], vertex_halo=newly_infected, vertex_halo_color=[0.8, 0, 0, 0.6])
        win.add(win.graph)

    cid = GLib.idle_add(update_state, g, win, newly_infected, complex, f)
    win.connect("delete_event", Gtk.main_quit)

    win.show_all()
    Gtk.main()

    print('\nEnd of propagation.\n\n')


if __name__ == '__main__':
    properties = read_properties('../properties/default.properties')
    set_properties(properties)

    n, m = 1000, 1
    output_size, bg_color = (1500, 1500), [1,1,1,1]

    g = barabasi_albert_model(n, m, model='SIRS')
    animate(g, complex=True)

































