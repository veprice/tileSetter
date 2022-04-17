### Data Handling Functions

"""
Pet Database
by Cady (penguinluver222)
"""
import pandas as pd
import datetime as dt

from dataLoader import petpath
petpath = '../data/pet_database/my-pet-database/'
new_stucks_path = '../data/pet_database/stuck_csvs/'
new_untakens_path = '../data/pet_database/untaken_csvs/'
from_date = '2021-09-10'

################################################## Loading & Using Pet Data ####
def loadDB(backup=from_date,filepath = petpath):
    #path = filepath + from_date + '.csv'
    # pet_DB = pd.read_csv(path,
    #                  index_col='Neopet')
    filepath += 'stuck_pets.csv'
    pet_DB = pd.read_csv(filepath, index_col='Neopet')
    pet_DB['updated'] = pd.to_datetime(pet_DB['updated'],infer_datetime_format=True)
    pet_DB.saver = SaveCount()
    return pet_DB



def loadNameDB(filepath=petpath):
    filepath += 'untaken_names.csv'
    name_db = pd.read_csv(filepath, index_col='Neopet')
    name_db = name_db
    name_db.saver = SaveCount()
    return name_db




# class Checker:
#     def __init__(self,db=names):
#         self.db = db
#     def tileSet(self,**kwargs):
#         sli



class dbChecker:
    def __init__(self,db):
        self.db = db
    def tileSet(self,N='all',**kwargs):
        dbslice = self.db.copy()
        for key, value in kwargs.items():
            # print('key: ' + str(key) + '; value: '+ str(value))
            # print(str(dbslice[key]==False))
            if key == 'L':
                dbslice = dbslice[ dbslice[key] >= value ]
            else:
                dbslice = dbslice[ dbslice[key] == value ]
        if type(N) == int:
            dbslice = dbslice.sample(n = N)
        return dbslice.reset_index()


        #print(petslice)



def get_pets(pet_slice):

    beep = {'Neopet':pet_slice.index.tolist(),
            'L' : pet_slice.L.tolist()}

    return pd.DataFrame(beep)

class SaveCount:
    def __init__(self):
        self.counter = 0
        self.save = False
        #self.saveto = save_path


    def check(self):

        if self.counter == 5:
            self.counter = 0
            self.save = True
        else:
            self.counter += 1
            self.save = False
        return


pets = loadDB()
names = loadNameDB()

def update3(db, name, **kwargs):
    print('****** Updating: ' + name + ' ******')
    if 'updated' in db.columns:
        print('\tLast update: ' +
              last_update + ' ---> ' + dt.datetime.today().strftime('%Y-%m-%d') )
    copy = db.loc[name]
    for key,val in kwargs.items():
        copy[key] = val


    confirm = input('Continue with update? y/n \n')

    if confirm == 'y':
        if 'updated' in db.columns:
            copy.updated = dt.datetime.today()
        db.loc[name] = copy

def nameToPet(petname,color,species,nameDB,petDB):
    nameDB = nameDB.copy().swapaxes(0,1)
    petDB = petDB.copy().swapaxes(0,1)


    new_pet = nameDB[petname].copy()#nameDB.pop(petname).squeeze()
    print(new_pet)
    petDB[petname] = ''

    petDB[petname]['Color'] = color
    petDB[petname]['Species'] = species
    petDB[petname]['UC'] = False
    petDB[petname]['Painted'] = isPainted1(color,species)
    petDB[petname]['nameQ'] = name_quality(petname)[0]
    petDB[petname]['RN'] = new_pet.RN
    petDB[petname]['RW'] = new_pet.RW
    petDB[petname]['MS'] = new_pet.MS
    petDB[petname]['BD'] = False
    petDB[petname]['star'] = new_pet.star
    petDB[petname]['status'] = 'adopted'
    petDB[petname]['updated'] = dt.date.today()
    petDB[petname]['page_url']= 'hush'
    petDB[petname]['pound_url']= 'no'
    petDB[petname]['img']= 'no'

    petDB =petDB.swapaxes(0,1)
    petDB = petDB.sort_values(by='updated',ascending=False).sort_index(key=lambda x: x.str.lower())
    return petDB#nameDB.swapaxes(0,1),petDB




def update2(petname,db=pets, color=False, species=False, status=False, notables=False):
     # notables = RN, RW, BD, MS, star

    last_update = db.at[petname,'updated'].strftime("%Y-%m-%d")
    copy = db.loc[petname].copy()

    print( '****** Updating ' + petname + '\'s entry ******' )

    if species != False:
        copy.Species = species
        print('\tSpecies: ' +
              db.Species[petname] + ' ---> ' + copy.Species)

    if color != False:
        copy.Color = color

        basics = ['Blue','Red','Green','Yellow']
        grundo_basics = ['Purple','White','Brown']
        if color in basics:
            copy.Painted = False
        elif (color in grundo_basics) and db.Species.petname == 'Grundo':
            copy.Painted = False
        else:
            copy.Painted = True

        print('\tColor: ' +
              db.Color[petname] + ' ---> ' + copy.Color)
        print('\tPainted: ' +
              db.Painted[petname] + ' ---> ' + copy.Painted)

    if status != False:
        copy.status = status

        print('\tStatus: ' +
              db.status[petname] + ' ---> ' + copy.status )

    if type(notables) == list:
        for i in notables == True:
            if '~' in i == True:
                i = i.replace('~','')
                copy[i] = False
            else:
                copy[i] = True

            print('\t' + i + ' = ' + db.at[petname,i] + ' ---> ' +
                  i + ' = ' + copy[i])

    print('\tLast update: ' +
          last_update + ' ---> ' + dt.datetime.today().strftime('%Y-%m-%d') )
    confirm = input('Continue with update? y/n \n')

    if confirm == 'y':
        copy.updated = dt.datetime.today()
        db.loc[petname] = copy

        db.saver.check()
        if db.saver.save == True:
            print( '!! Autosave triggered !!')
            savePetDB(db)


def update(db,Neopet,column,new_value):
    if Neopet not in db.index:
        print('Pet not found in database. Please check spelling and try again!')
        return

    db.at[Neopet,column] = new_value
    last_update = db.at[Neopet,'updated'].strftime("%Y-%m-%d")
    db.at[Neopet,'updated'] = dt.datetime.today()

    confirm ='Updating: ' + Neopet + ' the ' + db.Color[Neopet] + \
              ' ' + db.Species[Neopet] +\
              '\n' + column + ' updated to \'' + new_value + '\'!\n' +\
              'Last Update was on ' + last_update + '\n'

    print(confirm)

    db.saver.check()
    if db.saver.save == True:
        print( '!! Autosave triggered !!')
        savePetDB(pets)
    return


################################################### Data Cleaning Functions ####

#-! Determines VWN/WN/DN/BN ---------------------------------#
def name_quality(pet_names):
    # if format is Xxxxxxxx AND <= 8 letters
    if type(pet_names) == pd.DataFrame:
        petlist = pet_df.index.tolist()
    elif type(pet_names)==str:
        petlist = [pet_names]
    else:
        return


    qualities = []
    for i in petlist:
        if i.isalpha() == True:

            if i == i.capitalize():
                if len(i) <= 9:
                    quality = 'VWN'

                else:
                    quality = 'WN'
            else:
                quality = 'DN'

        elif len(re.sub('[^0-9]','', i)) < 1:
            if len(i) <= 10:
                quality = 'DN'

            else:
                quality = 'BN'

        else:
            quality = 'BN'

        qualities.append(quality)

    return qualities

#-! Painted ----------------------------------------------- #
def isPainted(pet_df):

    basics = ['Blue','Red','Green','Yellow']
    grundo_basics = ['Purple','White','Brown']

    beepa = pet_df.copy()
    beepa['Painted'] = True


    beepa.Painted = beep

    a.Painted.mask( (beepa.Species == 'Grundo') & \
                (beepa.Color.isin(grundo_basics)) ,False)
    beepa.Painted = beepa.Painted.mask(beepa.Color.isin(basics),False)


    return beepa.Painted

def isPainted1(color,species):
    basics = ['Blue','Red','Green','Yellow']
    grundo_basics = ['Purple','White','Brown']
    if color in basics:
        Painted = False
    elif (color in grundo_basics) and species == 'Grundo':
        Painted = False
    else:
        Painted = True
    return Painted
#-! ----- # updates pound status on older datasets -------- #
def poundStatus(pet_df):
    beepa = pet_df.status

    beepa = beepa.mask(beepa == False,'adopted')
    beepa = beepa.mask(beepa == True,'pound')

    return beepa


############################################### Database Updating Functions ####
def loadNewPets(from_date='today',path = new_stucks_path):
    filepath = new_stucks_path + from_date + '.csv'
    beep4 = pd.read_csv(filepath)

    petDB_cols = ['Color','Species','UC','Painted',
                  'L', 'nameQ','RN','RW','MS','BD',
                  'star','status', 'updated',
                  'page_url','pound_url','img']


    beep4.index = beep4.Neopet
    beep4['IMG'] = beep4['http://pets.neopets.com/cpn/']
    beep4['updated'] = beep4.updated + '/2021'
    beep4['updated'] = pd.to_datetime(beep4['updated'],infer_datetime_format=True)
    beep4['pound_url'] = 'http://neopets.com/pound/adopt.phtml?search=' + beep4.index

    beep4.columns = ['img','page_url','status','DR0','Color','Species','UC',
                     'L','star','RN','RW','MS','BD','updated',
                     'DR1','DR2','pound_url']


    beep4 = beep4[~(beep4.L == 0)]
    beep4 = beep4.drop(['DR0','DR1','DR2'],axis=1)
    beep4['Painted'] = isPainted(beep4)
    beep4['nameQ'] = name_quality(beep4)


    beep4 = beep4[petDB_cols]


    return beep4

    #-! Update database with new pets -----------#
def updatePets(old_pets,new_pets):
    old_pets['updated'] = pd.to_datetime(old_pets['updated'],infer_datetime_format=True)

    beep_all = pd.concat([old_pets,new_pets])

    # sort first by name, then by date
    beep_all = beep_all.sort_values(by='updated',ascending=False).sort_index(key=lambda x: x.str.lower())

    # drop duplicate names, keeping the most recent entry
    beep_all2 = beep_all[~beep_all.index.duplicated(keep='last')]

    return beep_all2

#!- Save database --------------------------#

def savePetDB(pet_db,category,path=petpath):

    pet_db = pet_db.sort_values(by='updated',ascending=False).sort_index(key=lambda x: x.str.lower())

    folder = path
    backup_filename = dt.datetime.now().strftime("%Y-%m-%d") + \
                      '.csv'
    if category == 'stuck':
        filename = 'stuck_pets.csv'
        backup_folder = path + 'stuck_backups/'

    elif category == 'names':
        filename = 'untaken_names.csv'
        backup_fodler = path + 'name_backups/'

    else:
        print('Category not recognized; must be \'stuck\' or \'names\'. \
               Please try again.')
        return

    backup_path = backup_folder + backup_filename
    main_path = folder + filename

        # save backup
    pet_db.to_csv(backup_path)
    pet_db.to_csv(main_path)

    print('Saved data to: ' + main_path)
    print('Saved backup to: ' + backup_path)

    return
