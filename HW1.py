
class Account_balance_exeption(Exception):
    pass

class Travel:
    def __init__(self,name,code):
        self.name=name
        self.code=code 
    
    def specific_code(self):
        return "Dear {}, This is your specific travel code: {}".format(self.name , self.code)


class Passenger(Travel):
    def __init__(self,name,code,distance,account_balance,score):

        super(Passenger,self).__init__(name,code)
        self.distance=distance
        self.account_balance=account_balance
        self.score=score
        self.pay_money()

    def pay_money(self):
        self.pay_moooney = self.distance *10
        print("Your travel cost : %i" % self.pay_moooney )
        return self.pay_moooney

    def  residual_account_balance(self):

        if self.account_balance >= self.pay_moooney : 
            self.account_balance -=  self.pay_moooney
            return self.account_balance
        else:
            print("Dear {},Your account balance is not enough" . format(self.name)) 
            raise Account_balance_exeption

rezvan= Passenger('Rezvan','NSCNCSJV', 100 , 1500 ,5)
print(rezvan.pay_money())
print(rezvan.specific_code())

sara= Passenger('Sara','NBNBCJSKN', 1200 , 2500 , 2)
print(sara.pay_money())
# print(sara.residual_account_balance())

class Driver(Travel):
    def __init__(self,name,code, passengers):
        super(Driver,self).__init__(name,code)
        self.passengers=passengers
    
    def receive_for_travel(self):
        money=0
        for pas in self.passengers:
            if pas.code == self.code:
                try: 
                    residual= pas.residual_account_balance()
                    money += pas.pay_money() *0.6
                except Account_balance_exeption:
                    money += 0
        return money

    def add_score(self):
        for pas in self.passengers:
            if pas.code == self.code:
                return 'A score_{} was recorded for you by {}'.format(pas.score , pas.name)


passengerList=[
    Passenger('Rezvan','NSCNCSJV', 100 , 1500, 5),
    Passenger('Sara','NBNBCJSKN', 120 , 2500 ,2),
    Passenger('Mohsen','HBJVCSJ', 50 , 2500 ,3),
    Passenger('Mahsa','JBJNBVK', 90 , 3500 ,5)
]

ali= Driver ('Ali' , 'NBNBCJSKN' , passengerList ) 
print(ali.specific_code())
print("receive_for_travel",ali.receive_for_travel())
print(ali.add_score())
ahmad= Driver ('Ahmad' , 'JBJNBVK' , passengerList ) 
hasan= Driver ('Hasan' , 'HBJVCSJ' , passengerList ) 

class Company:
    def __init__(self,company_name, drivers=[]):

        mystring="There are {} drivers in the {} company." 
        print(mystring.format(len(drivers),company_name))

        self.company_name = company_name   
        self.drivers = drivers

    def receive_for_travel(self):
        money=0
        for driv in self.drivers:
            money += driv.receive_for_travel() * 0.4/0.6  
        return money

snapp= Company('Snapp' ,  drivers=[ali,ahmad,hasan])
print(snapp.receive_for_travel())
