from django.contrib.postgres.fields import ArrayField
from django.db import models

class Graph(models.Model):
    name = models.CharField(max_length=50)
    FT_attribute = models.BooleanField(default = False)
    main_Graph_connection_vertice_name = models.CharField(max_length=50, default="None")
    descr = models.TextField()
    res = models.FloatField(default = 0.0)
    uncertain = models.FloatField(default = 0.0)
    
    parametrization = models.BooleanField(default = False)
    
    dist_typ = models.CharField(max_length=10, default = 'Normal')
    dist_par1 = models.FloatField(default = 0.0)
    dist_par2 = models.FloatField(default = 0.0)
    
    simpl_chains_listing = ArrayField(models.CharField(max_length=1000), default=['None',])
    simpl_chains_contrib = ArrayField(models.FloatField(), default=['0.0',])
    
    max_level = models.IntegerField(default = 5)
    max_position = models.IntegerField(default = 5)
    max_y_coord = models.IntegerField(default = 1)
    max_x_coord = models.IntegerField(default = 1)

    def __str__(self):
        return self.name

class U_chain(models.Model):
    name = models.CharField(max_length=50)
    in_Graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    vertices_connected_ident = ArrayField(models.CharField(max_length=50), default=['None',])
    initial_event_sign = models.BooleanField(default = False)
    should_be_calculated_sign = models.BooleanField(default = False)
    check_visualization = models.BooleanField(default = True)
    
    res_taken_from_FT = models.BooleanField(default = False)
    res_taken_from_FT_name = models.CharField(max_length=50, default = 'None')
    
    chain_color = models.CharField(max_length=7)
    
    weight = models.FloatField(default = 0.0)
    weight_uncertain = models.FloatField(default = 0.0)
    
    parametrization = models.BooleanField(default = False)
    
    probability_distributions = [
        ('Normal', 'Normal'),
        ('LogNormal', 'LogNormal'),
        ('Beta', 'Beta'),
        ('Gamma', 'Gamma'),
        ('Uniform', 'Uniform'),
        ]
    
    dist_typ = models.CharField(max_length=10, choices=probability_distributions, default = 'Normal')
    dist_par1 = models.FloatField(default = 0.0)
    dist_par2 = models.FloatField(default = 0.0)
    
    # visualization part is taken from the X_Vertice items 
    from_xcoord = models.IntegerField(default = 1)
    from_ycoord = models.IntegerField(default = 1)
    to_xcoord = models.IntegerField(default = 1)
    to_ycoord = models.IntegerField(default = 1)
    text_xcoord = models.IntegerField(default = 1)
    text_ycoord = models.IntegerField(default = 1)

class X_Vertice(models.Model):
    name = models.CharField(max_length=50)
    in_Graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    level_in_Graph = models.IntegerField()
    position_in_Graph = models.IntegerField()
    included_in_calculation = models.BooleanField(default = True)
    check_visualization = models.BooleanField(default = True)
    chains_connected_ident = ArrayField(models.CharField(max_length=50), default=['None',])
    contained_FT_Graph = models.BooleanField(default = False)
    connected_FT_Graph_name = models.CharField(max_length=50, default = "None")
    
    # visualization part
    graph_xcoord = models.IntegerField(default = 1)
    graph_ycoord = models.IntegerField(default = 1)
    graph_top_x_conn = models.IntegerField(default = 1)
    graph_bottom_x_conn = models.IntegerField(default = 1)
    graph_top_y_conn = models.IntegerField(default = 1)
    graph_bottom_y_conn = models.IntegerField(default = 1)
    
    initial_event_on_top_sign = models.BooleanField(default = False)
    initial_event_on_bottom_sign = models.BooleanField(default = False)
    initial_event_graph_bottom_x_conn = models.IntegerField(default = 1)
    initial_event_graph_bottom_y_conn = models.IntegerField(default = 1)
    initial_event_graph_top_x_conn = models.IntegerField(default = 1)
    initial_event_graph_top_y_conn = models.IntegerField(default = 1)
    
class Const_visual(models.Model):
    x0 = models.IntegerField(default = 10)
    y0 = models.IntegerField(default = 10)
    step_x_pos = models.IntegerField(default = 500)
    step_y_pos = models.IntegerField(default = 420)
