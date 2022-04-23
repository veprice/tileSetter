#!/usr/bin/env python

""" Name Builder, by Ginny (penguinluver222)

Created 09/06/2021
Generates potential names to look at for the pound using syllables and hopefully some statistics on commonality at some point? That'd be cool.

"""
import string
import pandas as pd
import numpy as np
import datetime as dt

'''
    --------------- Segment Loading + Cleaning ------------------
'''
#--! Import New Segments -------------------------------------------- #
def new_segments(filepath,old_df=''):
    # Imports a csv file containing a list of word/name new_segments
    # Integrates segments into existing segment data

    segments = pd.read_csv(filepath)
    print('New word segments loaded.')
    clean_seg = segment_cleaner(segments)
    print('New word segments cleaned + determined length + cvc format')
    labeled = label_pres(clean_seg)
    print('New prefixes labeled.')

    input1 = input('Would you like to merge new segments with existing segments? y/n\n')
    if input1 == 'y':
        output = merge_segments(labeled,old_df)
        print('Merge accepted. Returning merged segment dataframe.')
    elif input1 =='n':
        print('Merge declined. Returning new segments only.')
        output = labeled
    else:
        print('Invalid input. Defaulting to return new segments only.')
    return output

#--! Merge new segments into old segments --------------------------- #
def merge_segments(new,old):
    if old == '':
        error('No existing word segment data found.')
    else:
        merged = pd.concat([new,old],ignore_index=True).sort_values(by='bit')
        merged = merged.drop_duplicates().reset_index(drop=True)

        input = ('Word segment data merged. Would you like to save? y/n')
        if input == 'y':
            fname = 'WS_' + str(dt.date.today) + '.csv'
            merged.to_csv('./data/word-segments/' + fname,index=False)
            merged.to_csv('./data/word-segments.csv',index=False)

    return merged

#--! Word Segment Cleaner ------------------------------------------- #
def segment_cleaner(df):
    # Takes in a series of word/name segments
    # Returns dataframe with segments + length + cvc format

    df = df.drop_duplicates().sort_values() # Drop duplicates
    df = df[~df.str.contains(r'[_0-9]')].reset_index(drop=True) # Remove non-letters

    Ls = df.str.len() # get length

    # Construct dataframe
    final = pd.DataFrame({})
    final.insert(loc=0,column='bit',value=df)
    final.insert(loc=1,column='L',value=Ls)
    return final

#--! Label Segments As Prefixes ------------------------------------- #
def update_pres(bit_df, abcs=string.ascii_lowercase):

    stucks = pd.read_csv('./data/stuck-strings.csv')
    stucks = stucks.replace('\_','~',regex=True)
    stucks = stucks[~stucks.prefix.str.startswith('~')].reset_index(drop=True)
    markers = stucks.marker.str.lower()

    print('Updating stuck name prefixes ...')
    bit_df['prefix'] = False
    N_tagged = 1
    for n,i in enumerate(markers):
        if n>0 :
            if markers[n][0] != markers[n-1][0]:
                print(markers[n-1][0].upper()+' markers tagged: '+ str(N_tagged))
                N_tagged = 1
            elif n == len(markers)-1:
                N_tagged += 1
                print(markers[n-1][0].upper()+' markers tagged: '+ str(N_tagged))
            else:
                N_tagged += 1

        sliced = bit_df[bit_df.bit.str.startswith(i[0:3])].copy()
        # Get regex filter string
        F = get_regex(i)

        # Tag prefixes that match regex as 'True'
        sliced.loc[sliced.bit.str.match(F),'prefix'] = True

        bit_df.update(sliced)
    print('Active prefixes updated!')
    return bit_df

#--! Regex Generator for Prefix Filtering --------------------------- #
def get_regex(marker, abcs=string.ascii_lowercase):
    # Takes a "marker" string and generates regex
    # To select all prefixes in that group that
    # come alphabetically after that marker

    m = marker
    # go through marker backwards and omit first 2 letters of marker
    # e.g., dragon -> noga
    for i,L6 in enumerate(m[::-1][:-2]) :
        L5 = m[-i-2]

        if i == 0:
            if m[-1] == '~': # last character is underscore -> do not include last letter in regex selection
                R6 =''
                L5 = abcs[abcs.find(L5)+1]
            else:
                R0 = abcs[abcs.find(L6)]
                R6 = '['+ R0 + '-z]' # range of last letter
            F = L5 + R6

        else:
            if L6 == 'z':
                R0 = abcs[abcs.find(L6)] # avoid bounds errors when L6 = z
            else:
                R0 = abcs[abcs.find(L6)+1] # range starts at letter after L6
            R = '['+ R0 + '-z]'

            F = L5 +'('+R+'|'+F+')' # Add to existing regex


    F = m[0]+F+'.*' # add start indicator and .* to select full segment
    return F

w_s = pd.read_csv('./data/word-segments.csv')

'''
    ------------- Name Generation Classes + Functions ----------------
'''
#--! Build Name from Matrix ----------------------------------------- #
def build_names( name_matrix, N, bits=w_s, stuck=True ):
    segments = pd.DataFrame(columns=name_matrix.piece,index=list(range(N)))
    ng = name_matrix
    for piece in ng.itertuples():
        # index = piece[0]
        # piece name = piece[1]
        L = piece[2]
        # regex = piece[3]


        if piece[1] == piece[3]:
            segments.iloc[:,piece[0]] = piece[1]
        else:
            samply = w_s[w_s.L==L]

            if stuck == True and piece[0] == 0:
                if L < 3:
                    print('WARNING: Stuck prefixes must have at least 3 letters! Generating non-sticky names.')
                    stuck=False
                samply = samply[samply.prefix==stuck]



            samply = samply[samply.bit.str.match(piece[3])]

            if len(samply) < N:
                rep = True
            else:
                rep = False
            segments.iloc[:,piece[0]] = samply.bit.sample(n = N,replace=rep).reset_index(drop=True)
    names = pd.DataFrame(index=segments.index,columns=['Neopet','L'])
    names.Neopet = ''
    for i in range(len(segments.columns)):
            names.Neopet += segments.iloc[:,i]
    names.Neopet = names.Neopet.str.capitalize()
    names.L = names.Neopet.str.len()
    return names

#--! Name Generator class ------------------------------------------- #
class nameGen:
    def __init__(self,name_format,N=300,stuck=True,spread='equal'):
        # Default Properties
        self.nf = name_format.lower()
        self.stuck = stuck
        self.N = N
        self.spread = spread

        # Properties to be calculated
        self.Lmin = 0
        self.Lmax = 0
        self.ng = [] # name generator
        self.ng_list = []
        self.names = []
        self.stats = {'time':'','format':'','name_data':''}

        # Run other functions
        self.get_ng()        # create name generator(s)
        self.get_names()     # generate names

    def ngs(self):
        for i in self.ng_list:
            for j in i:
                print(j)
                print('---')
    def update_stats(self):

        stats = {}
        for i in self.names.L.unique():
            ind = (str(i) + ' Letters')
            n = len(self.names[self.names.L == i])
            stats.update({ ind : n })
        stats.update({' ':'---',
                      'All Names':len(self.names)
                     })


        stats = pd.DataFrame.from_dict(stats,orient='index')
        stats.columns = [str('NUM')]

        self.stats['name_data'] = stats
        self.stats['time'] = dt.datetime.now().time().strftime("%I:%M:%S %p")


        self.show_stats()

    def show_stats(self):
        print('\nNames Updated!')
        print('Generator\n'+'------------------')
        print(self.ng)
        print('------------------')
        print('\n' + 'Name Stats' +
              '\n' + 'Stuck? ' + str(self.stuck) +
              '\n' + '--------------')
        print(self.stats['name_data'])
        print('--------------')
        print('Last Update @ ' + self.stats['time'])


    def get_names(self):

        names = pd.DataFrame(columns=['Neopet','L'])

        for name_group in self.dd.itertuples():
            for i,matrix in enumerate(self.ng_list[name_group[0]]):
                temp_names = build_names( matrix, name_group[3], stuck=self.stuck)

                names = pd.concat([names,temp_names],ignore_index=True)
        names = names.drop_duplicates().sort_values(by=['L','Neopet'])\
                     .reset_index(drop=True)
        self.names = names
        self.update_stats()
        return names

    def get_ng(self):
        # Create generator
        name_format = self.nf
        seglist = name_format.split(',')
        seg_df = pd.DataFrame({}, columns=['pieces','Lmin','Lmax','regex'])

        for seg in seglist:
            if ':' in seg:  # segment types denoted by preceeding :
                seglist2 = seg.split(':')

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

                else:
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
            else:
                seg_df.loc[len(seg_df)] = [seg,len(seg),len(seg),seg]


        # Update Properties
        self.Lmin = seg_df.Lmin.sum()
        self.Lmax = seg_df.Lmax.sum()
        self.ng = seg_df # name generator

        self.get_ng_list()

    def get_ng_list(self,bits=w_s):
        ng = self.ng
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

        for piece in ng.itertuples():
            piece_no = piece[0]
            piece_name = piece[1]
            Lmin = piece[2]
            Lmax = piece[3]
            abc_count = piece[4]


            if Lmin != Lmax:

                ng_list_new = []
                for j in range(len(ng_list)):
                    for i in range((Lmax-Lmin)+1):
                        ng_list_new.append(ng_list[j].copy())

                L_list = list(range(Lmin,Lmax+1))
                dots = piece[4].count('.')
                for i in range(0,len(ng_list_new),len(L_list)):
                    for l,L in enumerate(L_list):
                        regex = piece[4].replace('.','',dots)
                        regex = regex.replace('.','[a-z]')
                        ng_list_new[i+l].loc[piece_no] = ['bit*',L,regex]

                        dots -=1

                ng_list = ng_list_new


            else:
                for ng_i in ng_list:
                    ng_i.loc[piece_no] = [piece_name,Lmin,piece[4]]

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


# # ---> Load default prefix/suffix set
# pres, pres_, marks = loadPrefixes(f_sticky,f_prefix)
# sufs = loadSuffixes(f_suffix)
# ################################################################################
# pres_max = pres.L.max()
# sufs_max = sufs.L.max()
# v_s = abcs[abcs.Letter.isin(['a','e','i','o','u','y'])]
# c_s = abcs[~abcs.Letter.isin(['a','e','i','o','u','y'])]
#
# ############################################################### nameBuilder ####
# class nameBuilder:
#     # A thing that lets you "build" a name by defining the 'bits' the name is made out of
#     # 'prefix' bit will sample from prefix data
#     # 'suffix' bit will sample from suffix data
#     # any other input string will be used for all names
#     #     (e.g., 'ay' is first 'bit' --> all names will start with 'Ay'
#
#     # ----> Set up
#     def __init__(self,N=300):
#
#         self.constructor = pd.DataFrame(columns=['bit','L','letters'])
#
#         # Set up dataframe variables
#         self.N_names = N
#         self.segments = False
#         self.names = False   #created in once .construct() is called
#
#         self.stats = {'time':'','format':'','name_data':''}
#
#
#
#     # ----> adds prefix 'bit' to constructor
#     # def add_prefix(self, L=(3, pres_max), lettrs = ('a','z')):
#     #
#     #     if type(L) == int:
#     #         L = ( L, L ) #set lmin and Lmax
#     #     if type(lettrs) == str:
#     #         lettrs = (lettrs,lettrs)
#     #
#     #     if L[0] < 3:
#     #         error('Prefixes must be at least 3 letters long!')
#     #         return
#     #
#     #     self.constructor = self.constructor.append({
#     #         'bit':      'prefix',
#     #         'L':        ( L[0], L[1] ),
#     #         'letters':  (lettrs[0],lettrs[1])
#     #         },ignore_index=True)
#     #
#     #
#     # # ----> adds suffix 'bit' to constructor
#     # def add_suffix(self, L=(1,sufs_max),lettrs = ('a','z')):
#     #
#     #     if type(L) == int:
#     #         L = (L, L)
#     #     elif type(L) != tuple:
#     #         return ('L must be int or tuple')
#     #
#     #     if type(lettrs) == str:
#     #         lettrs = (lettrs,lettrs)
#     #     elif type(lettrs) != tuple:
#     #         return('L must be string or tuple)')
#     #
#     #
#     #     self.constructor = self.constructor.append({
#     #         'bit':      'suffix',
#     #         'L':        ( L[0], L[1] ),
#     #         'letters':  ( lettrs[0],  lettrs[1] )
#     #         }, ignore_index=True)
#     #     return
#
#     # ----> adds user-defined string 'bit'
#     def add_bit(self,bit,L=False,ltrs = False,
#                 pres_max = pres_max, sufs_max = sufs_max):
#         #'prefix','suffix','c_','v_'
#         if L == False:
#             if bit =='prefix':
#                 L_ = (3,pres_max)
#             elif bit =='suffix':
#                 L_ = (1,sufs_max)
#             elif bit in ['c_','v_','l_']:
#                 L_ = 1
#             else:
#                 L_ = len(bit)
#         else:
#             L_ = L
#
#         if ltrs == False:
#             if bit in ['prefix','suffix','c_','v_','l_']:
#                 ltrs_ = ('a','z')
#             else:
#                 ltrs_ = ltrs
#
#         self.constructor = self.constructor.append( {
#             'bit': bit,
#             'L': L_,
#             'letters': ltrs_
#             }, ignore_index=True)
#
#
#
#     def edit_bit(self,idx,bit=False,L=False,ltrs=False):
#         copy = self.constructor.loc[idx]
#         if bit != False:
#             copy.bit = bit
#
#         if L != False:
#             copy.L = L
#
#         if ltrs != False:
#             copy.letters = ltrs
#
#         self.constructor.loc[idx] = copy
#
#         print('Bit updated!')
#         print('Constructor matrix is now:')
#         print(self.constructor)
#
#
#     def del_bit(self,idx):
#         self.constructor = self.constructor.drop(index=idx)
#
#         print('Bit deleted!')
#         print('Constructor matrix is now:')
#         print(self.constructor)
#
#     def swap_bits(self,idx1,idx2):
#         copy = self.constructor.copy()
#         self.constructor.loc[idx2] = copy.loc[idx1]
#         self.constructor.loc[idx1] = copy.loc[idx2]
#
#
#     # ----> Constructs name from constructor matrix
#     def tileSet(self, N=300, pres=pres, sufs=sufs, abcs=abcs_,
#                 vs = v_s, cs = c_s):
#         if type(N) == int:
#             self.N_names = N
#
#         self.segments = pd.DataFrame(index=range(0,self.N_names))
#
#         # ---> iterate through name 'bits'
#         name_format = '|'
#         for i in self.constructor.index:
#
#             bit   = self.constructor.at[i,'bit']
#
#
#             seggi = bit + '_' + str(i)
#             name_format += bit + '|'
#
#
#             # ---> Sample from chosen data
#             if bit in ['prefix','suffix','c_','v_','l_']:
#                 if bit in ['c_','v_','l_']:
#                     rep=True
#                 else:
#                     Lmin  = self.constructor.at[i,'L'][0]
#                     Lmax  = self.constructor.at[i,'L'][1]
#                     rep = False
#
#                 let = [ self.constructor.at[i,'letters'][0].lower(),
#                         self.constructor.at[i,'letters'][1].lower() ]
#
#                 #df[~df.col.str.get(0).isin(['t', 'c'])]
#                 az  = abcs_[abcs_.Letter.isin(let)].index.tolist()
#                 bcs = abcs_.Letter[az[0]:az[1]+1].tolist()
#
#                 # ---> Choose data to sample
#                 if bit == 'prefix':
#                     samply = pres[pres.L <= Lmax]
#                     samply = samply.rename(columns={'prefix': 'bit'})
#
#                 elif bit == 'suffix':
#                     samply = sufs[sufs.L <= Lmax]
#                     samply = samply.rename(columns={'suffix': 'bit'})
#
#                 elif bit == 'c_':
#                     samply = cs.rename(columns={'Letter':'bit'})
#                 elif bit == 'v_':
#                     samply = vs.rename(columns={'Letter':'bit'})
#                 elif bit == 'l_':
#                     samply = abcs.rename(columns={'Letter':'bit'})
#
#                 else:
#                     samply = []
#
#
#
#                 samply = samply[samply.bit.str.get(0).isin(bcs)]
#
#                 # ---> reduce # of generated names if sampling data is too small
#                 if (len(samply) < self.N_names) and rep == False:
#
#                     self.segments = self.segments.drop(\
#                                         index=range(len(samply),self.N_names))
#                     self.N_names = len(samply)
#
#
#
#                 self.segments[seggi] = samply.bit.sample(n = self.N_names,
#                                                          replace=rep).tolist()
#
#             # ---> or copy bit for entire column
#
#             else:
#                 self.segments[seggi] = bit
#
#
#         self.stats['format'] = name_format.strip() # updates word stats
#
#         # ---> turn name segments into names
#         self.names = pd.DataFrame(index = self.segments.index,
#                                   columns=['L','Neopet'])
#         self.names.Neopet = ''
#
#         for i in self.segments.columns:
#             self.names.Neopet +=  self.segments[i]
#
#
#         # ---> Get name lengths, sort, and clean up
#         self.names.L = self.names.Neopet.str.len()
#         self.names = self.names.drop_duplicates()\
#                          .sort_values(by=['L','Neopet'])\
#                          .reset_index(drop=True)
#
#         # ---> Capitalize the names
#         self.names.Neopet = self.names.Neopet.str.capitalize()
#
#         # ---> Apply webpage function
#         self.update_stats()
#
#         return self.names
#
#
#     # ---> updates name statistics
#     def update_stats(self):
#         stats = {}
#         for i in self.names.L.unique():
#             ind = (str(i) + ' Letters')
#             n = len(self.names[self.names.L == i])
#             stats.update({ ind : n })
#         stats.update({' ':'---',
#                       'All Names':len(self.names)
#                      })
#
#
#         stats = pd.DataFrame.from_dict(stats,orient='index')
#         stats.columns = [str('NUM')]
#
#         self.stats['name_data'] = stats
#         self.stats['time'] = dt.datetime.now().time().strftime("%I:%M:%S %p")
#
#
#         self.show_stats()
#
#     def show_stats(self):
#
#         print('Constructor\n'+'------------------')
#         print(self.constructor)
#
#         print('------------------')
#         print('\n' + 'Name Lengths' +
#               '\n' + '--------------')
#         print(self.stats['name_data'])
#         print('--------------')
#         print('Last Update @ ' + self.stats['time'])
#
#     def to_webpage(self,link_to='petpage'):
#         htmile.make_page(self.names,link_to)
#         self.update_stats()
#
# print('Done loading the nameBuilder!')

################################################## Functions to make Pages ####

# #-! Make Webpage --------------------#
# def make_page(names,linky='petpage'):
#
#     names['Neopet'] = names.Neopet.str.replace('~','_')
#
#     css_tag = '<link rel="stylesheet" type="text/css" '+ \
#               'href="' + f_css + '">'
#
#     # ---> generate img + link urls
#     names = get_links(names)
#
#     # ---> Page build starts here
#     page = [css_tag]
#
#     # ---> + 1 'letter' div for each name length
#     for i in names.L.unique():
#         iLs = str(i) + ' Letters'
#         page += ['<div class="letter">']
#         page += ['<h2>'+str(iLs)+'</h2>']
#
#         nameLs = names[names.L == i]
#
#         # ---> Generate image+link code for 'pet' divs
#         linkme = nameLs.Neopet + '<br>' + img_wrap(nameLs.img)
#         divp = div_wrap(a_wrap(linkme,nameLs[linky]))
#
#         page += divp.values.tolist() + ['</div><br>']
#
#     # ---> Save webpage code using Panda's .to_csv
#     webpage = pd.Series(page)
#     webpage.to_csv(f_webpage,
#                     sep=',',header=False,index=False,quoting=csv.QUOTE_NONE)
#     return
#
# #-! Get links for names ----------------------------#
# def get_links(names):
#     names['petpage'] = 'http://neopets.com/~' + names.Neopet
#     names['pound']   = 'http://neopets.com/pound/adopt.phtml?search=' + names.Neopet
#     names['img'] = 'http://pets.neopets.com/cpn/' + names.Neopet + '/1/1.png'
#     return names
#
# #-! HTML wrapper functions --------------------------#
# def div_wrap(to_wrap,clss='pet'):
#     tagopen = '<div class="' + clss + '">'
#     tagclosed = '</div>'
#     return tagopen + to_wrap + tagclosed
#
# def a_wrap(to_wrap,link_url):
#     tagopen0 = '<a href="'
#     tagopen1 = '">'
#     tagclosed = '</a>'
#     return tagopen0 + link_url + tagopen1 + to_wrap + tagclosed
#
# def img_wrap(img_urls):
#     tagopen = '<img src="'
#     tagclosed = '" />'
#     return tagopen + img_urls + tagclosed
