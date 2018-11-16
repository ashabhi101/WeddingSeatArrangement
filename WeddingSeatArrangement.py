# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:09:26 2018

@author: HP
"""
import pulp
import pandas as pd

max_tables = 3
max_table_size = 4
guests = '1 2 3 4 5 6 7 8 9 10'.split()
print(guests)

scorematrix = pd.DataFrame([[0,50,0,1,-10,0,0,0,0,0], [50,0,-100,0,0,0,0,0,0,0], [0,-100,0,0,0,50,0,0,0,0], 
                            [1,0,0,0,1,1,0,0,0,0], [-10,0,0,1,0,0,0,0,0,0], [0,0,50,1,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,10,0,10],[0,0,0,0,0,0,10,0,-100,0],[0,0,0,0,0,0,0,-100,0,0],[0,0,0,0,0,0,10,0,0,0]])
scorematrix.columns = guests
scorematrix.index = guests
scorematrix
def happiness(table):
    """
    Find the happiness of the table
    - by calculating the sum of scorematrix elements for guests
    """
    sum =0
    for i in table:
        for j in table:
            sum+= scorematrix[i][j]
    return sum       
                
#create list of all possible tables
possible_tables = [tuple(c) for c in pulp.allcombinations(guests, 
                                        max_table_size)]
print(possible_tables)
#create a binary variable to state that a table setting is used
x = pulp.LpVariable.dicts('table', possible_tables, 
                            lowBound = 0,
                            upBound = 1,
                            cat = pulp.LpInteger)
print(x)

seating_model = pulp.LpProblem("Wedding Seating Model", pulp.LpMaximize)
print(seating_model)
seating_model += sum([happiness(table) * x[table] for table in possible_tables])
print(seating_model)

#specify the maximum number of tables
seating_model += sum([x[table] for table in possible_tables]) <= max_tables, \
                            "Maximum_number_of_tables"
print(seating_model)
#A guest must seated at one and only one table
for guest in guests:
    seating_model += sum([x[table] for table in possible_tables
                                if guest in table]) == 1, "Must_seat_%s"%guest

seating_model.solve()

print("The choosen tables are out of a total of %s:"%len(possible_tables))
for table in possible_tables:
    if x[table].value() == 1.0:
        print(table)
