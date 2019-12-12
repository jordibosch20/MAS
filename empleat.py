import casa
#We are laoding the module
from casa import Casa
#from the module we are importing the class Casa, this way we only have to write
#Casa(17) to inicialize
#In the first case we have to call casa.Casa(17) to inicialize
class Empleat:
	def __init__(self):
		self.age = 20

if __name__ == "__main__":
	e1 = Empleat()
	print(e1.age)
	c1 = Casa(17)
	print(c1.return_size())