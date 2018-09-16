'''
This is the library for math calculations
There are representations like a|b which means the two vars statement that b = a * n is true where n such as Z 
There are two vars statements like a = (b*c) where a is var1 and (b*c) is var2, and the class is Equal
There are two vars operations like (b*c) where b is var1 and c is var2, and the class is Multiplication

'''

from copy import deepcopy, copy
import json, inspect, sys, logging

logging.basicConfig(filename='myMath.log',level=logging.DEBUG)
# var num is used to track auto-generated vars
var_num = 0
# when some vars have the same or similar definition, then they don't coexist
var_def = {}
subscript = {
    1: '₁',
    2: '₂',
    3: '₃',
    4: '₄',
    5: '₅',
    6: '₆',
    7: '₇',
    8: '₈',
    9: '₉',
    0: '₀',
}

with open("proven.json", "r+") as fp:
    proven = json.load(fp)

members_dict = dict(inspect.getmembers(sys.modules[__name__]))
class2str_dict = {}
for key in members_dict:
    if inspect.isclass(members_dict[key]):
        class2str_dict[members_dict[key]] = key

class Variable:
    '''
    A single variable that has restrictions
    '''
    def __init__(self, char, var_type=None, path='stated'):
        self.char = char
        self.type = var_type
        self.equivalences = [self]
        self.path = path

    def find_eqs(self):
        pass

    def find_basic_eqs(self):
        pass

    def find_commutations(self):
        pass

    def general_prop_deduction(self):
        pass

    def to_power(self, ):
        self.equivalences.append(Power(self, 1))

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        '''
        To determine whether two things are inherently equal, we just have to check if they have
        the same math representation. If both sides are math stuff, not None or something
        '''
        if other == None:
            return False
        elif {type(self), type(other)} == {Variable}:
            return self.char == other.char
        else:
            return self.char == str(other)


class Number(Variable):
    pass

class Integer(Variable): # I don't exactly need this
    def __init__(self, char, ):
        super().__init__(char, 'Z')


class TwoVarsClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
        self.attr2list()
        self.basic_vars = []  # don't need this for now
        self.equivalences = [self]
        self.path = None
        self.path_object = None
        self.path_explain = None
        self.find_eq_methods = []
        self.funcs = {
            'find basic eqs': {'func': self.find_basic_eqs},
            # 'vars find basic eqs': {'func': self.vars_find_basic_eqs}, 
            }
        self.useful = True
        self.get_eq_methods()
        mydebug(self, "initialized")

    def replace_var(self, a, b):  # replace a to b
        n = 0
        changed = False
        print(self.top_vars)
        for i in self.top_vars:
            print(i, a)
            if type(i) not in [Variable, int]:  # it is a box probably
                sub_changed = i.replace_var(a, b)
                if sub_changed:
                    changed = True
            if i == a:
                print("It equals")
                changed = True

                self.top_vars.remove(i)
                self.top_vars.insert(n, b)
            else:
                pass
            n += 1
        self.list2attr()
        return changed

    def list2attr(self):
        self.var1, self.var2 = self.top_vars

    def attr2list(self):
        self.top_vars = [self.var1, self.var2]

    def find_all_eq_self(self):
        mydebug(self, "find all eq self")
        if type(self.var1) not in [Variable, int]:
            self.var1.find_all_eq()
        if type(self.var2) not in [Variable, int]:
            self.var2.find_all_eq()
        while 1:
            old_eq_list = tuple(self.equivalences)
            for method in self.find_eq_methods:
                method()
                # mydebug(self, str(self.equivalences))
            self.equivalences, _ = symbol_set(self.equivalences)
            if old_eq_list == tuple(self.equivalences):
                mydebug(self, "no change")
                break
            else:
                mydebug(self, "something changed")

    def find_all_eq(self, ):
        mydebug(self, "find all eq")
        while 1:
            old_eq_list = tuple(self.equivalences)
            for eq in self.equivalences:
                if type(eq) not in [Variable, int] and eq != self:
                    eq.find_all_eq_self()
            self.find_all_eq_self()
            if old_eq_list == tuple(self.equivalences):
                mydebug(self, "no change")
                break

    def find_all_basic(self):
        mydebug(self, "find all basic")
        old_eq_list = tuple(self.equivalences)
        if type(self.var1) not in [Variable, int]:
            self.var1.find_all_basic()
        if type(self.var2) not in [Variable, int]:
            self.var2.find_all_basic()
        self.find_basic_eqs()
        if old_eq_list != tuple(self.equivalences):
            mydebug(self, "Something is different %s -> %s" % (str(old_eq_list), str(self.equivalences)))
        else:
            mydebug(self, "No change.")

    def find_basic_eqs(self):
        mydebug(self, "find basic eqs")
        if type(self.var1) == int:
            var1_eqs = [self.var1]
        else:
            var1_eqs = self.var1.equivalences
        if type(self.var2) == int:
            var2_eqs = [self.var2]
        else:
            var2_eqs = self.var2.equivalences
        for i in var1_eqs:
            for j in var2_eqs:
                # mydebug(self, ' '.join([str(i), str(j)]))
                if i != self.var1 or j != self.var2:
                    new_eq = self.copy(i, j)
                    if eq_not_in(new_eq, self.equivalences):
                        new_eq.path = 'basic'
                        new_eq.path_object = [i, j, self]
                        new_eq.path_explain = "%s = %s %s = %s %s %s = %s" % (str(self.var1), str(i), str(self.var2), str(j), str(new_eq.path), str(self), str(new_eq))
                        mydebug(new_eq, new_eq.path_explain)
                        self.equivalences.append(new_eq)
                        mydebug(new_eq, str(new_eq.equivalences))
        
        # self.equivalences, _ = symbol_set(self.equivalences)

    def find_all_commutations(self, ):
        mydebug(self, "find all commutations")
        old_eq_list = tuple(self.equivalences)
        if type(self.var1) not in [Variable, int]: 
            self.var1.find_all_commutations()
        if type(self.var2) not in [Variable, int]:
            self.var2.find_all_commutations()
        self.find_commutations()
        if old_eq_list != tuple(self.equivalences):
            mydebug(self, "Something is different %s -> %s" % (str(old_eq_list), str(self.equivalences)))
        else:
            mydebug(self, "No change.")

    def find_commutations(self):
        mydebug(self, "find commutation")
        new_eq = self.copy(self.var2, self.var1)
        new_eq.path = 'commutation'
        new_eq.path_object = self
        new_eq.path_explain = "%s = %s" % (str(self), str(new_eq))
        mydebug(self, new_eq.path_explain)
        self.equivalences.append(new_eq)
        self.equivalences, _ = symbol_set(self.equivalences)

    def sharing_eqs(self, ):
        mydebug(self, "sharing eqs")
        old_eq_list = tuple(self.equivalences)
        for i in self.equivalences:
            if i != self:
                for j in i.equivalences:
                    if j != self:
                        new_eq = j.copy(j.var1, j.var2)
                        new_eq.path = 'sharing equivalences'
                        new_eq.path_explain = "%s = %s %s = %s" % (str(self), str(i), str(i), str(j))
                        new_eq.path_object = [i, j]
                        self.equivalences.append(new_eq)

                self.equivalences, _ = symbol_set(self.equivalences)
        if old_eq_list != tuple(self.equivalences):
            mydebug(self, "Something is different %s -> %s" % (str(old_eq_list), str(self.equivalences)))
        else:
            mydebug(self, "No change.")

    def forget_me(self, ):
        self.useful = False

    def forget_others(self, ):
        for eq in self.equivalences:
            if eq != self:
                eq.forget_me()
        self.clear()

    def clear(self, ):
        new_eq_list = []
        for eq in self.equivalences:
            if eq.useful:
                new_eq_list.append(eq)
        self.equivalences = new_eq_list

    def copy(self, var1, var2):
        new_self = copy(self)
        new_self.var1 = var1
        new_self.var2 = var2
        new_self.attr2list()
        new_self.get_eq_methods()
        return new_self

    def get_eq_methods(self, ):
        self.find_eq_methods = [
            self.find_all_basic,
            self.find_all_commutations,
            self.sharing_eqs,
            self.general_prop_deduction,
        ]

    def general_prop_deduction(self, ):
        mydebug(self, "general property deduction")
        new_eq = match_proven(self)
        if new_eq != False:
            mydebug(self, "fits a proven")
            self.equivalences.append(new_eq)
            self.equivalences, _ = symbol_set(self.equivalences)
            return new_eq

    def gpd_and_vars(self, ):
        eq = self.general_prop_deduction()
        new_eq = eq.copy(eq.var1, eq.var2)
        if new_eq:
            n = 0
            for i in new_eq.top_vars:
                if type(i) not in {Variable, int}:
                    new_eq_var = i.general_prop_deduction()
                    if new_eq_var:
                        new_eq.top_vars[n] = new_eq_var
                    n += 1
            new_eq.list2attr()
            self.equivalences.append(new_eq)
            return new_eq

    def __repr__(self, ):
        return str(self)

    def __eq__(self, other):
        if other != None and type(other) not in [Variable, int]:
            return str(self) == str(other)
        else:
            return False


class Subset(TwoVarsClass):
    def __init__(self, var1, var2):
        super().__init__(var1, var2)

    def __str__(self):
        return '%s subset %s' % (str(self.var1), str(self.var2))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)


class Equal(Subset):
    def __init__(self, var1, var2, path='stated'):
        super().__init__(var1, var2)
        self.equivalences = [self]
        self.path = path
        self.funcs.update({
            'find eqs': {'func': self.find_eqs}, 
            'find basic eqs': {'func': self.find_basic_eqs},
            'vars find basic eqs': {'func': self.vars_find_basic_eqs}, 
            })

    def find_eqs(self):
        self.var1.find_eqs()
        self.var2.find_eqs()
        self.find_basic_eqs()
        self.equivalences, _ = symbol_set(self.equivalences)

    def operate_both_sides(self, operation, var):
        '''
        Takes var as the second parameter, b, makes both side from left=right to operation(left, var) = operation(right, var)
        '''
        new_eq = deepcopy(self)
        new_eq.var1 = operation(new_eq.var1, var)
        new_eq.var2 = operation(new_eq.var2, var)
        new_eq.path = {"operate both sides": "stuff"}
        self.equivalences.append(new_eq)

    def __str__(self):
        return '%s = %s' % (str(self.var1), str(self.var2))


class Divides(TwoVarsClass):
    def __init__(self, var1, var2, path='stated'):
        super().__init__(var1, var2)
        self.statement = None
        self.path = path
        self.check = False

        self.find_statement()

    def find_statement(self, ):
        new_var = get_new_var('Z')
        self.statement = Equal(self.var2, Multiplication(self.var1, new_var), path={'representation': self})

    def statement_qualify(self, statement):
        if type(statement) == Equal:
            if statement.var1 == self.var2:
                if type(statement.var2) == Multiplication:
                    if statement.var2.var1 == self.var1:
                        if statement.var2.var2.type == 'Z':
                            return True

    def find_commutations(self):
        return "Not available for divides"

    def __str__(self):
        return '%s | %s' % (str(self.var1), str(self.var2))

    def __repr__(self):
        return str(self)


class Multiplication(TwoVarsClass):
    '''
    When var1 and var2 are any sets, for example N or Z, it means a member of them such that a is a member of var1 and
    b is a member of var2. Then Multiplication(var1, var2) is Multiplication(a, b) for all possible combination of a, b
    '''
    def __init__(self, var1, var2, path='stated'):
        super().__init__(var1, var2)
        self.equivalences = [self]
        self.path = path
        self.funcs.update({
            'result': {'func': self.result}, 
            'find eqs': {'func': self.find_eqs}, 
            'find basic eqs': {'func': self.find_basic_eqs},
            'find commutations': {'func': self.find_commutations},
            'find association': {'func': self.find_associations},
            'general property deduction': {'func': self.general_prop_deduction},
            'sharing equivalences': {'func': self.sharing_eqs},
            'vars general property deduction': {'func': self.vars_general_prop_deduction},
            })

    def result(self):
        if {type(self.var1), type(self.var2)} == {Variable}:
            global var_def
            if self.var1.type == 'N' and self.var2.type == 'N':
                if str(self) not in var_def:
                    new_var = get_new_var('N')
                    var_def[str(self)] = new_var
                else:
                    new_var = var_def[str(self)]
                new_var.path = {'general property deduction': self}
                return new_var
            if self.var1.type == 'Z' and self.var2.type == 'Z':
                if str(self) not in var_def:
                    new_var = get_new_var('Z')
                    var_def[str(self)] = new_var
                else:
                    new_var = var_def[str(self)]
                new_var.path = {'general property deduction': self}
                return new_var

    def find_eqs(self):
        self.find_basic_eqs()
        self.find_associations()
        self.general_prop_deduction()
        self.find_commutations()
        self.sharing_eqs()

    def find_associations(self):
        # print('finding associations for %s' % (str(self)))
        for i in self.equivalences:
            # print(i)
            if type(i) == Multiplication:
                if type(i.var2) == Multiplication:
                    new_eq = deepcopy(i)
                    new_eq.path = {'association': copy(new_eq)}
                    new_eq.var1 = Multiplication(new_eq.var1, new_eq.var2.var1)
                    new_eq.var2 = new_eq.var2.var2
                    self.equivalences.append(new_eq)

                if type(i.var1) == Multiplication:
                    new_eq = deepcopy(i)
                    new_eq.path = {'association': copy(new_eq)}
                    new_eq.var2 = Multiplication(new_eq.var1.var2, new_eq.var2)
                    new_eq.var1 = new_eq.var1.var1
                    self.equivalences.append(new_eq)
                # print(self.equivalences)
                self.equivalences, _ = symbol_set(self.equivalences)

    def general_prop_deduction(self):
        for i in self.equivalences:
            # print('eq of %s' % (str(self)), self.equivalences)
            if type(i) == Multiplication:
                r = i.result()
                if r:
                    # print('##'*10, i.var1, i.var2, r)
                    self.equivalences.append(r)
                    self.equivalences, _ = symbol_set(self.equivalences)

    def vars_general_prop_deduction(self, ):
        self.var1.general_prop_deduction()
        self.var2.general_prop_deduction()

    def __str__(self):
        return '(%s * %s)' % (str(self.var1), str(self.var2))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)


class Addition(TwoVarsClass):
    def __init__(self, var1, var2, path='stated'):
        super().__init__(var1, var2)
        self.equivalences = [self]
        self.path = path
        self.funcs.update({
            'find commutations': {'func': self.find_commutations},
        })

    def find_associations(self):
        mydebug(self, "find associations")
        if type(self.var2) == Addition:
            new_eq = self.copy(Addition(self.var1, self.var2.var1), self.var2.var2)
            new_eq.path = 'association'
            new_eq.path_explain = "%s = %s" % (str(self), str(new_eq))
            new_eq.path_object = self
            self.equivalences.append(new_eq)
        
        self.equivalences, _ = symbol_set(self.equivalences)

    def find_common_factor(self):
        if {type(self.var1), type(self.var2)} == {Multiplication}:
            if self.var1.var1 == self.var2.var1:
                new_eq = Multiplication(self.var1.var1, Addition(self.var1.var2, self.var2.var2))
                self.equivalences.append(new_eq)

    def general_prop_deduction(self):
        if {type(self.var1), type(self.var2)} == {Variable}:
            if {self.var1.type, self.var2.type} == {"Z"}:
                new_var = get_new_var("Z",)
                self.equivalences.append(new_var)

    def get_eq_methods(self, ):
        super().get_eq_methods()
        self.find_eq_methods.append(self.find_associations)

    def __str__(self, ):
        return "(%s + %s)" % (self.var1, self.var2)


class Substraction(TwoVarsClass):
    def __str__(self, ):
        return "(%s - %s)" % (self.var1, self.var2)


class Division(TwoVarsClass):
    # def cancel_out_common_factors(self, ):
    #     mydebug(self, "cancel out common factors")
    #     if {type(self.var1), type(self.var2)} == {Multiplication} and self.var1.var1 == self.var2.var1:
    #         new_eq = Division(self.var1.var2, self.var2.var2)
    #         self.equivalences.append(new_eq)
    
    def __repr__(self, ):
        return str(self)

    def __str__(self, ):
        return "(%s / %s)" % (self.var1, self.var2)

    def find_all_commutations(self, ):
        mydebug(self, "derivative doesn't have find commutations")

    # def get_eq_methods(self, ):
    #     super().get_eq_methods()
    

class MathFunction:
    def __init__(self, var):
        self.var = var
        self.equivalences = [self]

    def find_all_eq(self,):
        mydebug(self, "math function doesn't have find all eq")

    def find_all_basic(self, ):
        mydebug(self, "math function doesn't have find all basic")

    def find_all_commutations(self, ):
        mydebug(self, "math function doesn't have find all commutations")

    def __repr__(self, ):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)


class Sec(MathFunction):
    def __str__(self, ):
        return "sec(%s)" % str(self.var)


class Tan(MathFunction):
    def __str__(self, ):
        return "tan(%s)" % str(self.var)


class Power(TwoVarsClass):
    # def __init__(self, var, power):
    #     self.var = var
    #     self.power = power
    #     super().__init__(var, power)

    def find_commutations(self, ):
        mydebug(self, "doesn't have commutative rule")

    def __str__(self, ):
        # return "%s^%d" % (str(self.var), self.power)
        return "%s^%d" % (str(self.var1), self.var2)

    def __repr__(self, ):
        return str(self)


def find_conclusion(statement1, statement2):
    var_list = []
    for i in [statement1, statement2]:
        for j in i.top_vars:
            if j not in var_list:
                var_list.append(j)
    if len(var_list) == 3 and statement1.var2 == statement2.var1:
        return Subset(statement1.var1, statement2.var2)


def find_inner_conclusion(statement1, statement2):  # statement or operation actually
    '''
    Takes two statements as parameters. If statement1.var2 is not variable, var2 replace
    statement2.var1 to statement2.var2
    '''
    print(statement1, statement2)
    # input()
    changed = False
    new_statement1 = deepcopy(statement1)
    if type(new_statement1.var2) not in [Variable, int]:
        if new_statement1.var2.replace_var(statement2.var1, statement2.var2):
            changed = True
    # if type(new_statement1.var1) != Variable:
    #     if new_statement1.var1.replace_var(statement2.var2, statement2.var1):
    #         changed = True
    if changed:
        print(new_statement1)
        new_statement1.path = {"find inner conclusion": "stuff"}
        return new_statement1


def symbol_set(some_list):
    new_list = []
    symbol_list = []
    for i in some_list:
        if str(i) not in symbol_list:
            symbol_list.append(str(i))
            new_list.append(i)
    
    return new_list, symbol_list


def eq_not_in(eq, eq_list):
    _, symbol_list = symbol_set(eq_list)
    if str(eq) not in symbol_list:
        return True
    else:
        return False


def add_proven(obj1, obj2):
    # obj1 calls, and obj2 is the eq that is generated
    global proven
    # if not already there
    {
        "self type": class2str_dict[type(obj1)],
        "var1 type": class2str_dict[type(obj1.var1)],
        "var2 type": class2str_dict[type(obj1.var2)],
        "condition": "obj.var1.var == obj.var2",
        "equivalence type": "Multiplication",
        "equivalence var1 type": "Sec",
        "equivalence var2 type": "Sec",
        "equivalence var1 parameters": ["obj.var2"],
        "equivalence var2 parameters": ["obj.var2"],
        "equivalence": "Multiplication(Sec(obj.var2), Sec(obj.var2))",
        "path": "Calculus Identity",
        "path object": "obj"
    }

def not_in_sl(item, sl):  # sl is symbol list
    if str(item) not in sl:
        return True
    return False


def get_new_var(var_type='Q', name=None, path='auto-assigned'):
    if name == None:
        global var_num
        var_num += 1
        if var_num < 10:
            my_subscript = subscript[var_num]
        else:
            my_subscript = ''
            for i in str(var_num).split():
                my_subscript += subscript[int(i)]

        name = 'x'+my_subscript

    return Variable(name, var_type, path=path)  # var_num should be global


def str2addition(my_str):
    if '+' in my_str:
        my_str = ''.join(my_str.split(' '))
        var1, var2 = my_str.split('+')
        return Addition(var1, var2, path={'premise'})
    else:
        return False


def match_proven(obj):
    global proven
    for theory in proven:
        condition_list = []
        try:
            condition_list.append(type(obj) == members_dict[theory["self type"]])
            condition_list.append(type(obj.var1) == members_dict[theory["var1 type"]])
            condition_list.append(type(obj.var2) == members_dict[theory["var2 type"]])
            condition_list.append(eval(theory["condition"], globals(), locals()))
        except AttributeError:
            continue
        if set(condition_list) == {True}:
            new_eq = eval(theory["equivalence"], globals(), locals())
            new_eq.path = theory["path"]
            new_eq.path_object = eval(theory["path object"], globals(), locals())
            return new_eq
    return False


def mydebug(obj, msg):
    logging.debug("%s: %s" % (str(obj), msg))

    