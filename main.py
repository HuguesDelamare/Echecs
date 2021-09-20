from controller.main_controller import Controller

class A:
    def __init__(self, val):
        self.val = val

    def printVal(self):
        print(self.val)

if __name__ == "__main__":
   controller = Controller()
   controller.main_menu()
   # Controller.main_menu *method static
    #a = A(2)
    #b = A(10)
    #a.printVal()
    #b.printVal()

else:
    print('error')