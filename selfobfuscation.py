import ast,random,string,astor
class a:
    def __init__(self):
        self.b={}
        self.c=string.ascii_letters.replace('l','').replace('I','').replace('O','')
        self.d={'self','cls','__init__','__main__','__name__','Exception','True','False','None','print','range','len','str','int','float','list','dict','set','tuple','ast','random','string','astor','NodeTransformer','parse','get_docstring','fix_missing_locations','to_source','Assign','Str','Name','visit','generic_visit','targets','value','annotation','body','args','attr','startswith','isinstance'}
        self.e=0
    def f(self):
        while True:
            if self.e<len(self.c):
                g=self.c[self.e]
                self.e+=1
                return g
            else:
                g=random.choice(self.c)+str(self.e)
                self.e+=1
                return g
    def h(self,i):
        if i in self.d:
            return i
        if i not in self.b:
            self.b[i]=self.f()
        return self.b[i]
    class j(ast.NodeTransformer):
        def __init__(self,k):
            self.k=k
        def visit_Name(self,l):
            l.id=self.k.h(l.id)
            return l
        def visit_FunctionDef(self,l):
            l.name=self.k.h(l.name)
            l.returns=None
            if l.args:
                for m in l.args.args:
                    m.annotation=None
                    m.id=self.k.h(m.id)
            if ast.get_docstring(l):
                l.body=l.body[1:]
            l=self.generic_visit(l)
            return l
        def visit_ClassDef(self,l):
            l.name=self.k.h(l.name)
            if ast.get_docstring(l):
                l.body=l.body[1:]
            l=self.generic_visit(l)
            return l
        def visit_Attribute(self,l):
            if not(isinstance(l.attr,str) and l.attr.startswith('__')):
                l.attr=self.k.h(l.attr)
            return self.generic_visit(l)
    class n(ast.NodeTransformer):
        def visit_AnnAssign(self,l):
            return ast.Assign(targets=[l.target],value=l.value)
        def visit_Expr(self,l):
            if isinstance(l.value,ast.Str):
                return None
            return l
    def o(self,p):
        q=ast.parse(p)
        q=self.n().visit(q)
        q=self.j(self).visit(q)
        ast.fix_missing_locations(q)
        return astor.to_source(q)

if __name__ == '__main__':
    r = a()
    import os

    for filename in os.listdir("."):
        if filename.endswith(".py"):
            s = r.o(open(filename).read())
            new_filename = "obfuscated_" + filename
            with open(new_filename, "w") as f:
                f.write(s)
            print(f"Obfuscated code for {filename} saved to {new_filename}")