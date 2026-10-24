import pathlib, json, datetime
class Memory:
    def __init__(self):
        self.items=[]
        self.cache={}
    def add(self, ev):
        ev['ts']=datetime.datetime.now().isoformat()
        self.items.append(ev)
    def all(self): return self.items
    def save_report(self, path):
        p=pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        with open(p,'w',encoding='utf-8') as f:
            f.write("# تقرير mythos_Katana\n\n")
            for it in self.items:
                f.write(f"- {it['ts']}: {it}\n")
        print(f"Report saved to {path}")
