
import pandas as pd
import time

#1:SCSP, 2:FCSP, 3:WCSP, 4:QCSP, 5:PCSP, 6:Integration CSPs
MODE = 6

if MODE == 1:
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
    
        def variable_check(self, goal, elements):
            #check whether each value from an actual goal matches with the target values
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #1 is returned iff the values from the target goal is
            #the same with that from the actually observed goal
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
    
    class target_goal:
        #target goal objects
        def __init__(self, c_elements):
            self.c_elements = c_elements
    
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","weight_label"]
        )
        #set actual goals from the dataset
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([1,1,1,1,1]))
    
        #create a SCSP
        scsp = SCSP()
        
        start = time.time()
        #variable check for all the values in each goal
        for i in range(len(target_goals)):
            scsp.variable_check(target_goals[i], goals_actual[i])
        
        print("Individual goal achievement: " + str(scsp.get_indi_goal_check_result()))
        
        #check the variable check result from all the actual goals  
        IsAchieved = scsp.multiplicative(scsp.c_result)
        print("Cumulative goal achievement: " + str(IsAchieved))
        
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #individual goal
        computed = scsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,5])
        
        i_ct = 0
        for i in range(len(labels)):
            if labels[i] == computed[i]:
                i_ct += 1
        indi_cts.append(i_ct)
        
        c_ct = 0
        if data.iloc[len(data)-1,5] == IsAchieved:
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/REPEAT))
    print("average computational time: " + str(sum(times)/len(times))+"sec")

elif MODE == 2:
    
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
    
        def variable_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual goal matches with the target variable's
            
            #check whether the total number of target values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target value - fuzzy level) and the target value,
                #then, the returning value becomes closer to one as the value gets closer to the target value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target value + fuzzy level) and the target value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
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
            
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","weight_label"]
        )
        
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
                    
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([1,1,1,1,1]))
    
        #declare fuzzy level for each value
        #to make it easier, 0.5 is used for all values
        fuzzy_levels =[]
        for i in range(len(data)-1):
            fuzzy_levels.append([0.5,0.5,0.5,0.5,0.5])

        #create a FCSP
        fcsp = FCSP()
        
        start = time.time()
        #variable check for all the values in each goal
        for i in range(len(target_goals)):
            fcsp.variable_check(target_goals[i], goals_actual[i],fuzzy_levels[i])
        
        print("Individual goal achievement: " + str(fcsp.get_indi_goal_check_result()))
        
        #check the check result from all the actual goals  
        IsAchieved = fcsp.multiplicative(fcsp.c_result)
        print("Cumulative goal achievement: " + str(IsAchieved))
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #individual goal
        computed = fcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,6])
        
        i_ct = 0
        for i in range(len(labels)):
            if labels[i] == round(computed[i],3):
                i_ct += 1
        indi_cts.append(i_ct)
        
        c_ct = 0
        if round(data.iloc[len(data)-1,6],4) == round(IsAchieved,4):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/REPEAT))
    print("average computational time: " + str(sum(times)/len(times))+"sec")


elif MODE == 3:
    
    class WCSP:
        def __init__(self):
            #declare true, false value with the result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the sum value by following the definition
            return sum(elements)
        
        def minimum(self, element):
            return min(element)
    
        def variable_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual goal matches with the target's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target value - fuzzy level) and the target value,
                #then, the returning value becomes closer to one as the value gets closer to the target value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target value + fuzzy level) and the target value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
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
            
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","weight_label"]
        )
        
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
                    
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([1,1,1,1,1]))
    
        #declare fuzzy level for each target value
        #to make it easier, 0.5 is used for all target values
        fuzzy_levels =[]
        for i in range(len(data)-1):
            fuzzy_levels.append([0.5,0.5,0.5,0.5,0.5])
    
        #weights for all target values
        weights =[]
        for i in range(len(data)-1):
            weights.append([2,4,6,8,10])
        
        #create a WCSP
        wcsp = WCSP()
        
        start = time.time()
        #variable check for all the values in each goal
        for i in range(len(target_goals)):
            wcsp.variable_check(target_goals[i], goals_actual[i],fuzzy_levels[i],weights[i])
        
        print("Individual goal achievement: " + str(wcsp.get_indi_goal_check_result()))
        
        #check the variable check result from all the actual goals  
        IsAchieved = wcsp.minimum(wcsp.c_result)
        print("Cumulative goal achievement: " + str(IsAchieved))
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #individual goal
        computed = wcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,7])
        
        i_ct = 0
        for i in range(len(labels)):
            if labels[i] == round(computed[i],3):
                i_ct += 1
        indi_cts.append(i_ct)
        
        c_ct = 0
        if round(data.iloc[len(data)-1,7]) == round(IsAchieved,3):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/REPEAT))
    print("average computational time: " + str(sum(times)/len(times))+"sec")
 
elif MODE == 4:
    
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
    
        def variable_check(self, goal, elements):
            #check whether each value from an actual goal matches with the target variable's 
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #conver the value into predefined qualitative value
                c_result.append(self.num_to_char[elements[i]])
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
            
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data_qua"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","quality_label"]
        )
        
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
                    
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([3,3,3,3,3]))

        #create a FCSP
        qcsp = QCSP()
        
        start = time.time()
        #variable check for all the values in each goal
        for i in range(len(target_goals)):
            qcsp.variable_check(target_goals[i], goals_actual[i])
        
        print("Individual goal achievement: " + str(qcsp.get_indi_goal_check_result()))
        
        #check the variable check result from all the actual goals  
        IsAchieved = qcsp.multiplicative(qcsp.c_result)
        print("Cumulative goal achievement: " + str(IsAchieved))
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #individual goal
        computed = qcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,5])
        
        i_ct = 0
        for i in range(len(labels)):
            if labels[i] == computed[i]:
                i_ct += 1
        indi_cts.append(i_ct)
        
        c_ct = 0
        if data.iloc[len(data)-1,5] == IsAchieved:
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/REPEAT))
    print("average computational time: " + str(sum(times)/len(times))+"sec")

        
elif MODE == 5:
    import numpy as np
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
    
        def variable_check(self, goal, elements, probability):
            #check whether each value from an actual goal matches with the target variable's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
                
            c_result = []
            #check whether each actual value is correct
            #in reality, this is conducted by assessing observed data 
            #but here uses A~E as observed values and simulate
            for i in range(len(goal.c_elements)):
               #check whether the value is correct 
               #here uses simulation instead
               if elements[i] == 'E':
                   #if the observed values is not allowe (in this case, E is an out-of-rule value), 
                   #then the probability takes 1-P(check)
                   #each of variable has a chance to get E with 20% probability
                   c_result.append(1-probability[i])
               else:
                   #if it is allowed, then the probability takes 1
                   c_result.append(self.true) 
            #store the check result 

            self.c_result.append(self.multiplicative(c_result))
         
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
            
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data_prob"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","prob_label"]
        )
        
        #declare actual goals with observed values
        #in reality, meaningful observed data to determine whether the value is allowed is assigned
        #in this example, since this allowing check is simulated randomly and hence meaningless information is assigned instead 
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([1,1,1,1,1]))
               
        #check probability for each values in each goal
        #to make it simpler, the same probability is used for every check in each goal 
        probability =[]
        for i in range(len(data)-1):
            probability.append([0.7,0.7,0.7,0.7,0.7])
        
        #create a PCSP
        pcsp = PCSP()
        
        start = time.time()
        #variable check for all the values in each goal
        for i in range(len(target_goals)):
            pcsp.variable_check(target_goals[i], goals_actual[i],probability[i])
        
        #check the variable check result from individual the actual goals  
        IsAchieved = pcsp.multiplicative(pcsp.c_result)  
        print("Individual goal achievement: " + str(pcsp.get_indi_goal_check_result()))
        
        #check the variable check result from all the actual goals  
        IsAchieved = pcsp.multiplicative(pcsp.c_result)
        print("Cumulative goal achievement: " + str(IsAchieved))
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #individual goal
        computed = pcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,5])
        
        i_ct = 0
        for i in range(len(labels)):
            if round(labels[i],4) == round(computed[i],4):
                i_ct += 1
        indi_cts.append(i_ct)
        
        c_ct = 0
        if round(data.iloc[len(data)-1,5],4) == round(IsAchieved,4):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/REPEAT))
    print("average computational time: " + str(sum(times)/len(times))+"sec")

elif MODE == 6:
    
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
    
        def variable_check(self, goal, elements):
            #check whether each value from an actual project matches with the target's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #1 is returned iff the value in the values from the target goal is
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
    
        def variable_check(self, goal, elements, fuzzy_level):
            #check whether each value from an actual project matches with the target variable's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append(self.false)
                #if the actual value is between the (target value - fuzzy level) and the target value,
                #then, the returning value becomes closer to one as the value gets closer to the target value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])
                # if the actual value is the same with the target value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append(self.true)
                #if the actual value is between the (target value + fuzzy level) and the target value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
                else:
                    c_result.append((goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
    class WCSP:
        def __init__(self):
            #declare true, false value with the result container
            self.true = 1
            self.false = 0
            self.c_result = []
            
        def additive(self, elements):
            #return the sum value by following the definition
            return sum(elements)
        
        def minimum(self, element):
            return min(element)
    
        def variable_check(self, goal, elements, fuzzy_level, weights):
            #check whether each value from an actual project matches with target variable's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #if the actual value is lower or higher than the taget value with fuzzy level,
                #then it returns 0
                if goal.c_elements[i]-fuzzy_level[i] >= elements[i] or goal.c_elements[i]+fuzzy_level[i]  <= elements[i] :
                    c_result.append((1-self.false)*weights[i])
                #if the actual value is between the (target  value - fuzzy level) and the target value,
                #then, the returning value becomes closer to one as the value gets closer to the target value 
                elif (goal.c_elements[i]-fuzzy_level[i]  < elements[i]) and (goal.c_elements[i] > elements[i]):
                    c_result.append((1-(elements[i]-(goal.c_elements[i]-fuzzy_level[i]))/fuzzy_level[i])*weights[i])
                # if the actual value is the same with the target value, then it returns 1
                elif goal.c_elements[i] == elements[i]:
                    c_result.append((1-self.true)*weights[i])
                #if the actual value is between the (target value + fuzzy level) and the target value,
                #then, the returning value becomes closer to zero as the value gets closer to the (target value + fuzzy level)
                else:
                    c_result.append((1-(goal.c_elements[i]+fuzzy_level[i] -elements[i])/fuzzy_level[i])*weights[i])
            #store the check result   
            self.c_result.append(self.additive(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
    
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
    
        def variable_check(self, goal, elements):
            #check whether each value from an actual project matches with target variable's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
            
            #define an example fuzzy situation by applying membership function
            c_result = []
            for i in range(len(goal.c_elements)):
                #conver the value into predefined qualitative value
                c_result.append(self.num_to_char[elements[i]])
            #store the check result   
            self.c_result.append(self.multiplicative(c_result))
       
        def get_indi_goal_check_result(self):
            return self.c_result
        
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
    
        def variable_check(self, goal, elements, probability):
            #check whether each value from an actual project matches with target variable's
            
            #check whether the total number of values in the actually observed goal 
            #is the same with that in the target goal 
            if len(goal.c_elements) != len(elements):
                print("the number of c_element is not the same as the number of elements")
                exit(0)
                
            c_result = []
            #check whether each actual value is correct
            #in reality, this is conducted by assessing observed data 
            #but here uses A~E as observed values and simulate
            for i in range(len(goal.c_elements)):
               #check whether the value is correct 
               #here uses simulation instead
               if elements[i] == 'E':
                   #if the observed values is not allowe (in this case, E is an out-of-rule value), 
                   #then the probability takes 1-P(check)
                   #each of variable has a chance to get E with 20% probability
                   c_result.append(1-probability[i])
               else:
                   #if it is allowed, then the probability takes 1
                   c_result.append(self.true) 
            #store the check result 

            self.c_result.append(self.multiplicative(c_result))
         
        def get_indi_goal_check_result(self):
            return self.c_result   
       
    class target_goal:
        def __init__(self, c_elements):
            #target goal objects
            self.c_elements = c_elements
    
    indi_cts = []
    cumulative_cts = []
    times = []
    REPEAT = 3
    for a in range(REPEAT):
        #load actual goal data
        file = "data"+str(a+1)+".csv"
        
        data = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","weight_label"]
        )
        
        #load actual goal data
        file = "data_qua"+str(a+1)+".csv"
        
        data_qua = pd.read_csv(
            file,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","binary_label","fuzzy_label","quality_label"]
        )
              
        #load actual goal data
        file_prob = "data_prob"+str(a+1)+".csv"
        
        data_prob = pd.read_csv(
            file_prob,
            sep=',',
            header=None,
            skiprows=[0],
            index_col=False,
           # usecols=["issuekey","linkedIssueKey","weight","isExplicit"],
            names=["var1","var2","var3","var4","var5","prob_label"]
        )
        
        
        goals_actual = []
        for i in range(len(data)-1):
            goals_actual.append([data.iloc[i,0],data.iloc[i,1],data.iloc[i,2],data.iloc[i,3],data.iloc[i,4]])
        
        goals_actual_qua = []
        for i in range(len(data_qua)-1):
            goals_actual_qua.append([data_qua.iloc[i,0],data_qua.iloc[i,1],data_qua.iloc[i,2],data_qua.iloc[i,3],data_qua.iloc[i,4]])
        
        #declare actual goals with observed values
        #in reality, meaningful observed data to determine whether the value is allowed is assigned
        #in this example, since this allowing check is simulated randomly and hence meaningless information is assigned instead 
        goals_actual_prob = []
        for i in range(len(data_prob)-1):
            goals_actual_prob.append([data_prob.iloc[i,0],data_prob.iloc[i,1],data_prob.iloc[i,2],data_prob.iloc[i,3],data_prob.iloc[i,4]])
        
                    
        #declare goals with target values 
        target_goals =[]
        for i in range(len(data)-1):
            target_goals.append(target_goal([1,1,1,1,1]))
        
        target_goals_qua =[]
        for i in range(len(data_qua)-1):
            target_goals_qua.append(target_goal([3,3,3,3,3]))
        
        #declare fuzzy level for each value
        #to make it easier, 0.5 is used for all values
        fuzzy_levels =[]
        for i in range(len(data)-1):
            fuzzy_levels.append([0.5,0.5,0.5,0.5,0.5])
        
        #declare fuzzy level for each value
        #to make it easier, 0.5 is used for all values
        weight_fuzzy_levels =[]
        for i in range(len(data)-1):
            weight_fuzzy_levels.append([0.5,0.5,0.5,0.5,0.5])
    
        #weights for all values
        weights =[]
        for i in range(len(data)-1):
            weights.append([2,4,6,8,10])
        
        #probability for all values
        probability =[]
        for i in range(len(data)-1):
            probability.append([0.7,0.7,0.7,0.7,0.7])
            
        #declare SCSP, FCSP, WCSP and PCSP
        scsp = SCSP()
        fcsp = FCSP()
        wcsp = WCSP()
        qcsp = QCSP()
        pcsp = PCSP()
        
        start = time.time()
        #conduct variable check for each value in each classic, fuzzy and probability goals
        for i in range(len(goals_actual)):
            scsp.variable_check(target_goals[i], goals_actual[i])
        for i in range(len(goals_actual)):
            fcsp.variable_check(target_goals[i], goals_actual[i],fuzzy_levels[i])
        for i in range(len(goals_actual)):
            wcsp.variable_check(target_goals[i], goals_actual[i],weight_fuzzy_levels[i],weights[i])
        for i in range(len(target_goals)):
            qcsp.variable_check(target_goals[i], goals_actual_qua[i])
        for i in range(len(goals_actual)):
            pcsp.variable_check(target_goals[i], goals_actual_prob[i],probability[i])
        
        #check the variable check result from all the actual goals  
        IsAchieved_binary = scsp.multiplicative(scsp.c_result)
        IsAchieved_fuzzy = fcsp.multiplicative(fcsp.c_result)
        IsAchieved_weight = wcsp.minimum(wcsp.c_result)
        IsAchieved_qua = qcsp.multiplicative(qcsp.c_result)
        IsAchieved_prob = pcsp.multiplicative(pcsp.c_result)
        
        print("Individual goal achievement: ")
        print("binary: "+ str(scsp.get_indi_goal_check_result()))
        print("fuzzy: " + str(fcsp.get_indi_goal_check_result()))  
        print("weight: " + str(wcsp.get_indi_goal_check_result()))
        print("Quality: " + str(qcsp.get_indi_goal_check_result()))
        print("probability: " + str(pcsp.get_indi_goal_check_result()))
        print()
  
        print("Cumulative goal achievement: ")
        print("binary: " + str(scsp.multiplicative(scsp.c_result)))
        print("fuzzy: " + str(fcsp.multiplicative(fcsp.c_result)))
        print("weight: " + str(wcsp.minimum(wcsp.c_result)))
        print("Quality: " + str(qcsp.multiplicative(qcsp.c_result)))
        print("probability: " + str(pcsp.multiplicative(pcsp.c_result)))
        print()
        
        result = [scsp.multiplicative(scsp.c_result),
                  fcsp.multiplicative(fcsp.c_result),
                  wcsp.minimum(wcsp.c_result),
                  qcsp.multiplicative(qcsp.c_result),
                  pcsp.multiplicative(pcsp.c_result)]
       
        print("In a list form:")
        print(result)
        end = time.time()
        times.append(end-start)
        
        #accuracy check
        #binary
        #individual goal
        i_ct = 0
        computed_binary = scsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,5])
        for i in range(len(labels)):
            if labels[i] == computed_binary[i]:
                i_ct += 1
        indi_cts.append(i_ct)
        #cumulative
        c_ct = 0
        if data.iloc[len(data)-1,5] == IsAchieved_binary:
            c_ct += 1
        cumulative_cts.append(c_ct)
        
        #fuzzy
        #individual goal
        i_ct = 0
        computed_fuzzy = fcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,6])
        for i in range(len(labels)):
            if round(labels[i],4) == round(computed_fuzzy[i],4):
                i_ct += 1
        indi_cts.append(i_ct)
        #cumulative
        c_ct = 0
        if round(data.iloc[len(data)-1,6],4) == round(IsAchieved_fuzzy,4):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
        #weight
        #individual goal
        i_ct = 0
        computed_weight = wcsp.get_indi_goal_check_result()
        labels = list(data.iloc[:-1,7])
        for i in range(len(labels)):
            if round(labels[i],4) == round(computed_weight[i],4):
                i_ct += 1
        indi_cts.append(i_ct)
        #cumulative
        c_ct = 0
        if round(data.iloc[len(data)-1,7],4) == round(IsAchieved_weight,4):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
        #quality
        #individual goal
        i_ct = 0
        computed_quality = qcsp.get_indi_goal_check_result()
        labels = list(data_qua.iloc[:-1,5])
        for i in range(len(labels)):
            if labels[i] == computed_quality[i]:
                i_ct += 1
        indi_cts.append(i_ct)
        #cumulative
        c_ct = 0
        if data_qua.iloc[len(data)-1,5] == IsAchieved_qua:
            c_ct += 1
        cumulative_cts.append(c_ct)
        
        #probability
        #individual goal
        i_ct = 0
        computed_prob = pcsp.get_indi_goal_check_result()
        labels = list(data_prob.iloc[:-1,5])
        for i in range(len(labels)):
            if round(labels[i],4) == round(computed_prob[i],4):
                i_ct += 1
        indi_cts.append(i_ct)
        #cumulative
        c_ct = 0
        if round(data.iloc[len(data)-1,5],4) == round(IsAchieved_prob,4):
            c_ct += 1
        cumulative_cts.append(c_ct)
        
    print("individual goal accuracy: " + str(sum(indi_cts)/((len(data)-1)*4*REPEAT)))
    print("cumulative goal accuracy: " + str(sum(cumulative_cts)/(4*REPEAT)))
    print("average computational time: " + str(sum(times)/len(times))+"sec")    