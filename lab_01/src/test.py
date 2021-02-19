import sympy as sy

c1 = sy.Circle(sy.Point(0, 0), 3)
c2 = sy.Circle(sy.Point(3, 0), 3)

print(c1.encloses(c2))
