import math
import copy
from experiment.models import X_Vertice, U_chain, Graph, Const_visual

def graph_xcoord_calc(graph_xpos, x0, step_x_pos):
    x_pos = (x0 + (graph_xpos * step_x_pos))
    return x_pos
    
def graph_ycoord_calc(graph_ypos, y0, step_y_pos):
    y_pos = (y0 + (graph_ypos * step_y_pos))
    return y_pos
    
def graph_top_x_conn_calc(graph_xpos, x0, step_x_pos):
    x_top_conn= (x0 + 150 + graph_xpos * step_x_pos)
    return x_top_conn
    
def graph_bottom_x_conn_calc(graph_xpos, x0, step_x_pos):
    x_bottom_conn= (x0 + 150 + (graph_xpos * step_x_pos))
    return x_bottom_conn

def graph_top_y_conn_calc(graph_ypos, y0, step_y_pos):
    y_top_conn= (y0 + graph_ypos * step_y_pos)
    return y_top_conn
    
def graph_bottom_y_conn_calc(graph_ypos, y0, step_y_pos):
    y_bottom_conn = ( y0 + 50 + (graph_ypos * step_y_pos))
    return y_bottom_conn
    
def initial_event_graph_bottom_x_conn_calc(graph_xpos, x0, step_x_pos):
    x_initial_bottom_conn= (x0 + 150 + (graph_xpos * step_x_pos))
    return x_initial_bottom_conn
    
def initial_event_graph_top_x_conn_calc(graph_xpos, x0, step_x_pos):
    x_initial_top_conn= (x0 + 150 + (graph_xpos * step_x_pos))
    return x_initial_top_conn    

def position_for_text_x_calc(x1, x2):
    x_text_position = int(10 + 0.5 * (x1 + x2))
    return x_text_position    

def position_for_text_y_calc(x1, x2, y1, y2):
    
    if x1==x2:
        y_text_position = int(0.5 * (y1 + y2) - 35)
    else:
        y_text_position = int(0.5 * (y1 + y2) - 135)
        
    return y_text_position    

def Beta_av(a, b):
    av_beta = a / (a + b)
    return av_beta

def Gamma_av(a, b):
    av_gamma = a / b
    return av_gamma

def Uniform_av(a, b):
    av_uniform = 0.5 * (a + b)
    return av_uniform


def Graph_Initialization():
    
    Graph_full_list = Graph.objects.all()
    X_full_list = X_Vertice.objects.all()
    U_full_list = U_chain.objects.all()
    
    for Gr in Graph_full_list:
        
        for Gr in Graph_full_list:
            
            curr_graph_arr = [ [ [] for j in range(0, 16) ] for i in range(0, 4) ]
            
            current_Graph_X_list1 = X_Vertice.objects.filter(in_Graph=Gr)
            current_Graph_X_list = current_Graph_X_list1.filter(included_in_calculation=True)
            
            current_Graph_U_list1 = U_chain.objects.filter(in_Graph=Gr)
            current_Graph_U_list = current_Graph_U_list1.filter(check_visualization=True)
            
            current_Graph_initial_event_U_list = current_Graph_U_list.filter(initial_event_sign=True)
            
            current_Graph_END_STATE_U_list1 = current_Graph_U_list.filter(should_be_calculated_sign=True)
            current_Graph_END_STATE_U_list = current_Graph_END_STATE_U_list1.filter(res_taken_from_FT=False)
            
            current_chain_count = 0

            #formation of the initial states branches that are included in calculation
            for U_IE in current_Graph_initial_event_U_list:
                
                U_IE_to_vertices = U_IE.vertices_connected_ident
                x_v1 = X_Vertice.objects.get(name=U_IE_to_vertices[0])

                if not x_v1.contained_FT_Graph:
                    
                    #layer 0 and layer 1
                    curr_graph_arr[0][current_chain_count].append(copy.deepcopy(U_IE.weight))
                    curr_graph_arr[1][current_chain_count].append(copy.deepcopy(U_IE.name))
                    curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1.name))
                    curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1.level_in_Graph))
                
                    current_chain_count += 1
                
                if x_v1.contained_FT_Graph:
                    ft_curr = Graph.objects.get(name=x_v1.connected_FT_Graph_name)
                    
                    for res_id in range(0, len(ft_curr.simpl_chains_listing)):

                        #layer 0 and layer 1
                        
                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(U_IE.weight))
                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(U_IE.name))
                        curr_graph_arr[2][current_chain_count].append('_')
                        curr_graph_arr[3][current_chain_count].append(0)
                        
                        #layer 2
                        
                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(ft_curr.simpl_chains_contrib[res_id]))
                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(ft_curr.simpl_chains_listing[res_id]))
                        curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1.name))
                        curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                        #layer 3
                        
                        x_v1_u_list = x_v1.chains_connected_ident
                        
                        for u_x_v in x_v1_u_list:
                            u_x_v1 = U_chain.objects.get(name=u_x_v)
                            if u_x_v1.res_taken_from_FT:
                                if u_x_v1.check_visualization:
                                    curr_graph_arr[0][current_chain_count].append(copy.deepcopy(u_x_v1.weight))
                                    curr_graph_arr[1][current_chain_count].append(copy.deepcopy(u_x_v1.name))
                                    
                                    #next vertice identification
                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                    if x_v1_next_vertice.name==x_v1.name:
                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                    curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.name))
                                    
                                    curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                if not u_x_v1.check_visualization:
                                    curr_graph_arr[0][current_chain_count].append(0)
                                    curr_graph_arr[1][current_chain_count].append('closed')
                                    curr_graph_arr[2][current_chain_count].append('closed')
                                    if Gr.FT_attribute:
                                        curr_graph_arr[3][current_chain_count].append(1000000000)
                                    if not Gr.FT_attribute:
                                        curr_graph_arr[3][current_chain_count].append((-1))
                                    
                        #end of layer 3                
                        current_chain_count += 1

                    #other possibilities inclusion as the independent braches that are not the parts of fault tree branch (not layer)
                    for u_x_v in x_v1_u_list:
                        u_x_v1 = U_chain.objects.get(name=u_x_v)
                        if not u_x_v1.res_taken_from_FT:
                            if u_x_v1.check_visualization:
                                
                                #next vertice identification
                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                if Gr.FT_attribute:
                                    if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                
                                        #layer 0 and layer 1
                                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(U_IE.weight))
                                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(U_IE.name))
                                        curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1.name))
                                        curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1.level_in_Graph))
                                
                                        #layer 2
                                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(u_x_v1.weight))
                                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(u_x_v1.name))
                                        curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.name))
                                        curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                        current_chain_count += 1
                                
                                if not Gr.FT_attribute:
                                    if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                
                                        #layer 0 and layer 1
                                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(U_IE.weight))
                                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(U_IE.name))
                                        curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1.name))
                                        curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1.level_in_Graph))
                                
                                        #layer 2
                                        curr_graph_arr[0][current_chain_count].append(copy.deepcopy(u_x_v1.weight))
                                        curr_graph_arr[1][current_chain_count].append(copy.deepcopy(u_x_v1.name))
                                        curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.name))
                                        curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                        current_chain_count += 1
                                
                            if not u_x_v1.check_visualization:
                                
                                #layer 0 and layer 1
                                curr_graph_arr[0][current_chain_count].append(copy.deepcopy(U_IE.weight))
                                curr_graph_arr[1][current_chain_count].append(copy.deepcopy(U_IE.name))
                                curr_graph_arr[2][current_chain_count].append(copy.deepcopy(x_v1.name))
                                curr_graph_arr[3][current_chain_count].append(copy.deepcopy(x_v1.level_in_Graph))
                                
                                #layer 2
                                curr_graph_arr[0][current_chain_count].append(0)
                                curr_graph_arr[1][current_chain_count].append('closed')
                                curr_graph_arr[2][current_chain_count].append('closed')
                                if Gr.FT_attribute:
                                    curr_graph_arr[3][current_chain_count].append(1000000000)
                                if not Gr.FT_attribute:
                                    curr_graph_arr[3][current_chain_count].append((-1))
                                
                                current_chain_count += 1
                                
            
            #end of the formation of the initial states branches that are included in calculation    
            
########scanning from level to level of continuation of the existing braches and formation of new ones that are the subbranches#####
            
            initial_states_num = current_chain_count
            
            if Gr.FT_attribute:
                
                for lev in range(Gr.max_level - 1, 0, -1):
                    
                    alt_lev = 0
                    
                    for el_n in range(0, current_chain_count):

                        alt_el = 0
                        
                        alt_el_n1 = 0
                        
                        st_0 = copy.deepcopy(curr_graph_arr[0][el_n])
                        st_1 = copy.deepcopy(curr_graph_arr[1][el_n])
                        st_2 = copy.deepcopy(curr_graph_arr[2][el_n])
                        st_3 = copy.deepcopy(curr_graph_arr[3][el_n])
                        
                        if not st_1[len(st_1)-1]=='closed':
                            
                            zz2 = len(st_1)-1
                            z2 = len(st_3)-1
                            zzz2 = st_3[len(st_3)-1]

                            if lev==st_3[len(st_3)-1]:
                        
                                x_v1 = X_Vertice.objects.get(name=st_2[len(st_2)-1])
                                x_v1_u_list = x_v1.chains_connected_ident

                                if not x_v1.contained_FT_Graph:
                                    
                                    for u_x_v in x_v1_u_list:
                                        u_x_v1 = U_chain.objects.get(name=u_x_v)

                                        if u_x_v1.check_visualization:
                                            if u_x_v1.should_be_calculated_sign:
                                                
                                                #final layer
                                                curr_graph_arr[0][el_n].append(1.0)
                                                curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                curr_graph_arr[2][el_n].append('END')
                                                curr_graph_arr[3][el_n].append('END')
                                
                                            if not u_x_v1.should_be_calculated_sign:
                                                if alt_el >= 1:
                                                    
                                                    #next vertice identification
                                                    uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                    if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                    if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                        
                                                        #generation of the new branches at the end of the array
                                                        #layer 0 and layer 1
                                                        for i1 in range(0, len(st_0)):
                                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                        #layer 2
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                        alt_el += 1
                                                
                                                if alt_el == 0:
                                                    
                                                    #next layer for the already existing branch (zero variant - others as a new branches)
                                                    #next vertice identification
                                                    uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                    if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                    if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                    
                                                        curr_graph_arr[0][el_n].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                        curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1_next_vertice.name))
                                                        curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                        alt_el += 1

                                        if not u_x_v1.check_visualization:
                                
                                            if alt_el >= 1:
                                                    
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(1000000000)
                                
                                                    alt_el += 1
                                                
                                            if alt_el == 0:
                                                    
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                
                                                    #next layer for the already existing branch (zero variant - others as a new branches)
                                                    curr_graph_arr[0][el_n].append(0)
                                                    curr_graph_arr[1][el_n].append('closed')
                                                    curr_graph_arr[2][el_n].append('closed')
                                                    curr_graph_arr[3][el_n].append(1000000000)
                                
                                                    alt_el += 1
                                
                                if x_v1.contained_FT_Graph:
                                    ft_curr = Graph.objects.get(name=x_v1.connected_FT_Graph_name)

                                    for res_id in range(0, len(ft_curr.simpl_chains_listing)):
                                        
                                        if alt_el >= 1:
                                    
                                            #layer 0 and layer 1
                        
                                            for i1 in range(0, len(st_0)):
                                                curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                            
                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(1.0)
                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('_')
                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('_')
                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 2
                        
                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(ft_curr.simpl_chains_contrib[res_id]))
                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(ft_curr.simpl_chains_listing[res_id]))
                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.name))
                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 3
                        
                                            for u_x_v in x_v1_u_list:
                                                u_x_v1 = U_chain.objects.get(name=u_x_v)
                                                if u_x_v1.res_taken_from_FT:
                                                    if u_x_v1.check_visualization:
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                        uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                    
                                                        #next vertice identification
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                        if x_v1_next_vertice.name==x_v1.name:
                                                            x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                    
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                                    if not u_x_v1.check_visualization:
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(1000000000)
                                            #end of layer 3                
                                            alt_el += 1

                                        if alt_el == 0:
                                            
                                            #layer 0 and layer 1
                        
                                            curr_graph_arr[0][el_n].append(1.0)
                                            curr_graph_arr[1][el_n].append('_')
                                            curr_graph_arr[2][el_n].append('_')
                                            curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 2
                        
                                            curr_graph_arr[0][el_n].append(copy.deepcopy(ft_curr.simpl_chains_contrib[res_id]))
                                            curr_graph_arr[1][el_n].append(copy.deepcopy(ft_curr.simpl_chains_listing[res_id]))
                                            curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1.name))
                                            curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 3
                        
                                            for u_x_v in x_v1_u_list:
                                                u_x_v1 = U_chain.objects.get(name=u_x_v)
                                                if u_x_v1.res_taken_from_FT:
                                                    if u_x_v1.check_visualization:
                                                        curr_graph_arr[0][el_n].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                        uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                    
                                                        #next vertice identification
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                        if x_v1_next_vertice.name==x_v1.name:
                                                            x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                        curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1_next_vertice.name))
                                    
                                                        curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                                    if not u_x_v1.check_visualization:
                                                        curr_graph_arr[0][el_n].append(0)
                                                        curr_graph_arr[1][el_n].append('closed')
                                                        curr_graph_arr[2][el_n].append('closed')
                                                        curr_graph_arr[3][el_n].append(1000000000)
                                            #end of layer 3                
                                            alt_el += 1
                                    
                        #other possibilities inclusion as the independent braches that are not the parts of fault tree branch (not layer)
                                    
                                    for u_x_v in x_v1_u_list:
                                        u_x_v1 = U_chain.objects.get(name=u_x_v)
                                        
                                        if not u_x_v1.res_taken_from_FT:

                                            if u_x_v1.check_visualization:
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                        
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                    alt_el += 1
                                                
                                            if not u_x_v1.check_visualization:
                                
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph < x_v1.level_in_Graph:
                                                
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(1000000000)
                                
                                                    alt_el += 1

                            if alt_el > 0:
                                alt_el -= 1
                        
                        alt_lev += copy.deepcopy(alt_el) + copy.deepcopy(alt_el_n1)
                        
                    current_chain_count += copy.deepcopy(alt_lev)
                
            if not Gr.FT_attribute:
                
                for lev in range(1, Gr.max_level):
                    
                    alt_lev = 0
                    
                    for el_n in range(0, current_chain_count):

                        alt_el = 0
                        
                        alt_el_n1 = 0
                        
                        st_0 = copy.deepcopy(curr_graph_arr[0][el_n])
                        st_1 = copy.deepcopy(curr_graph_arr[1][el_n])
                        st_2 = copy.deepcopy(curr_graph_arr[2][el_n])
                        st_3 = copy.deepcopy(curr_graph_arr[3][el_n])
                        
                        if not st_1[len(st_1)-1]=='closed':
                            
                            zz2 = len(st_1)-1
                            z2 = len(st_3)-1
                            zzz2 = st_3[len(st_3)-1]

                            if lev==st_3[len(st_3)-1]:
                        
                                x_v1 = X_Vertice.objects.get(name=st_2[len(st_2)-1])
                                x_v1_u_list = x_v1.chains_connected_ident

                                if not x_v1.contained_FT_Graph:
                                    
                                    for u_x_v in x_v1_u_list:
                                        u_x_v1 = U_chain.objects.get(name=u_x_v)

                                        if u_x_v1.check_visualization:
                                            if u_x_v1.should_be_calculated_sign:
                                                
                                                #final layer
                                                curr_graph_arr[0][el_n].append(1.0)
                                                curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                curr_graph_arr[2][el_n].append('END')
                                                curr_graph_arr[3][el_n].append('END')
                                
                                            if not u_x_v1.should_be_calculated_sign:
                                                if alt_el >= 1:
                                                    
                                                    #next vertice identification
                                                    uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                    if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                    if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                        
                                                        #generation of the new branches at the end of the array
                                                        #layer 0 and layer 1
                                                        for i1 in range(0, len(st_0)):
                                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                        #layer 2
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                        alt_el += 1
                                                
                                                if alt_el == 0:
                                                    
                                                    #next layer for the already existing branch (zero variant - others as a new branches)
                                                    #next vertice identification
                                                    uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                    if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                    if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                    
                                                        curr_graph_arr[0][el_n].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                        curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1_next_vertice.name))
                                                        curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                        alt_el += 1

                                        if not u_x_v1.check_visualization:
                                
                                            if alt_el >= 1:
                                                    
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append((-1))
                                
                                                    alt_el += 1
                                                
                                            if alt_el == 0:
                                                    
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                
                                                    #next layer for the already existing branch (zero variant - others as a new branches)
                                                    curr_graph_arr[0][el_n].append(0)
                                                    curr_graph_arr[1][el_n].append('closed')
                                                    curr_graph_arr[2][el_n].append('closed')
                                                    curr_graph_arr[3][el_n].append((-1))
                                
                                                    alt_el += 1
                                
                                if x_v1.contained_FT_Graph:
                                    ft_curr = Graph.objects.get(name=x_v1.connected_FT_Graph_name)

                                    for res_id in range(0, len(ft_curr.simpl_chains_listing)):
                                        
                                        if alt_el >= 1:
                                    
                                            #layer 0 and layer 1
                        
                                            for i1 in range(0, len(st_0)):
                                                curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                            
                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(1.0)
                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('_')
                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('_')
                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 2
                        
                                            curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(ft_curr.simpl_chains_contrib[res_id]))
                                            curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(ft_curr.simpl_chains_listing[res_id]))
                                            curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.name))
                                            curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 3
                        
                                            for u_x_v in x_v1_u_list:
                                                u_x_v1 = U_chain.objects.get(name=u_x_v)
                                                if u_x_v1.res_taken_from_FT:
                                                    if u_x_v1.check_visualization:
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                        uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                    
                                                        #next vertice identification
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                        if x_v1_next_vertice.name==x_v1.name:
                                                            x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                    
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                                    if not u_x_v1.check_visualization:
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append((-1))
                                            #end of layer 3                
                                            alt_el += 1

                                        if alt_el == 0:
                                            
                                            #layer 0 and layer 1
                        
                                            curr_graph_arr[0][el_n].append(1.0)
                                            curr_graph_arr[1][el_n].append('_')
                                            curr_graph_arr[2][el_n].append('_')
                                            curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 2
                        
                                            curr_graph_arr[0][el_n].append(copy.deepcopy(ft_curr.simpl_chains_contrib[res_id]))
                                            curr_graph_arr[1][el_n].append(copy.deepcopy(ft_curr.simpl_chains_listing[res_id]))
                                            curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1.name))
                                            curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1.level_in_Graph))
                        
                                            #layer 3
                        
                                            for u_x_v in x_v1_u_list:
                                                u_x_v1 = U_chain.objects.get(name=u_x_v)
                                                if u_x_v1.res_taken_from_FT:
                                                    if u_x_v1.check_visualization:
                                                        curr_graph_arr[0][el_n].append(copy.deepcopy(u_x_v1.weight))
                                                        curr_graph_arr[1][el_n].append(copy.deepcopy(u_x_v1.name))
                                                        uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                    
                                                        #next vertice identification
                                                        x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                        if x_v1_next_vertice.name==x_v1.name:
                                                            x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                        curr_graph_arr[2][el_n].append(copy.deepcopy(x_v1_next_vertice.name))
                                    
                                                        curr_graph_arr[3][el_n].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                                    if not u_x_v1.check_visualization:
                                                        curr_graph_arr[0][el_n].append(0)
                                                        curr_graph_arr[1][el_n].append('closed')
                                                        curr_graph_arr[2][el_n].append('closed')
                                                        curr_graph_arr[3][el_n].append((-1))
                                            #end of layer 3                
                                            alt_el += 1
                                    
                        #other possibilities inclusion as the independent braches that are not the parts of fault tree branch (not layer)
                                    
                                    for u_x_v in x_v1_u_list:
                                        u_x_v1 = U_chain.objects.get(name=u_x_v)
                                        
                                        if not u_x_v1.res_taken_from_FT:

                                            if u_x_v1.check_visualization:
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                        
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.weight))
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(u_x_v1.name))
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.name))
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(x_v1_next_vertice.level_in_Graph))
                                
                                                    alt_el += 1
                                                
                                            if not u_x_v1.check_visualization:
                                
                                                #next layer for the already existing branch (zero variant - others as a new branches)
                                                #next vertice identification
                                                uu_x_v1_conn_list = u_x_v1.vertices_connected_ident
                                                x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[0])
                                                if x_v1_next_vertice.name==x_v1.name and len(uu_x_v1_conn_list)==2:
                                                    x_v1_next_vertice = X_Vertice.objects.get(name=uu_x_v1_conn_list[1])
                                    
                                                if x_v1_next_vertice.level_in_Graph > x_v1.level_in_Graph:
                                                
                                                    #generation of the new branches at the end of the array
                                                    #layer 0 and layer 1
                                                    for i1 in range(0, len(st_0)):
                                                        curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_0[i1]))
                                                        curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_1[i1]))
                                                        curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_2[i1]))
                                                        curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(copy.deepcopy(st_3[i1]))
                                
                                                    #layer 2
                                                    curr_graph_arr[0][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append(0)
                                                    curr_graph_arr[1][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[2][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append('closed')
                                                    curr_graph_arr[3][current_chain_count + alt_el + alt_lev + alt_el_n1 - 1].append((-1))
                                
                                                    alt_el += 1

                            if alt_el > 0:
                                alt_el -= 1
                        
                        alt_lev += copy.deepcopy(alt_el) + copy.deepcopy(alt_el_n1)
                        
                    current_chain_count += copy.deepcopy(alt_lev)

            res_for_current_Graph = 0.0
            
            Gr.simpl_chains_listing.clear()
            Gr.simpl_chains_contrib.clear()
            
            Gr.simpl_chains_listing = []
            Gr.simpl_chains_contrib = []
            
            filtered_current_chain_count = 0
            
            for i2 in range(0, current_chain_count):
                
                st_fin_0 = copy.deepcopy(curr_graph_arr[0][i2])
                st_fin_1 = copy.deepcopy(curr_graph_arr[1][i2])
                st_fin_2 = copy.deepcopy(curr_graph_arr[2][i2])
                st_fin_3 = copy.deepcopy(curr_graph_arr[3][i2])
                
                if not 'closed' in st_fin_1:
                    filtered_current_chain_count += 1
            
            for i2 in range(0, filtered_current_chain_count):
                Gr.simpl_chains_listing.append('')
                Gr.simpl_chains_contrib.append(1.0)
            
            end_states_names_list = []
            for end_state in current_Graph_END_STATE_U_list:
                end_state.weight = 0.0
                end_states_names_list.append(copy.deepcopy(end_state.name))
                end_state.save()
            
            filtered_counts = 0
            
            for i2 in range(0, current_chain_count):
                
                end_state_should_be_calculated_sign = 0
                end_state_should_be_calculated_name = ''
                
                st_fin_0 = copy.deepcopy(curr_graph_arr[0][i2])
                st_fin_1 = copy.deepcopy(curr_graph_arr[1][i2])
                st_fin_2 = copy.deepcopy(curr_graph_arr[2][i2])
                st_fin_3 = copy.deepcopy(curr_graph_arr[3][i2])
                
                if not 'closed' in st_fin_1:
                    s_c = '_begin_'
                    s_r = 1.0

                    for j2 in range(0, len(st_fin_0)):
                        
                        s_c += copy.deepcopy(st_fin_1[j2]) + '-' + copy.deepcopy(st_fin_2[j2]) + '-'
                        s_r *= copy.deepcopy(st_fin_0[j2])
                        
                        if copy.deepcopy(st_fin_1[j2]) in end_states_names_list:
                            end_state_should_be_calculated_name = copy.deepcopy(st_fin_1[j2])
                            end_state_should_be_calculated_sign = 1
                            
                    s_c += '_end_'
                    
                    if end_state_should_be_calculated_sign == 1:
                        end_state_should_be_calculated_u = U_chain.objects.get(name=end_state_should_be_calculated_name)
                        qu = copy.deepcopy(end_state_should_be_calculated_u.weight)
                        qu += copy.deepcopy(s_r)
                        end_state_should_be_calculated_u.weight = copy.deepcopy(qu)
                        end_state_should_be_calculated_u.save()
                    
                    Gr.simpl_chains_listing[filtered_counts] = copy.deepcopy(s_c)
                    Gr.simpl_chains_contrib[filtered_counts] = copy.deepcopy(s_r)
                    
                    filtered_counts += 1
            
            for i2 in range(0, filtered_current_chain_count):
                res_for_current_Graph += copy.deepcopy(Gr.simpl_chains_contrib[i2])
            
            Gr.res = res_for_current_Graph
            
            if res_for_current_Graph!=0.0:    
                for i2 in range(0, filtered_current_chain_count):
                    rr = copy.deepcopy(Gr.simpl_chains_contrib[i2])
                    Gr.simpl_chains_contrib[i2] = copy.deepcopy(rr/res_for_current_Graph)
            
            Gr.save()
    
    return