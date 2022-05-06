class Variable:

    def __init__(self, name, order = 0) -> None:
        
        self.name = name
        self.order = order
        self.solution_dict = {self.d(i): [] for i in range(self.order)}

    def d(self, order):
        d_name = f'{self.name}[{order}]'
        return d_name

    def set_inital_condition(self, ic: dict):
        
        for i in ic:
            self.solution_dict[i].append(ic[i])
        
    def rep(self, rep_list):

        if len(rep_list) != self.order:
            raise Exception
        else:
            return {self.d(i): el for i, el in enumerate(rep_list)}


class Rep:

    def __init__(self) -> None:
        pass


if __name__ == '__main__':

    X = Variable('X', order = 3)    
    X_ic = {X.d(0): 3, X.d(1): 2, X.d(2): 1}
    X.set_inital_condition(X_ic)
    print(X.solution_dict)
    print(X.rep([87, 6, 29]))

    Y = Variable('Y', order = 3)    
    Y_ic = {Y.d(0): 4, Y.d(1): 5, Y.d(2): 6}
    Y.set_inital_condition(Y_ic)
    print(Y.solution_dict)

    def f():
        x0 = X.d(0)
        return X.d(1)

    print(f())



class Function:

    def __init__(self, variables, ) -> None:
        pass




class IC_Solution:

    def __init__(self) -> None:
        pass



