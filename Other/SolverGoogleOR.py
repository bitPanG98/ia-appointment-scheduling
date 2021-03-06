from ortools.sat.python import cp_model
import random

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self._solutions = set(sols)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print("print")
        if self.__solution_count in self._solutions:
            for v in self.__variables:
                if self.Value(v) == 1:
                    print("Stampo soluzione" ,'%s=%i' % (v, self.Value(v)), end=' ')
                    print()


    def solution_count(self):
        return self.__solution_count

def innerFunction (x, y):
    if x[1] != y[1]:
        return True
    # se sono qui sono sicuro che sto considerando due appuntamenti che avvengono nello stesso giorno.
    #print("x = ", x, "   y = ", y)
    if (x[3] != y[3] and abs(float(x[2])-float(y[2])) < distance(x[3], y[3])*0.5 + 1):
        return False
    if (x[3] == y[3] and abs(float(x[2])-float(y[2])) != 1):
        return False
    else:
        return True

def constraintFunction():
    return innerFunction

def takeSecond(elem):
    return elem[1]

def distance(a, b):
    if (a=='A' and b=='B') or (b=='A' and a=='B'):
        return 1
    if (a=='A' and b=='C') or (b=='A' and a=='C'):
        return 1
    if (a=='A' and b=='D') or (b=='A' and a=='D'):
        return 2
    if (a=='B' and b=='C') or (b=='B' and a=='C'):
        return 2
    if (a=='C' and b=='D') or (b=='C' and a=='D'):
        return 1
    if (a=='B' and b=='D') or (b=='B' and a=='D'):
        return 1
    if (a == b):
        return 0




appointments = dict()

"""
appointment1 = {
  "Name": "Ford",
  "Surname": "Mustang",
  "House" : "A",
  "Day" : ["mon", "wed", "fri"],
  "Day" : ["mon"],
  "Pref" : ["Morning"]
}

appointment2 = {
  "Name": "Ford",
  "Surname": "Mustang",
  "House" : "A",
  "Day" : ["mon"],
  "Pref" : ["Morning"]
}


appointments["1"] = appointment1
appointments["2"] = appointment2
"""

days = ["mon", "tue", "wed", "thu", "fri", "sat"]

hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00",
"17.50"]

locations = ["A", "B", "C", "D"]

surnames = [ "Smith", "Jones", "Taylor", "Williams", "Brown", "Davies", "Evans",
"Wilson", "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson", "Wood",
"Thompson", "White", "Watson", "Jackson", "Wright", "Green", "Harris", "Cooper",
"King", "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes"]

names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James",
"Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte",
"Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper",
"Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel",
"Sofia"]

prefs = ["Morning", "Afternoon"]

for i in range(30):
    appointment = {
      "Name": names[random.randint(0, len(names)-1)],
      "Surname": surnames[random.randint(0, len(surnames)-1)],
      "House" : locations[random.randint(0, len(locations)-1)],
      "Day" : [days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)]],
      "Pref" : [prefs[random.randint(0, len(prefs)-1)]]
    }
    appointments[str(i)] = appointment

dominio = []
count = 0

for i in days:
    for y in hours:
        for loc in locations:
            dominio.append([i, y, loc])

#print(dominio)

model = cp_model.CpModel()

#print(dominio)
#print(appointments)
# sto iterando su tutte le chiavi

variables = {}
"""
for x in appointments:
    currvar = {}
    dom = []

    for y in dominio:
        hour , minutes = y[1].split(".")
        hour = int(hour)

        if "Morning" in appointments[x]["Pref"] and hour < 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
                dom.append(y)

        if "Afternoon" in appointments[x]["Pref"] and hour > 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
                dom.append(y)

    for y in dom:
        currvar[(x, y[0], y[1], y[2])] = model.NewBoolVar('Appuntamento %s giorno %s ora %s casa %s' % (x, y[0], y[1], y[2]))
    variables.update(currvar)
    print(variables)
"""

for x in appointments:
    for y in dominio:
        variables[(x, y[0], y[1], y[2])] = model.NewBoolVar('Appuntamento %s giorno %s ora %s casa %s' % (x, y[0], y[1], y[2]))

#print(variables)

for a in appointments:
    model.Add(sum(variables[(a, d, h, l)] for d in days for h in hours for l in locations) == 1)


"""
for d in days:
    #print(d)
    for h in hours:
        #print(h)
        for l in locations:
            model.Add(sum(variables[(a, d, h, l)] for a in appointments) == 1)
"""
"""
for x in variables:
    for y in variables:
        if(x != y):
            #print("Aggiungo un constraint")
            #print(x[0])
            if(x[0] == y[0]):
                model.Add()
            #model.Add(innerFunction(x,y))
"""

#solver = cp_model.CpSolver()
#solver.parameters.linearization_level = 0

solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter(variables, range(2))
status = solver.SearchForAllSolutions(model, solution_printer)

#solver.SearchForAllSolutions(model, solution_printer)
"""
# Statistics.
print()
print('Statistics')
print('  - conflicts       : %i' % solver.NumConflicts())
print('  - branches        : %i' % solver.NumBranches())
print('  - wall time       : %f s' % solver.WallTime())
print('  - solutions found : %i' % solution_printer.solution_count())

"""
"""
ordApp = [[],[],[],[],[],[]]

for x in solution:
    if solution[x][0]==days[0]:
        ordApp[0].append([x, solution[x]])
    if solution[x][0]==days[1]:
        ordApp[1].append([x, solution[x]])
    if solution[x][0]==days[2]:
        ordApp[2].append([x, solution[x]])
    if solution[x][0]==days[3]:
        ordApp[3].append([x, solution[x]])
    if solution[x][0]==days[4]:
        ordApp[4].append([x, solution[x]])
    if solution[x][0]==days[5]:
        ordApp[5].append([x, solution[x]])

print(ordApp)
for x in ordApp:
    x.sort(key =  takeSecond)

index = 0
for x in ordApp:
    print("\n\nGiorno: ", days[index])
    print("\nMattina:")
    cond = True
    for y in x:
        if (cond and float(y[1][1])>12):
            print("\nPomeriggio:")
            cond = False
        print("Ore: ", y[1][1], "Casa: ", y[1][2], " Appuntamento con: ", appointments[y[0]]["Name"], " ", appointments[y[0]]["Surname"])
    index+=1
"""
