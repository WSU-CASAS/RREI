class cont_mdp(object):
    """
    MDP example
    """
    def __init__(self,states,actions,state_action):
        self.states=states
        self.actions=actions
        self.state_action=state_action
        # print("state in the class init", self.states)
        # ['13|30|221', '12|16|184', '6|18|197', '12|24|270', 
        #generate uniform policy
        self.uniform_policy={}
        grid_set=set()
        for state in self.states:
            items=state.split('|')
            grid_set.add('|'.join(items[:2])) #'13|30'
        grids=list(grid_set)

        #'13|30'; for each cell in the grid. 
        for grid in grids:
            policy={}
            grid_l=list(map(int,grid.split('|')))
            x=grid_l[0]
            y=grid_l[1]
            acts=[]
            # i = -1, 0, 1
            for i in range(-1,2):
                # j = -1, 0, 1
                for j in range(-1,2):
                    # it will have 9 directions? 
                    acts.append('|'.join(map(str,[x+i,y+j])))
            for act in acts:
                policy[act]=1/9
            self.uniform_policy[grid]=policy

