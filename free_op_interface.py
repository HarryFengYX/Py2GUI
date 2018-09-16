from my_socket import *
# from myMath import *
import inspect
import myMath
from myMath import *
from my_inspect import *
import logging

def send_functions():
    global func_list
    global server

    func_info = []
    n = 0
    for f in func_list:
        func_info.append(';'.join([f['name'], f['info'], str(n)]))
        n += 1
    func_info = '\n'.join(func_info)
    server.send(func_info)

def send_objects():
    global vars_list
    global server

    obj_info = []
    n = 0
    for var in vars_list:
        obj_info.append(';'.join([str(var), str(type(var)), str(n)]))
        n += 1
    obj_info = '\n'.join(obj_info)
    server.send(obj_info)

def send_checked_objects():
    global server

    check_var_info_list = server.data.decode().split(':')[1].split('.')
    # as the message should be in the format of 
    # co:index to check a preexisting var
    # and co:index.attribute to check an attribute that is an object
    # and co:index.name_of_list.index
    if len(check_var_info_list) == 1:
        check_preexisting_object(check_var_info_list)
        
    elif len(check_var_info_list) == 2:
        create_var_from_attribute(check_var_info_list)

    elif len(check_var_info_list) == 3:
        create_var_from_list_attribute(check_var_info_list)

def check_preexisting_object(check_var_info_list):
    global vars_list
    global server

    var_index = check_var_info_list[0]
    var = vars_list[int(var_index)]
    logging.debug("Checking %s" % (str(var)))
    # format: name;type;attr_name:type,value(s);attr_name:type,value(s)
    # type can be function, list, or any other type
    # if the type is a function, it will be added in the function view in unity
    var_name = str(var)
    var_type = str(type(var))
    var_attrs = []
    for key in var.__dict__:
        attr_name = key
        attr = var.__dict__[attr_name]
        if type(attr) == list:
            attr_type = 'list'
        else:
            attr_type = 'other'
        if attr == None:
            attr_values = "None"
        elif type(attr) == list:
            attr_values = ','.join([str(i) for i in attr])
        else:
            attr_values = str(attr)
        attr_info = "%s:%s,%s" % (attr_name, attr_type, attr_values)
        var_attrs.append(attr_info)
    for key in get_functions(var):
        attr_name = key
        attr_type = 'func'
        attr_values = key
        attr_info = "%s:%s,%s" % (attr_name, attr_type, attr_values)
        var_attrs.append(attr_info)

    var_attrs = ';'.join(var_attrs)
    var_info = "%s;%s;%s" % (var_name, var_type, var_attrs)
    print(var_info)
    server.send(var_info)

def create_var_from_attribute(check_var_info_list):
    global vars_list
    global server

    var_parent_index = check_var_info_list[0]
    var_parent = vars_list[int(var_parent_index)]
    attr_name = check_var_info_list[1]
    var = getattr(var_parent, attr_name)
    vars_list.append(var)
    server.send(str(len(vars_list)-1))

def create_var_from_list_attribute(check_var_info_list):
    global vars_list
    global server

    var_parent_index = check_var_info_list[0]
    var_parent = vars_list[int(var_parent_index)]
    list_name = check_var_info_list[1]
    var_list = getattr(var_parent, list_name)
    list_index = check_var_info_list[2]
    var = var_list[int(list_index)]
    vars_list.append(var)
    server.send(str(len(vars_list)-1))

def get_func_list():
    global func_list
    func_list = []
    for name, member in inspect.getmembers(myMath):
        # print(name, inspect.isclass(member), inspect.isfunction(member))
        if name.startswith("__"):
            continue
        elif inspect.isclass(member) or inspect.isfunction(member):
            # 
            member_info = {
                'name': name,
                'func': member,
                'info': ' '.join(str(member.__doc__).strip().split('\n')),
            }
        
            func_list.append(member_info)
        vars_list.append(member)

def create_string():
    pass

def call_function():
    global server
    
    function_message = server.data.decode()[3:]
    function_info, parameters_index = function_message.split(":")
    function_info_list = function_info.split(".")
    logging.debug("Function Info: %s" % (function_info))
    logging.debug("Parameter Info: %s" % (parameters_index))
    
    if len(function_info_list) == 1:
        function_index = function_info_list[0]
        function = func_list[int(function_index)]['func']
        
    elif len(function_info_list) == 2:
        obj_index, function_name = function_info_list
        obj = vars_list[int(obj_index)]
        function = getattr(obj, function_name)

    logging.debug("function: %s" % (str(function)))

    if parameters_index != '':
        parameters_index_list = parameters_index.split(",")
        #     parameter_list = [vars_list[int(i)] for i in parameters_index_list]
        # except ValueError:
        parameter_list = []
        for p in parameters_index_list:
            try:
                parameter_list.append(vars_list[int(p)])
            except ValueError:
                parameter_list.append(p)
    else:
        parameter_list = []
    logging.debug("parameters: %s" % (', '.join([str(i) for i in parameter_list])))
    new_var = function(*parameter_list)
    if new_var != None:
        vars_list.append(new_var)
    server.send("success")

# func_list = [
#     {
#         'name': 'find inner conclusion',
#         'func': find_inner_conclusion,
#         'info': 'Takes two parameters: statement1 and statement2 and return a deduced statement if there is one.'
#     },
#     {
#         'name': 'find conclusion',
#         'func': find_conclusion,
#         'info': 'Takes two parameters: statement1 and statement2 and return a deduced statement if there is one.'
#     },
#     {
#         'name': 'Addition',
#         'func': Addition,
#         'info': 'Takes two parameters: a and b, returns a+b.'
#     },
#     {
#         'name': 'Multiplication',
#         'func': Multiplication,
#         'info': 'Takes two parameters: a and b, returns a*b.'
#     },
# ]

func_list = []
# vars_list = []

vars_list = [
    Variable('a'),
    Variable('b'),
    # Multiplication(vars_list[0], vars_list[1]),
]
t = Variable('t')
x = Substraction(t, Power(t, 2))
y = Substraction(t, Power(t, 3))
d = Derivative(y, x)
d.find_parametric_form(t)
d = d.equivalences[-1]
d.var1.general_prop_deduction()
d.var2.general_prop_deduction()
vars_list.extend([t, d, x, y])
logging.basicConfig(filename='example.log',level=logging.DEBUG)


server = socket_server('localhost', 50000)
server.accept_client()
logging.info('client accepted')
get_func_list()
while 1:
    try:
        server.receive_data()
        if server.data == b'get functions':
            logging.debug("Starting to send functions.")
            send_functions()
        elif server.data == b'get objects':
            logging.debug("Starting to send objects.")
            send_objects()
        elif server.data.decode().startswith("co:"):
            logging.debug("Starting to send checked objects.")
            send_checked_objects()
        elif server.data.decode().startswith("cf:"): # Call the function
            logging.debug("Starting to call a function.")
            call_function()
    except KeyboardInterrupt:
        server.close_client()