from lake_parser import Lark_StandAlone, Transformer

class Statement:
    pass

class Package(Statement):
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Package({self.name})'
    def pretty(self):
        return self.__str__()

class Import(Statement):
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Import({self.name})'
    def pretty(self):
        return self.__str__()

class EnumMember:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'EnumMember({self.name})'
    def __repr__(self):
        return self.__str__()
    def pretty(self):
        return self.__str__()

class EnumDecl(Statement):
    def __init__(self, args):
        self.name = args[0].children[0].children[0].value
        self.members = []
        length = len(args)
        for i in range(1, length):
            self.members.append(EnumMember(args[i].children[0].children[0].value))
    def __str__(self):
        return f'EnumDecl({self.name}, {self.members})'
    def pretty(self):
        return self.__str__()
    
class StructField:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __str__(self):
        return f'StructField({self.name}, {self.type})'
    def __repr__(self):
        return self.__str__()
    def pretty(self):
        return self.__str__()

class StructDecl(Statement):
    def __init__(self, args):
        self.name = args[0].children[0].value
        self.fields = []
        length = len(args)
        for i in range(1, length):
            self.fields.append(StructField(args[i].children[0].children[0].value, args[i].children[1].children[0].value))
    def __str__(self):
        return f'StructDecl({self.name}, {self.fields})'
    def pretty(self):
        return self.__str__()

class FunctionParam:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __str__(self):
        return f'FunctionParam({self.name}, {self.type})'
    def __repr__(self):
        return self.__str__()
    def pretty(self):
        return self.__str__()

class FunctionDecl(Statement):
    def __init__(self, args):
        self.name = args[0].children[0].children[0].value
        self.params = []
        self.return_type = args[0].children[2].children[0].children[0].value if len(args[0].children[2].children) > 0 else None
        for child in args[0].children[1].children:
            self.params.append(FunctionParam(child.children[0].children[0].value, child.children[1].children[0].value))
        
        self.statements = []
        statements_raw = args[0].children[3:]
    
        for statement in statements_raw:
            transform = TreeToLake().transform(statement)
            self.statements.append(transform)

        for statement in self.statements:
            print(statement)

    def __str__(self):
        s = f'FunctionDecl({self.name}, {self.params}, {self.return_type}) (\n'
        for statement in self.statements:
            s += f'\t{statement.pretty()}\n'
        s += f')'

        return s
    def pretty(self):
        return self.__str__()
    
class AssignmentTyped:
    def __init__(self, args):
        self.var_name = args[0].children[0].value
        self.type = args[1].children[0].value
        self.value = args[2].children[0]

    def __str__(self):
        return f'Assignment({self.var_name}, {self.type}, {self.value})'
    def __repr__(self):
        return self.__str__()

class StructCall: 
    def __init__(self, args):
        print("----")
        print(args[0])
        print("------")
        self.name = args[0].children[0].value
        self.params = []
        for child in args[1].children:
            self.params.append(child.value)
    def __str__(self):
        return f'StructCall({self.name}, {self.params})'
    
    
class TreeToLake(Transformer):
    def package(self, args):
        return Package(args[0])
    def import_stmt(self, args):
        return Import(args[0])
    def enum_decl(self, args):
        return EnumDecl(args)
    def struct_decl(self, args):
        return StructDecl(args)
    def function_decl(self, args):
        return FunctionDecl(args)
    def assignment_typed(self, args):
        return AssignmentTyped(args)
    #def struct_call(self, args):
        #return StructCall(args)

    

parser = Lark_StandAlone()

with open('./test.lk') as f:
    code = f.read()
    l = parser.parse(code)
   
   
    print('\033[92m'+l.pretty()+ '\033[0m')

    transform = TreeToLake().transform(l)
   
    print('\033[94m'+transform.pretty()+ '\033[0m')

