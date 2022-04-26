

#1:SCSP, 2:FCSP, 3:WCSP, 4:Fuzzy&Weight CSP, 5:PCSP, 6:N-dimension CSPs
MODE = 4 

if MODE == 1:
    class SCSP:
        
        def __init__(self):
            #declare true, false value with the constrain result container
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
    
        def constraint_check(self, goal, elements):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #1 is returned iff the value in the constraint values from the target goal is
            #the samw with that from the actually observed goal
            c_result = []
            for i in range(len(goal.c_elements)):
                if goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                else:
                    c_result.append(self.false)
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
            print()
        
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        #target goal objects
        def __init__(self, c_elements):
            self.c_elements = c_elements
            
    #declare goals with target constraint values        
    target_goals = [target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1])]
   
    #declare actual goals with observed values
    goals_actual = [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]]
    
    #create a SCSP
    scsp = SCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        scsp.constraint_check(target_goals[i], goals_actual[i])
    
    print("Individual goal achievement: " + str(scsp.get_indi_goal_check_result()))
    
    #check the constraint check result from all the actual goals  
    IsAchieved = scsp.multiplicative(scsp.c_result)
    print("Cumulative goal achievement: " + str(IsAchieved))

elif MODE == 2:
    
    class FCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the maximum value by following the definition
            return max(elements)
            
        def multiplicative(self, elements):
            #return the minimum value by following the definition
            return min(elements)
    
        def constraint_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
            
    #declare goals with target constraint values         
    target_goals = [target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1])]
    
    #declare actual observed goals with observed values
    goals_actual = [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]]
    
    #declare fuzzy level for each constraint value
    #to make it easier, 0.5 is used for all constraint values
    fuzzy_levels=[[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]]
    
    #create a FCSP
    fcsp = FCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        fcsp.constraint_check(target_goals[i], goals_actual[i],fuzzy_levels[i])
    
    print("Individual goal achievement: " + str(fcsp.get_indi_goal_check_result()))
    
    #check the constraint check result from all the actual goals  
    IsAchieved = fcsp.multiplicative(fcsp.c_result)
    print("Cumulative goal achievement: " + str(IsAchieved))

elif MODE == 3:
    
    class WCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the sum value by following the definition
            return sum(elements)
        
        def minimum(self, element):
            return min(element)
    
        def constraint_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((1-(goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
            #store the check result   
            self.c_result.append(self.additive(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
            
    #declare goals with target constraint values         
    target_goals = [target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1])]
    
    #declare actual observed goals with observed values
    goals_actual = [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]]
    
    #declare fuzzy level for each constraint value
    #to make it easier, 0.5 is used for all constraint values
    fuzzy_levels=[[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]]
    
    #weights for all constraint values
    weights=[[2,4,6,8,10],[2,4,6,8,10],[2,4,6,8,10]]
    
    #create a WCSP
    wcsp = WCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        wcsp.constraint_check(target_goals[i], goals_actual[i],fuzzy_levels[i],weights[i])
    
    print("Individual goal achievement: " + str(wcsp.get_indi_goal_check_result()))
    
    #check the constraint check result from all the actual goals  
    IsAchieved = wcsp.minimum(wcsp.c_result)
    print("Cumulative goal achievement: " + str(IsAchieved))
    
elif MODE == 4:
    
    class FW_FCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def maximum(self, elements):
            #return the maximum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(tmp[0])):
                remove =[]
                extracted = [row[i] for row in tmp]
                maximum = max(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != maximum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
                        
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp

            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)
     
            return index, tmp
                                        
                        
        def minimum(self, elements):
             #return the minimum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(elements[0])-1):
                remove =[]
                extracted = [row[i] for row in tmp]
                minimum = min(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != minimum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
  
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp
             
            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)

            tmp[0][len(tmp[0])-1] = sum([row[len(tmp)-1] for row in tmp])
            return index, tmp
    
        def constraint_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
            #store the check result   
            self.c_result.append(c_result)
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class FW_WCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def maximum(self, elements):
            #return the maximum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(tmp[0])):
                remove =[]
                extracted = [row[i] for row in tmp]
                maximum = max(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != maximum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
                        
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp

            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)
     
            return index, tmp[0]
                                                              
        def minimum(self, elements):
             #return the minimum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(elements[0])-1):
                remove =[]
                extracted = [row[i] for row in tmp]
                minimum = min(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != minimum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
  
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp
             
            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)

            tmp[0][len(tmp[0])-1] = sum([row[len(tmp)-1] for row in tmp])
            return index, tmp[0]
    
        def constraint_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((1-(goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
            #store the check result   
            self.c_result.append(c_result)
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
        
    #declare goals with target constraint values         
    target_goals = [target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1])]
    
    #declare actual observed goals with observed values
    goals_actual = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
    
    #declare fuzzy level for each constraint value
    #to make it easier, 0.5 is used for all constraint values
    fuzzy_levels=[[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]]
    
    #create a FCSP
    fcsp = FW_FCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        fcsp.constraint_check(target_goals[i], goals_actual[i],fuzzy_levels[i])

    print("Cumulative goal achievement: " + "goal " + str(fcsp.minimum(fcsp.get_indi_goal_check_result())[0]) + ' ' + 
          str((fcsp.minimum(fcsp.get_indi_goal_check_result())[1][0])))

    
    #weights for all constraint values
    weights=[[2,4,6,8,10],[2,4,6,8,10],[2,4,6,8,10]]
    
    #create a WCSP
    wcsp = FW_WCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        wcsp.constraint_check(target_goals[i], goals_actual[i],fuzzy_levels[i],weights[i])
    
    print("Cumulative goal achievement: " + "goal " + str(wcsp.minimum(wcsp.get_indi_goal_check_result())[0]) + ' ' + 
          str((wcsp.minimum(wcsp.get_indi_goal_check_result())[1])))


elif MODE == 5:
    import numpy as np
    import random
    class PCSP:
        
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return max by following the definition
            return max(elements)
            
        def multiplicative(self, elements):
            #return multiplication of each probability by following the definition
            return np.prod(elements)
    
        def constraint_check(self, goal, elements, probability):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
                
            c_result = []
            #check whether each actual value is allowed by the constraint
            #in reality, this is conducted by assessing observed data 
            #but here uses random values as simulation
            for i in range(len(goal.c_elements)):
               #check whether the value is allowed by the constraint 
               #here uses simulation instead
               n = random.randint(1,5)
               if n <= 4:
                   #if it is allowed, then the probability takes 1
                   c_result.append(self.true)
               else:
                   #if not, then the probability takes 1-P(constraint)
                   c_result.append(1-probability[i]) 
            #store the check result                  
            self.c_result.append(self.multiplicative(c_result))
         
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
            
    #declare goals with target constraint values 
    target_goals = [target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1]), target_goal([1,1,1,1,1])]
    
    #declare actual goals with observed values
    #in reality, meaningful observed data to determine whether the value is allowed is assigned
    #in this example, since this allowing check is simulated randomly and hence meaningless information is assigned instead 
    goals_actual = [['1?','1?','1?','1?','1?'],['1?','1?','1?','1?','1?'],['1?','1?','1?','1?','1?']]
    
    #constraint probability for each constrain in each project
    #to make it simpler, the same constrain probability is used for every constraint in each project 
    probability=[[0.6,0.6,0.6,0.6,0.6],[0.6,0.6,0.6,0.6,0.6],[0.6,0.6,0.6,0.6,0.6]]
    
    #create a PCSP
    pcsp = PCSP()
    
    #constraint check for all the values in each goal
    for i in range(len(target_goals)):
        pcsp.constraint_check(target_goals[i], goals_actual[i],probability[i])
    
    #check the constraint check result from all the actual goals  
    IsAchieved = pcsp.multiplicative(pcsp.c_result)  
    print("Individual goal achievement: " + str(pcsp.get_indi_goal_check_result()))
    
    #check the constraint check result from all the actual goals  
    IsAchieved = pcsp.multiplicative(pcsp.c_result)
    print("Cumulative goal achievement: " + str(IsAchieved))

elif MODE == 6:
    
    import numpy as np
    import random
    
    class SCSP:   
        def __init__(self):
            #declare true, false value with the constrain result container
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
    
        def constraint_check(self, goal, elements):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #1 is returned iff the value in the constraint values from the target goal is
            #the samw with that from the actually observed goal
            c_result = []
            for i in range(len(goal.c_elements)):
                if goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                else:
                    c_result.append(self.false)
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
            
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class FCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the maximum value by following the definition
            return max(elements)
            
        def multiplicative(self, elements):
            #return the minimum value by following the definition
            return min(elements)
    
        def constraint_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
            
        def get_indi_goal_check_result(self):
            return self.c_result
            
    class WCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the sum value by following the definition
            return sum(elements)
        
        def minimum(self, element):
            return min(element)
    
        def constraint_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((1-(goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
            #store the check result   
            self.c_result.append(self.additive(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
      
    class FW_FCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def maximum(self, elements):
            #return the maximum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(tmp[0])):
                remove =[]
                extracted = [row[i] for row in tmp]
                maximum = max(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != maximum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
                        
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp

            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)
     
            return index, tmp                                      
                        
        def minimum(self, elements):
             #return the minimum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(elements[0])-1):
                remove =[]
                extracted = [row[i] for row in tmp]
                minimum = min(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != minimum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
  
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp
             
            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)

            tmp[0][len(tmp[0])-1] = sum([row[len(tmp)-1] for row in tmp])
            return index, tmp
    
        def constraint_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
            #store the check result   
            self.c_result.append(c_result)
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class FW_WCSP:
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def maximum(self, elements):
            #return the maximum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(tmp[0])):
                remove =[]
                extracted = [row[i] for row in tmp]
                maximum = max(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != maximum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
                        
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp

            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)
     
            return index, tmp[0]
                                                              
        def minimum(self, elements):
             #return the minimum value by following the definition    
            index = []
            tmp = elements.copy()
            for i in range(len(elements[0])-1):
                remove =[]
                extracted = [row[i] for row in tmp]
                minimum = min(extracted)
                for j in range(len(extracted)):
                    if extracted[j] != minimum:
                        remove.append(j)
                if len(remove) != 0:
                    for i in range(len(remove)):
                        del tmp[remove[i]-i]
  
                if len(tmp) == 1:
                    for i in range(len(elements)):
                       if elements[i] == tmp[0]:
                          index = i
                    return index, tmp
             
            for i in range(len(elements)):
               if elements[i] == tmp[0]:
                   index.append(i)

            tmp[0][len(tmp[0])-1] = sum([row[len(tmp)-1] for row in tmp])
            return index, tmp[0]
    
        def constraint_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget constraint value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target constraint value - fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to one as the value gets closer to the target constraint value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target constraint value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target constraint value + fuzzy level) and the target constraint value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target constraint value + fuzzy level)
                else:
                    c_result.append((1-(goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
            #store the check result   
            self.c_result.append(c_result)
       
        def get_indi_goal_check_result(self):
            return self.c_result
 
    class PCSP:
        
        def __init__(self):
            #declare true, false value with the constrain result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return max by following the definition
            return max(elements)
            
        def multiplicative(self, elements):
            #return multiplication of each probability by following the definition
            return np.prod(elements)
    
        def constraint_check(self, goal, elements, probability):
            #check whether each value from an actual project satisfies the corresponding constraint
            
            #check whether the total number of constrain values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
                
            c_result = []
            #check whether each actual value is allowed by the constraint
            #in reality, this is conducted by assessing observed data 
            #but here uses random values as simulation
            for i in range(len(goal.c_elements)):
               #check whether the value is allowed by the constraint 
               #here uses simulation instead
               n = random.randint(1,5)
               if n <= 4:
                   #if it is allowed, then the probability takes 1
                   c_result.append(self.true)
               else:
                   #if not, then the probability takes 1-P(constraint)
                   c_result.append(1-probability[i]) 
            #store the check result                  
            self.c_result.append(self.multiplicative(c_result))
            
        def get_indi_goal_check_result(self):
            return self.c_result
       
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
    
     
    #declare goals with target constraint values for classic, fuzzy and probability 
    goal_classic, goal_fuzzy, goal_weight, goal_fw, goal_prob = \
    [target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1])],\
    [target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1])],\
    [target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1])],\
    [target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1])],\
    [target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1]),target_goal([1,1,1,1,1])]
  
    #declare actual goal values for the classic, fuzzy and probablistic goal
    goal_actual_classic, goal_actual_fuzzy, goal_actual_weight, goal_actual_fw, goal_actual_prob = \
    [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]], \
    [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]], \
    [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]], \
    [[1,1,1,1,1],[1,1,0.7,1,1],[1,1,1,1,1]], \
    [['1?','1?','1?','1?','1?'],['1?','1?','1?','1?','1?'],['1?','1?','1?','1?','1?']] 
    
    #declare fuzzy level and probability for corresponding constraint values in the fuzzy and probability target goals 
    fuzzy_level, weight_fuzzy_level, fw_fuzzy_level, probability = \
    [[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]], \
    [[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]], \
    [[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]], \
    [[0.6,0.6,0.6,0.6,0.6],[0.6,0.6,0.6,0.6,0.6],[0.6,0.6,0.6,0.6,0.6]]
    
    #cost for weight and fuzzy_weight model
    fuzzy_cost, weight_fuzzy_cost, fw_cost = [[2,4,6,8,10],[2,4,6,8,10],[2,4,6,8,10]],\
    [[2,4,6,8,10],[2,4,6,8,10],[2,4,6,8,10]],\
    [[2,4,6,8,10],[2,4,6,8,10],[2,4,6,8,10]]
    
    #declare SCSP, FCSP and PCSP
    scsp = SCSP()
    fcsp = FCSP()
    wcsp = WCSP()
    fw_fcsp = FW_FCSP()
    fw_wcsp = FW_WCSP()
    pcsp = PCSP()
   
    
    #conduct constraint check for each value in each classic, fuzzy and probability goals
    for i in range(len(goal_classic)):
        scsp.constraint_check(goal_classic[i], goal_actual_classic[i])
    for i in range(len(goal_fuzzy)):
        fcsp.constraint_check(goal_fuzzy[i], goal_actual_fuzzy[i],fuzzy_level[i])
    for i in range(len(goal_weight)):
        wcsp.constraint_check(goal_weight[i], goal_actual_weight[i],weight_fuzzy_level[i],fuzzy_cost[i])
    for i in range(len(goal_fw)):
        fw_fcsp.constraint_check(goal_fw[i], goal_actual_fw[i],fw_fuzzy_level[i])
    for i in range(len(goal_fw)):
        fw_wcsp.constraint_check(goal_fw[i], goal_actual_fw[i],fw_fuzzy_level[i],fw_cost[i])
    for i in range(len(goal_prob)):
        pcsp.constraint_check(goal_prob[i], goal_actual_prob[i],probability[i])
    
    
    print("Individual goal achievement: ")
    print("binary: "+ str(scsp.get_indi_goal_check_result()))
    print("fuzzy: " + str(fcsp.get_indi_goal_check_result()))    
    print("weight: " + str(wcsp.get_indi_goal_check_result()))
    print("probability: " + str(pcsp.get_indi_goal_check_result()))
    print()
    # there is no individual comparison for fuzzy weight because it is the comparison of goals
    
    print("Cumulative goal achievement: ")
    print("binary: " + str(scsp.multiplicative(scsp.c_result)))
    print("fuzzy: " + str(fcsp.multiplicative(fcsp.c_result)))
    print("weight: " + str(wcsp.minimum(wcsp.c_result)))
    print("fuzzy_weight's fuzzy: goal" + str(fw_fcsp.minimum(fw_fcsp.get_indi_goal_check_result())[0]) + ' ' + 
          str((fw_fcsp.minimum(fw_fcsp.get_indi_goal_check_result())[1][0])))
    print("fuzzy_weight's weight: goal " + str(fw_wcsp.minimum(fw_wcsp.get_indi_goal_check_result())[0]) + ' ' + 
          str((fw_wcsp.minimum(fw_wcsp.get_indi_goal_check_result())[1])))
    print("probability: " + str(pcsp.multiplicative(pcsp.c_result)))
    print()
    
    result = [scsp.multiplicative(scsp.c_result),fcsp.multiplicative(fcsp.c_result),
              wcsp.minimum(wcsp.c_result),[fw_fcsp.minimum(fw_fcsp.get_indi_goal_check_result())[0],
              fw_fcsp.minimum(fw_fcsp.get_indi_goal_check_result())[1][0]],
              [fw_wcsp.minimum(fw_wcsp.get_indi_goal_check_result())[0],
              fw_wcsp.minimum(fw_wcsp.get_indi_goal_check_result())[1]],
              pcsp.multiplicative(pcsp.c_result)]
    
    print("In a list form:")
    print(result)
    