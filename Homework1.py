import sys
import pickle

class Person:
    def __init__(self, lastName, firstName, middleInitial, id, phone):
        self.lastName = lastName
        self.firstName = firstName
        self.middleInitial= middleInitial
        self.id = id
        self.phone = phone
    
    def display(self):
        print("Employee id:", self.id)
        print("\t" + self.firstName, self.middleInitial, self.lastName)
        print("\t" + self.phone + "\n")


#formats each name (accounts for multiple first or last names)
def processNames(unformattedNames):
    LastNames = ""
    for index in range(len(unformattedNames)):
        LastName = unformattedNames[index]
        LastName = LastName.lower()[0].upper()
        LastNames+= LastName
    return LastNames


#returns middle initial when given middle name, x if no middle name
def processMiddleInitial(MiddleNames):
    MiddleInitial = MiddleNames
    if len(MiddleInitial) == 0:
        MiddleInitial = "X"
    else:
        MiddleInitial = MiddleInitial[0]

    return MiddleInitial.upper()


#processes ID, if invalid- asks user to reenter until it isnt
def processID(idNumber, dict):
    personID = idNumber

    if personID in dict:
        print("\nError: There is a duplicate id in the input file\n")

    personID = personID.replace("-","").replace(" ","")
    while (len(personID)!= 6) or (not personID[0].isalpha()) or (not personID[1].isalpha()) or (not personID[2].isnumeric()) or (not personID[3].isnumeric()) or (not personID[4].isnumeric()) or (not personID[5].isnumeric()):
        print("ID invalid:", personID)
        print("ID is two letters followed by 4 digits")
        personID = input("Please enter a valid id: ")

    return personID  


#processes phonenumber, if invalid- asks user to reenter until it isnt
def processPhone(phoneNumber):
        personPhone = phoneNumber.replace("\n", "")
        personPhoneStripped = personPhone.replace("-","").replace(" ","").replace("\n","").replace(".", "")
        #print("replaced is", personPhoneStripped)
        while (not len(personPhone)== 12) or (not personPhoneStripped.isnumeric()) or not personPhone[3] == "-" or not personPhone[7] == "-":
            print("Phone", personPhone, "is invalid")
            print("Enter phone number in form 123-456-7890")
            personPhone = input("Enter phone number: ")
        return personPhone


#processes the input given the user given path name
def process_input(relative_path):
    DictOfPeople ={}
    
    #shold put this in a try just in case it doesnt open
    file = open(relative_path, 'r')
    Lines = file.readlines()

    for index in range(1, len(Lines)):
        PersonAttributes = Lines[index].split(",")

        #0 is Last Name
        PersonAttributes[0] = processNames(PersonAttributes[0])

        #1 is First Name
        PersonAttributes[1] = processNames(PersonAttributes[1])

        #2 is Middle Initial
        PersonAttributes[2] = processMiddleInitial(PersonAttributes[2])

        #3 is the ID
        PersonAttributes[3] = processID(PersonAttributes[3], DictOfPeople)

        #4 is the Phone
        PersonAttributes[4] = processPhone(PersonAttributes[4])

        #create new person with all our processed data and enter into dict
        newPerson = Person(PersonAttributes[0], PersonAttributes[1], PersonAttributes[2], PersonAttributes[3], PersonAttributes[4])
        
        DictOfPeople[newPerson.id] = newPerson

    return DictOfPeople



def main():
    try:    
        RelativePath = str(sys.argv[1])
    
    except:
        print("There was no path name provided or an en eror occurred trying to process the path name")
        quit()
    
    PeopleDict = process_input(RelativePath)

    with open('PeopleDict.pickle', 'wb') as filename:
        pickle.dump(PeopleDict, filename, protocol=pickle.HIGHEST_PROTOCOL)

    with open('PeopleDict.pickle', 'rb') as filename:
        PeopleDictFromFile = pickle.load(filename)

    print("Employee List:\n")
    for person in PeopleDictFromFile:
        PeopleDictFromFile[person].display()
        

main()
