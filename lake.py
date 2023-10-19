from lake_parser import Lark_StandAlone, Transformer


class Package:
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Package({self.name})'

class Import:
    def __init__(self, args):
        self.name = args.children[0].value
    def __str__(self):
        return f'Import({self.name})'
    

class TreeToLake(Transformer):
    def package(self, args):
        return Package(args[0])
    def import_stmt(self, args):
        return Import(args[0])
    

parser = Lark_StandAlone()

with open('./test.lk') as f:
    code = f.read()
    l = parser.parse(code)
    #print(l.pretty())

    transform = TreeToLake().transform(l)
    print(transform.pretty())

