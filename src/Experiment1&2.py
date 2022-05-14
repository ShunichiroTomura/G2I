
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class SCSP:
    
    def __init__(self):
        #declare true, false value with the result container
        self.true = 1
        self.false = 0
        self.c_result = []
        
    def additive(self, elements):
        # normal logical or (if any of the results contains 1, then it returns 1) by following the definition
        if 1 in elements:
            return self.true
        else:
            return self.false
        
    def multiplicative(self, elements):
        # normal logical and (iff all the results contains 1, then it returns 1) by following the definition
        if 0 in elements:
            return self.false
        else:
            return self.true

    def variable_check(self, goal_elements, elements):
        #check whether each value from an actual project matches with the target's
        
        #check whether the total number of values in the actually observed goal 
        #is the same with that in the target goal 
        if len(goal_elements) != len(elements):
            print("the number of c_element is not the same as the number of elements")
            exit(0)
        
        #1 is returned iff the value in the values from the target goal is
        #the samw with that from the actually observed goal
        c_result = []
        for i in range(len(goal_elements)):
            if goal_elements[i] == elements[i]:
                c_result.append(self.true)
            else:
                c_result.append(self.false)
        #store the check result   
        self.c_result.append(self.multiplicative(c_result))

    
    def get_c_result(self):
        return self.c_result
    
    def reset(self):
        self.c_result = []

class FCSP:
    def __init__(self):
        #declare true, false value with the result container
        self.true = 1
        self.false = 0
        self.c_result = []
        
    def additive(self, elements):
        #return the maximum value by following the definition
        return max(elements)
        
    def multiplicative(self, elements):
        #return the minimum value by following the definition
        return min(elements)

    def variable_check(self, goal_elements, elements, fuzzy_level):
        #check whether each value from an actual project matches with the target variable's
        
        #check whether the total number of values in the actually observed goal 
        #is the same with that in the target goal 
        if len(goal_elements) != len(elements):
            print("the number of c_element is not the same as the number of elements")
            exit(0)
        
        #define an example fuzzy situation by applying membership function
        c_result = []
        for i in range(len(goal_elements)):
            #if the actual value is lower or higher than the taget value with fuzzy level,
            #then it returns 0
            if goal_elements[i]-fuzzy_level[i] >= elements[i] or goal_elements[i]+fuzzy_level[i]  <= elements[i] :
                c_result.append(self.false)
            #if the actual value is between the (target value - fuzzy level) and the target value,
            #then, the returning value becomes closer to one as the value gets closer to the target value 
            elif (goal_elements[i]-fuzzy_level[i]  < elements[i]) and (goal_elements[i] > elements[i]):
                c_result.append((elements[i]-(goal_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
            # if the actual value is the same with the target value, then it returns 1
            elif goal_elements[i] == elements[i]:
                c_result.append(self.true)
            #if the actual value is between the (target value + fuzzy level) and the target value,
            #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
            else:
                c_result.append((goal_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
        #store the check result   
        self.c_result.append(self.multiplicative(c_result))
   
    def get_c_result(self):
        return self.c_result
    
    def reset(self):
        self.c_result = []

class WCSP:
    def __init__(self):
        #declare true, false value with the result container
        self.true = 1
        self.false = 0
        self.c_result = []
        
    def additive(self, elements):
        #return the sum value by following the definition
        return max(elements)
    
    def multiplicative(self, element):
        return sum(element)

    def variable_check(self, goal_elements, elements, fuzzy_level, weights):
        #check whether each value from an actual project matches with target variable's
        
        #check whether the total number of values in the actually observed goal 
        #is the same with that in the target goal 
        if len(goal_elements) != len(elements):
            print("the number of c_element is not the same as the number of elements")
            exit(0)
        
        #define an example fuzzy situation by applying membership function
        c_result = []
        for i in range(len(goal_elements)):
            #if the actual value is lower or higher than the taget value with fuzzy level,
            #then it returns 0
            if goal_elements[i]-fuzzy_level[i] >= elements[i] or goal_elements[i]+fuzzy_level[i]  <= elements[i] :
                c_result.append((self.false)*weights[i])
            #if the actual value is between the (target  value - fuzzy level) and the target value,
            #then, the returning value becomes closer to one as the value gets closer to the target value 
            elif (goal_elements[i]-fuzzy_level[i]  < elements[i]) and (goal_elements[i] > elements[i]):
                c_result.append(((elements[i]-(goal_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
            # if the actual value is the same with the target value, then it returns 1
            elif goal_elements[i] == elements[i]:
                c_result.append((self.true)*weights[i])
            #if the actual value is between the (target value + fuzzy level) and the target value,
            #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
            else:
                c_result.append(((goal_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
        #store the check result   
        self.c_result.append(self.multiplicative(c_result))
   
    def get_c_result(self):
        return self.c_result
    
    def reset(self):
        self.c_result = []

class QCSP:
    def __init__(self):
        #declare true, false value with the result container
        self.char_to_num ={"cold":1,"cool":2,"moderate":3,"warm":4,"hot":5}
        self.num_to_char = {1:"cold",2:"cool",3:"moderate",4:"warm",5:"hot"}
        self.c_result = []
        
    def additive(self, elements):
        #return the maximum value by following the definition
        tmp = []
        for i in range(len(elements)):
            tmp.append(self.char_to_num[elements[i]])
        return self.num_to_char[max(tmp)]
        
    def multiplicative(self, elements):
        #return the minimum value by following the definition
        tmp = []
        for i in range(len(elements)):
            tmp.append(self.char_to_num[elements[i]])
        return self.num_to_char[min(tmp)]

    def variable_check(self, goal_elements, elements):
        #check whether each value from an actual project matches with target variable's
        
        #check whether the total number of values in the actually observed goal 
        #is the same with that in the target goal 
        if len(goal_elements) != len(elements):
            print("the number of c_element is not the same as the number of elements")
            exit(0)
        
        #define an example fuzzy situation by applying membership function
        c_result = []
        for i in range(len(goal_elements)):
            #conver the value into predefined qualitative value
            c_result.append(self.num_to_char[elements[i]])
        #store the check result   
        self.c_result.append(self.multiplicative(c_result))
   
    def get_c_result(self):
        return self.c_result
    
    def reset(self):
        self.c_result = []

#read goal data
data_goal = pd.read_csv(
            "goals_boolean.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
            names=["index","var_target", "var_actual", "result"]
        )

#read edge data
data_edges = pd.read_csv(
            "edges.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
        )

print(data_goal)
print(data_edges)

# find parents and children nodes
goal_parents_original = []
goal_children = []
for i in range(len(data_goal)):
    if np.isnan(data_goal.iloc[i,2]):
        goal_parents_original.append(i)
    else:
        goal_children.append(i)

print(goal_parents_original)
print(goal_children)

#define a c-semiring type
csp = SCSP()

# check the satisfiability level of each children node
MAX_VAR_NUM = 1
for i in range(len(goal_children)):
    var_target = []
    var_actual = []
    for j in range(MAX_VAR_NUM):
        if np.isnan(data_goal.iloc[goal_children[i],j+1]):
            break
        else:
            var_target.append(data_goal.iloc[goal_children[i],j+1])
            var_actual.append(data_goal.iloc[goal_children[i],j+1+MAX_VAR_NUM])
    csp.variable_check(var_target, var_actual)
    data_goal.iloc[goal_children[i],-1] = csp.multiplicative(csp.get_c_result())
    csp.reset()

#based on the result from the children nodes, we calculate the satisfiability of parent goals
goal_parents = goal_parents_original.copy()
while True:
    if len(goal_parents) == 0:
        break
    parents =[]
    for i in range(len(goal_parents)):
        cnt = 0
        children = []
        for j in range(len(data_edges)):
            if data_edges.iloc[j,goal_parents[i]] == 1:
                if np.isnan(data_goal.iloc[j, -1]) == False:
                    cnt += 1
                    children.append(j)
        if cnt == data_edges.iloc[:,goal_parents[i]].sum():
            children_result = []
            for k in range(len(children)):
                children_result.append(data_goal.iloc[children[k],-1])
            data_goal.iloc[goal_parents[i],2] = csp.multiplicative(children_result)
            data_goal.iloc[goal_parents[i],3] = csp.multiplicative(children_result)
            csp.reset()
            parents.append(i)
    for i in range(len(parents)):
        goal_parents.remove(parents[i])

print(data_goal)

#display the result as a graph
G = nx.DiGraph()

for i in range(len(data_goal)):
    G.add_node(data_goal.index[i])

for i in range(len(data_edges)):
    for j in range(len(data_edges.iloc[0,:])):
        if data_edges.iloc[i,j] == 1:
            G.add_edges_from([(i, j)])

labels = {}           
for i in range(len(data_goal)):
    labels[i] = "{" + str(data_goal.iloc[i,0]) + ": " + str(round(data_goal.iloc[i,-1],2)) + "}"
    
nx.draw_spectral(G, labels=labels, with_labels=True,font_weight='normal',arrowsize=15, font_size=15)
plt.show()


#===actual algorithm1===#
#read new goals
data_new_goal = pd.read_csv(
            "new goals.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
            names=["index","var_target", "var_actual", "result"]
        )

#check the satisfiability level of each goal
for i in range(len(data_new_goal)):
    var_target = []
    var_actual = []
    for j in range(MAX_VAR_NUM):
        print(j)
        if np.isnan(data_new_goal.iloc[i,j+1]):
            break
        else:
            var_target.append(data_new_goal.iloc[i,j+1])
            var_actual.append(data_new_goal.iloc[i,j+1+MAX_VAR_NUM])
    csp.variable_check(var_target, var_actual)
    data_new_goal.iloc[i,3] = csp.multiplicative(csp.get_c_result())
    csp.reset()

print(data_new_goal)

#choose a target goal
TARGET_GOAL = 3

#choose the highest satisfiability goal and replace the target goal with it
for i in range(len(data_new_goal)):
    print(i)
    if csp.additive([data_goal.iloc[TARGET_GOAL, -1], data_new_goal.iloc[i, -1]]) == data_new_goal.iloc[i, -1]:
        for j in range(len(data_goal.iloc[0,:])):
            data_goal.iloc[TARGET_GOAL,j] = data_new_goal.iloc[i,j]

#reset the result of parent goals for updating
for i in range(len(goal_parents_original)):
    data_goal.iloc[goal_parents_original[i],-1] = np.nan

#recalculate the satisfiability of parents goals 
goal_parents = goal_parents_original.copy()
while True:
    if len(goal_parents) == 0:
        break
    parents =[]
    for i in range(len(goal_parents)):
        cnt = 0
        children = []
        for j in range(len(data_edges)):
            if data_edges.iloc[j,goal_parents[i]] == 1:
                if np.isnan(data_goal.iloc[j, -1]) == False:
                    cnt += 1
                    children.append(j)
        if cnt == data_edges.iloc[:,goal_parents[i]].sum():
            children_result = []
            for k in range(len(children)):
                children_result.append(data_goal.iloc[children[k],-1])
            data_goal.iloc[goal_parents[i],2] = csp.multiplicative(children_result)
            data_goal.iloc[goal_parents[i],3] = csp.multiplicative(children_result)
            csp.reset()
            parents.append(i)
    for i in range(len(parents)):
        goal_parents.remove(parents[i])

print(data_goal)

#display the result as a graph
G = nx.DiGraph()

for i in range(len(data_goal)):
    G.add_node(data_goal.index[i])

for i in range(len(data_edges)):
    for j in range(len(data_edges.iloc[0,:])):
        if data_edges.iloc[i,j] == 1:
            G.add_edges_from([(i, j)])

labels = {}           
for i in range(len(data_goal)):
    labels[i] = "{" + str(data_goal.iloc[i,0]) + ": " + str(round(data_goal.iloc[i,-1],2)) + "}"
    
nx.draw_spectral(G, labels=labels, with_labels=True, font_weight='normal',arrowsize=15, font_size=15)
plt.show()

    


