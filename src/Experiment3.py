# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:40:42 2022

@author: Shunichiro Tomura
"""

import numpy as np
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
        #print(goal_elements)
        #print(elements)
        #print(c_result)
        #print(self.multiplicative(c_result))
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

"""    
class PCSP:
    def __init__(self):
        #declare true, false value with the result container
        self.true = 1
        self.false = 0
        self.c_result = []
        
    def additive(self, elements):
        #return max by following the definition
        return max(elements)
        
    def multiplicative(self, elements):
        #return multiplication of each probability by following the definition
        return np.prod(elements)

    def variable_check(self, goal_elements, elements, probability):
        #check whether each value from an actual project matches with target variable's
        
        #check whether the total number of values in the actually observed goal 
        #is the same with that in the target goal 
        if len(goal_elements) != len(elements):
            print("the number of c_element is not the same as the number of elements")
            exit(0)
            
        c_result = []
        #check whether each actual value is correct
        #in reality, this is conducted by assessing observed data 
        #but here uses A~E as observed values and simulate
        for i in range(len(goal_elements)):
           #check whether the value is correct 
           #here uses simulation instead
           if elements[i] == 'E':
               #if the observed values is not allowe (in this case, E is an out-of-rule value), 
               #then the probability takes 1-P(check)
               #each of variable has a chance to get E with 20% probability
               c_result.append(1-probability[i])
           else:
               #if it is allowed, then the probability takes 1
               c_result.append(probability[i]) 
        #store the check result 

        self.c_result.append(self.multiplicative(c_result))
     
    def get_c_result(self):
        return self.c_result
    
    def reset(self):
        self.c_result = [] 
   
class target_goal:
    def __init__(self, index, c_elements):
        #target goal objects
        self.index = index
        self.c_elements = c_elements
"""

import pandas as pd

data_goal = pd.read_csv(
            "goals.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["index","var_target", "var_actual", "result"]
        )

data_edges = pd.read_csv(
            "edges.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            #names=["index","var"]
        )
        

import networkx as nx
import matplotlib.pyplot as plt

#goal2 = target_goal(2,[1])   
#goal3 = target_goal(3,[1])       
#goal1 = target_goal(1,[goal2,goal3])

print(data_goal)
print(data_edges)

goal_parents_original = []
goal_children = []
for i in range(len(data_goal)):
    if np.isnan(data_goal.iloc[i,2]):
        goal_parents_original.append(i)
    else:
        goal_children.append(i)

print(goal_parents_original)
print(goal_children)

#goals_target =[]
#for i in range(len(data_goal)):
#    goals_target.append(target_goal(data_goal.iloc[i,0],[data_goal.iloc[i,1]]))

#print(goals_target[0].index)

csp = WCSP()

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
    csp.variable_check(var_target, var_actual,[0.5],[2])
    data_goal.iloc[goal_children[i],-1] = csp.multiplicative(csp.get_c_result())
    csp.reset()

#print(data_goal)
#print(len(data_edges.iloc[:,0]))
goal_parents = goal_parents_original.copy()
while True:
    if len(goal_parents) == 0:
      #  print('D')
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
        #print(cnt)
        if cnt == data_edges.iloc[:,goal_parents[i]].sum():
            children_result = []
            for k in range(len(children)):
                children_result.append(data_goal.iloc[children[k],-1])
            data_goal.iloc[goal_parents[i],2] = csp.multiplicative(children_result)
            data_goal.iloc[goal_parents[i],3] = csp.multiplicative(children_result)
            csp.reset()
            #print('a')
            parents.append(i)
    #print(parents)
    #print(goal_parents)
    for i in range(len(parents)):
        goal_parents.remove(parents[i])

print(data_goal)
        
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


#======#
data_new_goal = pd.read_csv(
            "new goals.csv",
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["index","var_target", "var_actual", "result"]
        )


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
    csp.variable_check(var_target, var_actual,[0.5],[2])
    data_new_goal.iloc[i,3] = csp.multiplicative(csp.get_c_result())
    csp.reset()

print(data_new_goal)

TARGET_GOAL = 3

for i in range(len(data_new_goal)):
    print(i)
    if csp.additive([data_goal.iloc[TARGET_GOAL, -1], data_new_goal.iloc[i, -1]]) == data_new_goal.iloc[i, -1]:
        for j in range(len(data_goal.iloc[0,:])):
            data_goal.iloc[TARGET_GOAL,j] = data_new_goal.iloc[i,j]

for i in range(len(goal_parents_original)):
    data_goal.iloc[goal_parents_original[i],-1] = np.nan

#print(data_goal)


goal_parents = goal_parents_original.copy()
while True:
    if len(goal_parents) == 0:
      #  print('D')
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
        #print(cnt)
        if cnt == data_edges.iloc[:,goal_parents[i]].sum():
            children_result = []
           # print(children)
            for k in range(len(children)):
                children_result.append(data_goal.iloc[children[k],-1])
            data_goal.iloc[goal_parents[i],2] = csp.multiplicative(children_result)
            data_goal.iloc[goal_parents[i],3] = csp.multiplicative(children_result)
            csp.reset()
            #print('a')
            parents.append(i)
    #print(parents)
   # print(goal_parents)
    for i in range(len(parents)):
        goal_parents.remove(parents[i])
   # print(data_goal)

print(data_goal)
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

#G = nx.DiGraph()

#G.add_node(goal2.index, label ="{" + str(goal2.index) + ":" + str(goal2.c_elements) + "}")
#G.add_node(goal3.index, label ="{" + str(goal3.index) + ":" + str(goal3.c_elements) + "}")
#G.add_node(goal1.index, label ="{" + str(goal1.index) + ":" + str(goal1.c_elements) + "}")

#G.add_edges_from([(goal2.index, goal1.index)])
#G.add_edges_from([(goal3.index, goal1.index)])

#labels = nx.get_node_attributes(G, 'label') 

#nx.draw_spectral(G, labels=labels, with_labels=True, font_weight='bold')

        

#if MODE = 1:
    


