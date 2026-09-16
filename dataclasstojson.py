from dataclasses import dataclass, astuple, asdict
import json

@dataclass #dataclass decorator
class customer:
    name: str
    id: int
    surname: str

Obj1 = customer("Endrick",1254,"Nowak")

print(astuple(Obj1))
print(asdict(Obj1))

print(json.dumps(asdict(Obj1)))