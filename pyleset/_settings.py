# Defaults for pylesetter library
import pkg_resources
import pandas as pd
import datetime as dt
from pprint import pprint
# Directory to write output files to

class bitData:
    def __init__(self,use_defaults=True):
        if use_defaults == True:
            data_dir = 'data/_defaults/'
            dir_path = pkg_resources.resource_filename(__name__,data_dir)
            bits_name   = 'name-bits.csv'
            stucks_path = 'stuck-strings.csv'
            backups_dir = 'backups/'

            updated = resource_listdir(__name__, backups_dir)[-1]
            updated = dt.datetime.strptime(updated[5:15],'%Y-%m-%d')


        else:
            raise('Non-default name segment data are not yet supported.')

        self.settings = {   'filename'     : bits_name,
                            'in_directory' : dir_path,
                            'backup_dir'   : backups_dir,
                            'stuck_list'   : stucks_path,
                          }

        print('Retrieving data with the following settings:')
        pprint(self.settings,indent=2,width=1)
        self.bitDF = pd.read_csv(bits_path, encoding='latin-1')
        self.stuckDF = pd.read_csv(stucks_path, encoding='latin-1')

        print('Data Loaded!\n\n' +
              'Last update: '+ updated.strfrtime('%b %d %Y')+'.\n')

        self.update_pres()

    def update_pres(self):
        check = input('Update sticky prefixes? (y/n)\t -> ')

        if check == 'y':
            self.backup()
            self.update_csv()
        else:
            print('Skipped updating prefixes.')

    def backup(self):
        check = input('Save backup? (y/n)\t-> ')
        if check == y:
            filename = self.settings['in_directory'] + \
                       self.settings['backups_dir'] + \
                       'bits-' + updated.strfrtime('%Y-%m-%d') + \
                       '.csv'
            self.bitDF.to_csv(filename,index=False)
