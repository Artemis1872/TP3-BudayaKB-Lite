class FBUser:
    def __init__(self, birthday, fullname):
        self.birthday = birthday
        self.fullname = fullname
        self.firstname = self.fullname.split()[0]
        self.lastname = self.fullname.split()[-1]


agus = FBUser("9 Januari", "Agus Septiadi")
print(agus.birthday)
print(agus.fullname)
print(agus.firstname)
print(agus.lastname)

dennis = FBUser("9 Juni", "Dennis Al Baihaqi Walangadi")
print(dennis.birthday)
print(dennis.fullname)
print(dennis.firstname)
print(dennis.lastname)