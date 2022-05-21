#!/usr/bin/env python

""" Name Builder, by Ginny (penguinluver222)

Created 09/06/2021
Generates potential names to look at for the pound using syllables and hopefully some statistics on commonality at some point? That'd be cool.

"""
# import needed packages
import pandas as pd
import numpy as np
import datetime as dt

# import local modules
from .dataLoader import _default_bits
from .htmile import tileSet

'''

    ------------- Name Generation Classes + Functions ----------------
'''
#--! Build Name from Matrix ----------------------------------------- #
def _build_names( name_matrix, N, ws_df, stuck=True ):
    segments = pd.DataFrame(columns=name_matrix.piece,index=list(range(N)))
    ng = name_matrix
    for piece in ng.itertuples():
        # index = piece[0]
        # piece name = piece[1]
        L = piece[2]
        # regex = piece[3]


        if piece[1] == piece[3]: # do not sample bits; copy string directly
            segments.iloc[:,piece[0]] = piece[1]
        else:
            samply = ws_df[ws_df.L==L]

            if stuck == True and piece[0] == 0:
                if L < 3:
                    print('WARNING: Stuck prefixes must have at least 3 letters! Generating non-sticky names.')
                    stuck=False
                samply = samply[samply.prefix==stuck]



            samply = samply[samply.bit.str.match(piece[3])]

            if len(samply) < N:

                N = len(samply)
                print('Showing all '+str(N)+ ' unique '+ str(L)+'L names.\n')

            segments.iloc[:,piece[0]] = samply.bit.sample(n = N).reset_index(drop=True)
    names = pd.DataFrame(index=segments.index,columns=['Neopet','L'])
    names.Neopet = ''
    for i in range(len(segments.columns)):
            names.Neopet += segments.iloc[:,i]
    names.Neopet = names.Neopet.str.capitalize()
    names.L = names.Neopet.str.len()
    return names

#--! Name Generator class ------------------------------------------- #
class nameGen:
    """
    A "name generator" object that creates random names of a specified format.

    Args:
        name_format (str):  a string that specifies the desired name format.
        N (int):            Number of names to generate.
                            default: 300
        stuck (bool):       Only generate names with "sticky" prefixes.
                            default: True
        spread:             Distribution of name lengths; only option currently available
                            is 'equal', though this will hopefully change in a later version.

    Returns:
        Name generator object with attributes

    """
    def __init__(self, name_format, N=300, stuck=True, spread='equal', _ns_dat=_default_bits.bitDF):
        # Default Properties
        self.nf = name_format.lower()
        self.stuck = stuck
        self.N = N
        self.spread = spread
        self.ws = _ns_dat

        # Properties to be calculated
        self.Lmin = 0
        self.Lmax = 0
        self.ng = [] # name generator
        self.ng_list = []
        self.names = []
        self.stats = {'time':'','format':'','name_data':''}

        # Run other functions
        self._get_ng()        # create name generator(s)
        tileSet(self.get_names()) # generate names & tileset
        self.show_stats()

    def get_names(self,output=True):
        """
        Creates randomly generated Neopet names using the name generator's settings.

        Args:
            output:     BOOL    Return names DataFrame as output (in addition to assigning to .names)


        Returns:
            Assigns [generator].names variable to
            DataFrame of names [if output=True]
            Neopet      str     Neopet name
            L           int     Length of name

        """
        # update distribution data if N has changed significantly
        if abs(self.N - self.dd.names_per.sum()) > 50:
            self.dd['names_per'] = np.ceil(self.N/self.dd.N_matrix/len(self.dd))\
                                          .astype(int)
        names = pd.DataFrame(columns=['Neopet','L'])

        # generate names for each name generator in self.ng_list
        for name_group in self.dd.itertuples():
            for i,matrix in enumerate(self.ng_list[name_group[0]]):
                temp_names = _build_names( matrix, name_group[3], self.ws, stuck=self.stuck)
                names = pd.concat([names,temp_names],ignore_index=True)

        names = names.drop_duplicates().sort_values(by=['L','Neopet'])\
                     .reset_index(drop=True) # Cleanup names
        self.names = names
        print('Names Updated!\n')

        self._update_stats()

        if output==False:
            return
        else:
            return names

    def show_stats(self):
        """
        Prints statistics about the most recently generated set of Neopet names.
        """
        print('Generator\n'+
              '-----------------------------------')
        print(self.ng)
        print('-----------------------------------\n\n' +
              '--- Name Stats --------\n' +
              'Stuck? ' + str(self.stuck) + '\n' +
              '--------------' )
        print(self.stats['name_data'])
        print('-----------------------\n' +
              'Last Update @ ' + self.stats['time'])


    def _update_stats(self):

        stats = {}
        for i in self.names.L.unique():
            ind = (str(i) + ' Letters')
            n = len(self.names[self.names.L == i])
            stats.update({ ind : n })
        stats.update({
                      'Total Names':len(self.names)
                     })

        stats = pd.DataFrame.from_dict(stats,orient='index')
        stats.columns = [str('# of names')]

        self.stats['name_data'] = stats
        self.stats['time'] = dt.datetime.now().time().strftime("%I:%M:%S %p")

    def _get_ng(self):
        # Create general name generator matrix from user input
        # (ng = "name generator")
        name_format = self.nf

        # Parse user input & set up dataframe
        seglist = name_format.split(',')
        seg_df = pd.DataFrame({}, columns=['pieces','Lmin','Lmax','regex'])

        for seg in seglist:
            if ':' in seg:  # segment types denoted by preceeding :
                seglist2 = seg.split(':')

                # Interprets 'bit' type input
                if 'bit' in seglist2[0]:

                    if len(seglist2[1]) == 2:
                    # check bit length range; if not specified, set to default
                        Lmin = int(seglist2[1][0])
                        Lmax = int(seglist2[1][1])
                    else:
                        Lmin = 1
                        Lmax = 6

                    # Interpret regex if included
                    if len(seglist2[2])>0:
                        regex = r''
                        ui = seglist2[2] #user input
                        i=0
                        ilist = []
                        while i < len(ui):
                            if ui[i] =='[':

                                while ui[i] != ']':
                                    regex += ui[i]
                                    i+=1
                                regex += ']'
                            elif ui[i] == '.':
                                regex += '.'
                                ilist = ilist[:-1]
                            else:
                                if ui[i] == 'x':
                                    regex += '[a-z]'
                                elif ui[i] == 'c':
                                    regex += '[^aeiouy]'
                                elif ui[i] == 'v':
                                    regex += '[aeiouy]'

                            ilist += [i]
                            if len(ilist) > Lmin:
                                raise NameError('Cannot define more characters than minimum word segment (\'bit\') length; \nuse \'.\' as a placeholder instead.')
                            i += 1


                    else:
                        regex = r'[a-z]'*Lmin + r'.'*(Lmax-Lmin)
                    seg_df.loc[len(seg_df)] = ['bit*',Lmin,Lmax,regex]

                else: #interprets 'cvx' style input
#                 'x' in seg or 'v' in seg or 'c' in seg:
                    if len(seglist2[1]) > 0:
                        L = int(seglist2[1])
                        seglist2[0] = seglist2[0]*L
                    for l in seglist2[0]:
                        if l == 'x':
                            seg_df.loc[len(seg_df)] = ['x*',1,1,r'[a-z]']
                        elif l =='v':
                            seg_df.loc[len(seg_df)] = ['v*',1,1,r'[aeiouy]']
                        elif l == 'c':
                            seg_df.loc[len(seg_df)] = ['c*',1,1,r'[^aeiouy]']
            else: # Treat as regular string
                seg_df.loc[len(seg_df)] = [seg,len(seg),len(seg),seg]


        # Update Properties
        self.Lmin = seg_df.Lmin.sum()
        self.Lmax = seg_df.Lmax.sum()
        self.ng = seg_df # name generator

        self._get_ng_list()
        # create list of generator matrices from general generator

    def _get_ng_list(self):
        ng = self.ng
        # collapse pieces into minimum 3 letters for stuck prefixes
        if self.stuck == True:
            if ng.pieces[0] in ['x*','v*','c*','bit*'] == True:
                while ng.loc[0,'Lmin'] < 3:
                    ng.loc[0,'Lmin'] += ng.loc[1,'Lmin']
                    ng.loc[0,'Lmax'] += ng.loc[1,'Lmax']
                    ng.loc[0,'regex'] += ng.loc[1,'regex']
                    ng = ng.drop(1,axis=0).reset_index(drop=True)

                ng.loc[0,'pieces'] = 'bit'

        ng_list = []
        ng_list = [pd.DataFrame(columns=['piece','L','regex'])]

        # create all possible generator matrices from general matrix self.ng
        for piece in ng.itertuples():
            piece_no = piece[0]
            piece_name = piece[1]
            Lmin = piece[2]
            Lmax = piece[3]
            abc_count = piece[4]

            # Creates all possible matrix combinations for 'bits' that have a range of possible values
            if Lmin != Lmax:

                # Make duplicates of existing matrices in ng_list
                ng_list_new = []
                for j in range(len(ng_list)):
                    for i in range((Lmax-Lmin)+1):
                        ng_list_new.append(ng_list[j].copy())

                # Add the range of possible 'bits' onto copied matrices
                L_list = list(range(Lmin,Lmax+1))
                dots = piece[4].count('.')+1 #regex parsing
                for i in range(0,len(ng_list_new),len(L_list)):
                    for l,L in enumerate(L_list):
                        # regex parsing -- replace dots with [a-z]
                        dots -=1
                        regex = piece[4].replace('.','',dots)
                        regex = regex.replace('.','[a-z]')
                        # add new row to ith matrix of ng_list_new
                        ng_list_new[i+l].loc[piece_no] = ['bit*',L,regex]

                ng_list = ng_list_new # Replace ng_list with updated ng_list


            else:
                # Add next matrix row to all matrices in ng_list
                for ng_i in ng_list:
                    ng_i.loc[piece_no] = [piece_name,Lmin,piece[4]]

        # Arrange ng_list into the specified distribution
        # Currently only 'equal' distribution is available
        dist_data = pd.DataFrame({ 'L':list(range(self.Lmin,self.Lmax+1)) } )
        dist_data['N_matrix'] = [0]*len(dist_data)

        ng_list2 = [[]]*len(dist_data)
        for i in ng_list:
            L = i.L.sum()
            dist_data.loc[dist_data.L==L,'N_matrix'] += 1
            ng_list2[L-self.Lmin] = ng_list2[L-self.Lmin] + [i]

        self.ng_list = ng_list2

        dist_data['names_per'] = np.ceil(self.N/dist_data.N_matrix/len(dist_data)).astype(int)
        self.dd = dist_data

    # used for troubleshooting
    # def ngs(self):
    #     for i in self.ng_list:
    #         for j in i:
    #             print(j)
    #             print('---')
