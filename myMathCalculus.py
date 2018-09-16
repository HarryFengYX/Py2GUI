from myMath import *

class Limit:
    '''
    lim var->value f(x)
    '''
    def __init__(self, function, toApproachVar, toApproachValue):
        self.func = function
        self.toApproachVar = toApproachVar
        self.toApproachValue = toApproachValue

class Derivative(Division):
    '''
    a is the usual y, and b is the usual x. We will have da/db just like dy/dx
    as I don't find a way to do it like a up and down fraction, it is just going
    to be ugly
    '''
    def find_parametric_form(self, p=None):
        mydebug(self, "find parametric form")
        if p == None:
            try:
                p = self.var1.var
            except AttributeError:
                mydebug(self, "find parametric form failed due to no p")
                return
        var1 = Derivative(self.var1, p)
        var2 = Derivative(self.var2, p)
        new_eq = Division(var1, var2)
        self.equivalences.append(new_eq)

    def __str__(self, ):
        return "(d(%s / d%s))" % (str(self.var1), str(self.var2))

t = Variable('t')
d = Derivative(t, t)

