from Benchmark_ import Benchmarker
from itertools import permutations,count 
import matplotlib.pyplot as plt 
import time
class Exhaustiver: 

    def __init__(self , initial_solution ,iteration_num ,vehicle_num,early_stop):
        self.Optimal_cost = float("inf")
        self.Best_solution =None
        self.initial_solution = initial_solution 
        
        self.iteration_step = iteration_num
        if early_stop :
            self.Early_stop = iteration_num//3
        else:
            self.Early_stop = iteration_num
        self.Cost_Array = []
        self.vehicle_num = vehicle_num
        
        if self.vehicle_num > 1 :
            self.cost_function = Benchmarker.MultiVehicle_Cost
            self.MultiVehicle_adjust() 
            
        else : 
            print("use single vehicle")
            self.cost_function = Benchmarker._routeCost 
        
        self.init_Generator(self.initial_solution) 
    
    
    def init_Generator(self,iterable): 
        Generator = permutations(iterable) 
        self.Generator = Generator 
        
    def MultiVehicle_adjust(self): 
        step = len(self.initial_solution)//self.vehicle_num 
        for i in range(self.vehicle_num-1): 
            self.initial_solution.insert((i+1)*step,"|") 
        print(self.initial_solution)
            
    def getSolution(self): 
        sol = list(self.Generator.__next__() )
        #print(sol)
    
        return sol

    def evaluate(self,plotting=False):
        start_time = time.time()
        step_count = 0
        stop_count = 0
        rev_count = 0
        rev = False 
        try:
            for step in range(self.iteration_step):
                
                candidate = self.getSolution()
                
                
                if rev: 
                    l = len(candidate)//2 
                    candidate = candidate[l:]+ candidate[:l]
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost,solution= self.cost_function(candidate,self.vehicle_num)
                    
                else: 
                    #cost,solution = Benchmarker._routeCost(candidate)
                    cost,solution= self.cost_function(candidate,self.vehicle_num)
                    # TODO reverse
                
                if cost < self.Optimal_cost: 
                    self.Optimal_cost = cost 
                    self.Best_solution = solution
                    stop_count = 0
                    rev_count = 0
                else:  
                    stop_count +=1 
                    rev_count +=1 
                
                self.Cost_Array.append(self.Optimal_cost) 
                
                if rev_count >= 8: 
                     rev = not rev 
                     rev_count = 0
                     #print("--------REV---------")
                if stop_count >= self.Early_stop: 
                    print("early stop at {}".format(step))
                    break 
                step_count +=1
        except: 
            print("error")
        finally: 
            print("Best solution: {} , cost: {} " .format(self.Best_solution,self.Optimal_cost))
            print(f"total step: {step_count}")
            if plotting:
                self.plotting()
            print("time" , time.time()-start_time)
            return self.Optimal_cost , self.Best_solution 


    def plotting(self): 
        #print(self.Cost_Array)
        
        # plt.subplot(1,2,1),Benchmarker.plotting(Benchmarker.SourceGraph)
        # plt.subplot(1,2,2),plt.plot(range(len(self.Cost_Array)),self.Cost_Array) 
        # plt.show()
        testing_setting = f"optimizer: Exhaustiver\n\nCost:{self.Optimal_cost}\n\niterations :{self.iteration_step}\n\nvehicle_num:{self.vehicle_num}\n\nCriterion:MinSum" 
       
        
        Benchmarker.plotting(Benchmarker.SourceGraph,solution_path=self.Best_solution,
                             optimizer="Exhaustiver",Cost_log=self.Cost_Array,testing_set=testing_setting,vehicle_num=self.vehicle_num)
        
        
        
Benchmarker.setting(setting_file_path="map/Adjency3.json")
Benchmarker.Source_graphLoading()

#Exahuser = Exhaustiver(initial_solution=["b","D","a","B","E","C","2","5","H","j","h","L","e","T","s","4","K",'l'],iteration_num=1000,vehicle_num=4,early_stop=False)
Exahuser = Exhaustiver(initial_solution=["1F_stage","1F_gate_2","1F_HenGi","1F_table","1F_forest","1F_willy_destroy"],iteration_num=1400,vehicle_num=1,early_stop=False)
#Exahuser = Exhaustiver(initial_solution=["A","1","c","b","e","2","E","C","d","4","G"],iteration_num=39916800,vehicle_num=1,early_stop=False)
Exahuser.evaluate(plotting=True)

#print(Exahuser.cost_function(['G', 'D', 'A', 'I', 'C', 'L']))
