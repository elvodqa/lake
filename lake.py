from lake_parser import Lark_StandAlone, Transformer

class Statement:
    pass

class Package(Statement):
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Package({self.name})'

class Import(Statement):
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Import({self.name})'

class EnumMember:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'EnumMember({self.name})'
    def __repr__(self):
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
    
class StructField:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __str__(self):
        return f'StructField({self.name}, {self.type})'
    def __repr__(self):
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

class FunctionParam:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def __str__(self):
        return f'FunctionParam({self.name}, {self.type})'
    def __repr__(self):
        return self.__str__()

class FunctionDecl(Statement):
    def __init__(self, args):
        self.name = args[0].children[0].children[0].value
        self.params = []
        self.return_type = args[0].children[2].children[0].children[0].value if len(args[0].children[2].children) > 0 else None
        length = len(args)
        for child in args[0].children[1].children:
            self.params.append(FunctionParam(child.children[0].children[0].value, child.children[1].children[0].value))

    def __str__(self):
        return f'FunctionDecl({self.name}, {self.params}, {self.return_type})'
    
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
    

parser = Lark_StandAlone()

with open('./test.lk') as f:
    code = f.read()
    l = parser.parse(code)
   
   
    print('\033[92m'+l.pretty()+ '\033[0m')

    transform = TreeToLake().transform(l)
   
    print('\033[94m'+transform.pretty()+ '\033[0m')

