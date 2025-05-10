import math

import experiment.calculation_initialization as calc

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from experiment.models import X_Vertice, U_chain, Graph, Const_visual

@login_required()
def science_base(request):
    return render(request, 'science_base.html')
    
@login_required()
def science_experiment(request):
    
    Graph_list = Graph.objects.all()
    
    Gr1 = None
    main_Graph_name = ''
    
    for Grr in Graph_list:
        if not Grr.FT_attribute:
            Gr1 = Grr
            main_Graph_name = Grr.name
    
    a_list = X_Vertice.objects.filter(in_Graph=Gr1)
    a2_list = U_chain.objects.filter(in_Graph=Gr1)
    
    max_level = 1
    max_range = 1
    
    C_V = Const_visual.objects.get(pk=1)
    C_V = Const_visual.objects.get(pk=1)
    xx0 = C_V.x0
    yy0 = C_V.y0
    stepx = C_V.step_x_pos
    stepy = C_V.step_y_pos
    
    for X_V in a_list:
        if X_V.level_in_Graph > max_level: max_level = X_V.level_in_Graph
        if X_V.position_in_Graph > max_range: max_range = X_V.position_in_Graph
    
    max_level += 1
    max_range += 1
    
    Gr1.max_level = max_level
    Gr1.max_position = max_range
    Gr1.max_y_coord = yy0 + max_level * stepy
    Gr1.max_x_coord = xx0 + max_range * stepx
    Gr1.save()
    
    for X_V in a_list:
        graph_lev = X_V.level_in_Graph
        graph_pos = X_V.position_in_Graph
        X_V.graph_xcoord = calc.graph_xcoord_calc(graph_pos, xx0, stepx)
        X_V.graph_ycoord = calc.graph_ycoord_calc(graph_lev, yy0, stepy)
        X_V.graph_top_x_conn = calc.graph_top_x_conn_calc(graph_pos, xx0, stepx)
        X_V.graph_bottom_x_conn = calc.graph_bottom_x_conn_calc(graph_pos, xx0, stepx)
        X_V.graph_top_y_conn = calc.graph_top_y_conn_calc(graph_lev, yy0, stepy)
        X_V.graph_bottom_y_conn = calc.graph_bottom_y_conn_calc(graph_lev, yy0, stepy)
        X_V.initial_event_graph_bottom_x_conn = calc.initial_event_graph_bottom_x_conn_calc(graph_pos, xx0, stepx)
        X_V.initial_event_graph_bottom_y_conn = Gr1.max_y_coord - 1
        X_V.initial_event_graph_top_x_conn = calc.initial_event_graph_top_x_conn_calc(graph_pos, xx0, stepx)
        X_V.initial_event_graph_top_y_conn = 2
        
        X_V.save()
    
    q1 = ''
    q2 = ''
    q3 = ''
    q4 = ''
    
    for U_C in a2_list:
        xv1 = None
        xv2 = None
        uu = U_C.vertices_connected_ident
        xv1 = X_Vertice.objects.get(name=uu[0])
        if len(uu) == 2:
            xv2 = X_Vertice.objects.get(name=uu[1])
            if xv1.included_in_calculation and xv2.included_in_calculation:
                    U_C.check_visualization=True
                    q1 += xv1.name + xv2.name
            else:
                    q2 += xv1.name + xv2.name
                    U_C.check_visualization=False
        else:
            if xv1.included_in_calculation:
                q3 += xv1.name
                U_C.check_visualization=True
            else:
                q4 += xv1.name
                U_C.check_visualization=False
            
        if xv1.initial_event_on_top_sign or xv1.initial_event_on_bottom_sign:
            if xv2 == None:
                U_C.from_xcoord = xv1.initial_event_graph_top_x_conn
                U_C.from_ycoord = xv1.initial_event_graph_top_y_conn
                U_C.to_xcoord = xv1.graph_top_x_conn
                U_C.to_ycoord = xv1.graph_top_y_conn
                if xv1.initial_event_on_bottom_sign:
                    U_C.from_xcoord = xv1.graph_top_x_conn
                    U_C.from_ycoord = xv1.graph_top_y_conn
                    U_C.to_xcoord = xv1.initial_event_graph_bottom_x_conn
                    U_C.to_ycoord = xv1.initial_event_graph_bottom_y_conn
            else:
                U_C.from_xcoord = xv1.graph_bottom_x_conn
                U_C.from_ycoord = xv1.graph_bottom_y_conn
        
                U_C.to_xcoord = xv2.graph_top_x_conn
                U_C.to_ycoord = xv2.graph_top_y_conn
        else:
            U_C.from_xcoord = xv1.graph_bottom_x_conn
            U_C.from_ycoord = xv1.graph_bottom_y_conn
        
            U_C.to_xcoord = xv2.graph_top_x_conn
            U_C.to_ycoord = xv2.graph_top_y_conn
        
        U_C.text_xcoord = calc.position_for_text_x_calc(U_C.from_xcoord, U_C.to_xcoord)
        U_C.text_ycoord = calc.position_for_text_y_calc(U_C.from_xcoord, U_C.to_xcoord, U_C.from_ycoord, U_C.to_ycoord)
        
        if U_C.parametrization:
            if U_C.dist_typ == 'Normal' or U_C.dist_typ == 'LogNormal':
                U_C.weight = U_C.dist_par1
            elif U_C.dist_typ == 'Beta':
                U_C.weight = calc.Beta_av(U_C.dist_par1, U_C.dist_par2)
            elif U_C.dist_typ == 'Gamma':
                U_C.weight = calc.Gamma_av(U_C.dist_par1, U_C.dist_par2)
            else:
                U_C.weight = calc.Uniform_av(U_C.dist_par1, U_C.dist_par2)
        
        
        if U_C.res_taken_from_FT:
            gr_u1 = Graph.objects.get(name=U_C.res_taken_from_FT_name)
            U_C.parametrization = gr_u1.parametrization
            U_C.dist_typ = gr_u1.dist_typ
            U_C.dist_par1 = gr_u1.dist_par1
            U_C.dist_par2 = gr_u1.dist_par2
            U_C.weight = gr_u1.res
            U_C.weight_uncertain = gr_u1.uncertain
        
        U_C.save()
    
    calc.Graph_Initialization()
    #list of results formation
    
    res_graph = []
    for res_id in range(len(Gr1.simpl_chains_listing)):
        res_graph.append('')
        str1 = Gr1.simpl_chains_listing[res_id] + ' contribution = ' + str(Gr1.simpl_chains_contrib[res_id])
        res_graph[res_id] = str1
    
    if request.method == 'POST':
        calcul_incl = False
        for X_V in a_list:
            calcul_incl = request.POST.get('vertice_' + X_V.name + '_calcul')
            if calcul_incl:
                X_V.included_in_calculation = True
                calcul_incl = False
            else:
                X_V.included_in_calculation = False
                calcul_incl = False
            
            X_V.save()
        
        for U_C in a2_list:
            xv1 = None
            xv2 = None
            uu = U_C.vertices_connected_ident
            xv1 = X_Vertice.objects.get(name=uu[0])
            if len(uu) == 2:
                xv2 = X_Vertice.objects.get(name=uu[1])
                if xv1.included_in_calculation and xv2.included_in_calculation:
                    U_C.check_visualization=True
                    q1 += xv1.name + xv2.name
                else:
                    q2 += xv1.name + xv2.name
                    U_C.check_visualization=False
            else:
                if xv1.included_in_calculation:
                    q3 += xv1.name
                    U_C.check_visualization=True
                else:
                    q4 += xv1.name
                    U_C.check_visualization=False
            
            if not U_C.should_be_calculated_sign:
                if not U_C.res_taken_from_FT:
                    if U_C.parametrization:
                        U_C.dist_typ = request.POST.get('probability_distr_type_for_chain_' + U_C.name)
                        U_C.dist_par1 = float(request.POST.get('chain_' + U_C.name +  '_probab_1_calcul'))
                        U_C.dist_par2 = float(request.POST.get('chain_' + U_C.name +  '_probab_2_calcul'))
                
                        if U_C.dist_typ == 'Normal' or U_C.dist_typ == 'LogNormal':
                            U_C.weight = U_C.dist_par1
                        elif U_C.dist_typ == 'Beta':
                            U_C.weight = calc.Beta_av(U_C.dist_par1, U_C.dist_par2)
                        elif U_C.dist_typ == 'Gamma':
                            U_C.weight = calc.Gamma_av(U_C.dist_par1, U_C.dist_par2)
                        else:
                            U_C.weight = calc.Uniform_av(U_C.dist_par1, U_C.dist_par2)
                    if not U_C.parametrization:
                        U_C.weight = float(request.POST.get('chain_' + U_C.name + '_calcul'))
                        U_C.weight_uncertain = float(request.POST.get('chain_' + U_C.name +  '_uncert_calcul'))
            
            if U_C.res_taken_from_FT:
                gr_u1 = Graph.objects.get(name=U_C.res_taken_from_FT_name)
                U_C.parametrization = gr_u1.parametrization
                U_C.dist_typ = gr_u1.dist_typ
                U_C.dist_par1 = gr_u1.dist_par1
                U_C.dist_par2 = gr_u1.dist_par2
                U_C.weight = gr_u1.res
                U_C.weight_uncertain = gr_u1.uncertain
            
            U_C.save()
        
        calc.Graph_Initialization()
        
        #list of results formation
        res_graph = []
        for res_id in range(len(Gr1.simpl_chains_listing)):
            res_graph.append('')
            str1 = Gr1.simpl_chains_listing[res_id] + ' contribution = ' + str(Gr1.simpl_chains_contrib[res_id])
            res_graph[res_id] = str1
        
    context = {'X_Vertice_list': a_list, 'Graph': Gr1, 'U_chain_list': a2_list, 'constants': C_V, 'q1': q1,  'q2': q2,  'q3': q3,  'q4': q4, 'res_graph': res_graph}
    return render(request, 'experiment.html', context)

@login_required()
def science_fault_tree(request, Graph_name):
    
    C_V = Const_visual.objects.get(pk=1)
    C_V = Const_visual.objects.get(pk=1)
    xx0 = C_V.x0
    yy0 = C_V.y0
    stepx = C_V.step_x_pos
    stepy = C_V.step_y_pos
    
    Graph_list = Graph.objects.all()
    
    Gr1 = None
    max_level = 1
    max_range = 1
    
    for Grr in Graph_list:
        if Grr.name==Graph_name:
            Gr1 = Grr

    if Gr1==None:
        return HttpResponse("The Graph with that name does not exist")
    else:
        
        a_list = X_Vertice.objects.filter(in_Graph=Gr1)
        a2_list = U_chain.objects.filter(in_Graph=Gr1)
        
        for X_V in a_list:
            if X_V.level_in_Graph > max_level: max_level = X_V.level_in_Graph
            if X_V.position_in_Graph > max_range: max_range = X_V.position_in_Graph
        
        max_level += 1
        max_range += 1
        
        Gr1.max_level = max_level
        Gr1.max_position = max_range
        Gr1.max_y_coord = yy0 + max_level * stepy
        Gr1.max_x_coord = xx0 + max_range * stepx
        Gr1.save()

        for X_V in a_list:
            graph_lev = X_V.level_in_Graph
            graph_pos = X_V.position_in_Graph
            X_V.graph_xcoord = calc.graph_xcoord_calc(graph_pos, xx0, stepx)
            X_V.graph_ycoord = calc.graph_ycoord_calc(graph_lev, yy0, stepy)
            X_V.graph_top_x_conn = calc.graph_top_x_conn_calc(graph_pos, xx0, stepx)
            X_V.graph_bottom_x_conn = calc.graph_bottom_x_conn_calc(graph_pos, xx0, stepx)
            X_V.graph_top_y_conn = calc.graph_top_y_conn_calc(graph_lev, yy0, stepy)
            X_V.graph_bottom_y_conn = calc.graph_bottom_y_conn_calc(graph_lev, yy0, stepy)
            X_V.initial_event_graph_bottom_x_conn = calc.initial_event_graph_bottom_x_conn_calc(graph_pos, xx0, stepx)
            X_V.initial_event_graph_bottom_y_conn = Gr1.max_y_coord - 1
            X_V.initial_event_graph_top_x_conn = calc.initial_event_graph_top_x_conn_calc(graph_pos, xx0, stepx)
            X_V.initial_event_graph_top_y_conn = 2
        
            X_V.save()
        
        q1 = ''
        q2 = ''
        q3 = ''
        q4 = ''
    
        for U_C in a2_list:
            xv1 = None
            xv2 = None
            uu = U_C.vertices_connected_ident
            xv1 = X_Vertice.objects.get(name=uu[0])
            if len(uu) == 2:
                xv2 = X_Vertice.objects.get(name=uu[1])
                if xv1.included_in_calculation and xv2.included_in_calculation:
                    U_C.check_visualization=True
                    q1 += xv1.name + xv2.name
                else:
                    q2 += xv1.name + xv2.name
                    U_C.check_visualization=False
            else:
                if xv1.included_in_calculation:
                    q3 += xv1.name
                    U_C.check_visualization=True
                else:
                    q4 += xv1.name
                    U_C.check_visualization=False
                    
            if xv1.initial_event_on_top_sign or xv1.initial_event_on_bottom_sign:
                if xv2 == None:
                    U_C.from_xcoord = xv1.initial_event_graph_top_x_conn
                    U_C.from_ycoord = xv1.initial_event_graph_top_y_conn
                    U_C.to_xcoord = xv1.graph_top_x_conn
                    U_C.to_ycoord = xv1.graph_top_y_conn
                    if xv1.initial_event_on_bottom_sign:
                        U_C.from_xcoord = xv1.graph_top_x_conn
                        U_C.from_ycoord = xv1.graph_top_y_conn
                        U_C.to_xcoord = xv1.initial_event_graph_bottom_x_conn
                        U_C.to_ycoord = xv1.initial_event_graph_bottom_y_conn
                else:
                    U_C.from_xcoord = xv1.graph_bottom_x_conn
                    U_C.from_ycoord = xv1.graph_bottom_y_conn
        
                    U_C.to_xcoord = xv2.graph_top_x_conn
                    U_C.to_ycoord = xv2.graph_top_y_conn
            else:
                U_C.from_xcoord = xv1.graph_bottom_x_conn
                U_C.from_ycoord = xv1.graph_bottom_y_conn
        
                U_C.to_xcoord = xv2.graph_top_x_conn
                U_C.to_ycoord = xv2.graph_top_y_conn
            
            U_C.text_xcoord = calc.position_for_text_x_calc(U_C.from_xcoord, U_C.to_xcoord)
            U_C.text_ycoord = calc.position_for_text_y_calc(U_C.from_xcoord, U_C.to_xcoord, U_C.from_ycoord, U_C.to_ycoord)
           
            if U_C.parametrization:
                if U_C.dist_typ == 'Normal' or U_C.dist_typ == 'LogNormal':
                    U_C.weight = U_C.dist_par1
                elif U_C.dist_typ == 'Beta':
                    U_C.weight = calc.Beta_av(U_C.dist_par1, U_C.dist_par2)
                elif U_C.dist_typ == 'Gamma':
                    U_C.weight = calc.Gamma_av(U_C.dist_par1, U_C.dist_par2)
                else:
                    U_C.weight = calc.Uniform_av(U_C.dist_par1, U_C.dist_par2)
            
            if U_C.res_taken_from_FT:
                gr_u1 = Graph.objects.get(name=U_C.res_taken_from_FT_name)
                U_C.parametrization = gr_u1.parametrization
                U_C.dist_typ = gr_u1.dist_typ
                U_C.dist_par1 = gr_u1.dist_par1
                U_C.dist_par2 = gr_u1.dist_par2
                U_C.weight = gr_u1.res
                U_C.weight_uncertain = gr_u1.uncertain
                
                
            U_C.save()
        
        calc.Graph_Initialization()
        
        #list of results formation
        res_graph = []
        for res_id in range(len(Gr1.simpl_chains_listing)):
            res_graph.append('')
            str1 = Gr1.simpl_chains_listing[res_id] + ' contribution = ' + str(Gr1.simpl_chains_contrib[res_id])
            res_graph[res_id] = str1            
        
        if request.method == 'POST':
            calcul_incl = False
            for X_V in a_list:
                calcul_incl = request.POST.get('vertice_' + X_V.name + '_calcul')
                if calcul_incl:
                    X_V.included_in_calculation = True
                    calcul_incl = False
                else:
                    X_V.included_in_calculation = False
                    calcul_incl = False
            
                X_V.save()
            
            for U_C in a2_list:
                xv1 = None
                xv2 = None
                uu = U_C.vertices_connected_ident
                xv1 = X_Vertice.objects.get(name=uu[0])
                if len(uu) == 2:
                    xv2 = X_Vertice.objects.get(name=uu[1])
                    if xv1.included_in_calculation and xv2.included_in_calculation:
                        U_C.check_visualization=True
                        q1 += xv1.name + xv2.name
                    else:
                        q2 += xv1.name + xv2.name
                        U_C.check_visualization=False
                else:
                    if xv1.included_in_calculation:
                        q3 += xv1.name
                        U_C.check_visualization=True
                    else:
                        q4 += xv1.name
                        U_C.check_visualization=False
            
                if not U_C.should_be_calculated_sign:
                    if not U_C.res_taken_from_FT:
                        if U_C.parametrization:
                            U_C.dist_typ = request.POST.get('probability_distr_type_for_chain_' + U_C.name)
                            U_C.dist_par1 = float(request.POST.get('chain_' + U_C.name +  '_probab_1_calcul'))
                            U_C.dist_par2 = float(request.POST.get('chain_' + U_C.name +  '_probab_2_calcul'))
                    
                            if U_C.dist_typ == 'Normal' or U_C.dist_typ == 'LogNormal':
                                U_C.weight = U_C.dist_par1
                            elif U_C.dist_typ == 'Beta':
                                U_C.weight = calc.Beta_av(U_C.dist_par1, U_C.dist_par2)
                            elif U_C.dist_typ == 'Gamma':
                                U_C.weight = calc.Gamma_av(U_C.dist_par1, U_C.dist_par2)
                            else:
                                U_C.weight = calc.Uniform_av(U_C.dist_par1, U_C.dist_par2)
                        if not U_C.parametrization:
                            U_C.weight = float(request.POST.get('chain_' + U_C.name + '_calcul'))
                            U_C.weight_uncertain = float(request.POST.get('chain_' + U_C.name +  '_uncert_calcul'))                
                
                if U_C.res_taken_from_FT:
                    gr_u1 = Graph.objects.get(name=U_C.res_taken_from_FT_name)
                    U_C.parametrization = gr_u1.parametrization
                    U_C.dist_typ = gr_u1.dist_typ
                    U_C.dist_par1 = gr_u1.dist_par1
                    U_C.dist_par2 = gr_u1.dist_par2
                    U_C.weight = gr_u1.res
                    U_C.weight_uncertain = gr_u1.uncertain
                
                U_C.save()
            
            calc.Graph_Initialization()
            
            #list of results formation
            res_graph = []
            for res_id in range(len(Gr1.simpl_chains_listing)):
                res_graph.append('')
                str1 = Gr1.simpl_chains_listing[res_id] + ' contribution = ' + str(Gr1.simpl_chains_contrib[res_id])
                res_graph[res_id] = str1                
            
        context = {'X_Vertice_list': a_list, 'Graph': Gr1, 'U_chain_list': a2_list, 'constants': C_V, 'q1': q1,  'q2': q2,  'q3': q3,  'q4': q4, 'res_graph': res_graph}
        return render(request, 'fault_tree.html', context)
    
@login_required()
def science_logout(request):
    logout(request)
    return HttpResponse("You are logged out.")


def science_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request = request, username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('science_base'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'science_login.html', {})
