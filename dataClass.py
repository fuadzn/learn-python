from dataclasses import dataclass

@dataclass #dataclass decorator
class customerD:
    name: str
    id: int
    surname: str

class customer:
    def __init__(self,name,aid,books):
        self.name = name
        self.id = aid
        self.surname = books
    
Obj1 = customer("Erick", 1254, "Nowak")
Obj2 = customer("Erick", 1254, "Nowak")

Obj3 = customerD("Erick", 1254, "Nowak")
Obj4 = customerD("Erick", 1254, "Nowak")


print("Difference for debuging")
print(Obj1)
print(Obj3)

print("\nDifference in Equality Check")
print(Obj1 == Obj2)
print(Obj3 == Obj4)