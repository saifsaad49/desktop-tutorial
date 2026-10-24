import pathlib, datetime
from .redact import redact
class Memory:
    def __init__(self, engagement_dir: pathlib.Path):
        self.items = []
        self.dir = pathlib.Path(engagement_dir)
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"cannot create {self.dir}: {e}")
        # early writability check
        probe = self.dir / ".writetest"
        try:
            probe.write_text("ok")
            probe.unlink()
        except OSError as e:
            raise OSError(f"reports dir not writable: {self.dir}: {e}")
    def add(self, ev):
        ev = dict(ev)
        ev['ts'] = datetime.datetime.now().isoformat()
        self.items.append(ev)
    def all(self):
        return self.items
    def save_report(self):
        p = self.dir / "report.md"
        try:
            with open(p, 'w', encoding='utf-8') as f:
                f.write("# Report mythos_Katana\n")
                for it in self.items:
                    f.write(redact(str(it)) + "\n")
        except OSError as e:
            raise OSError(f"cannot write {p}: {e}")
        return p
