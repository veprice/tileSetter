#!/usr/bin/env python

""" Name Builder, by Ginny (penguinluver222)

Created 09/06/2021
Generates potential names to look at for the pound using syllables and hopefully some statistics on commonality at some point? That'd be cool.

"""
import string
import pandas as pd
import datetime as dt

from dataLoader import f_sticky, f_prefix, f_suffix
#import htmile

# ----> Load alphabet with and without underscores
abcs = pd.DataFrame(list(string.ascii_lowercase),columns=['Letter'])
abcs_ = abcs.append({'Letter':'~'},ignore_index=True)


######################################################### Loading Functions ####

#-! Importing Current Prefixes ---------------------------------#
def updateStuckPrefixes(prefix_path,stucks_path,alphabet=abcs_):

    print('Prefixes from file:   ' + prefix_path)
    print('Stickies from file:   ' + stucks_path)

    # ----> Load prefixes <----
    pre = pd.read_csv(prefix_path,names=['prefix'])
    pre.prefix = pre.prefix.str.lower()
    pre['L'] = pre.prefix.str.len()

    print('4L+ prefixes:         ' + str(len(pre)))

    # ----> Load current stuck 3L strings <----
    stuck_strings = pd.read_csv(stucks_path)
    stuck_strings.prefix = stuck_strings.prefix.str.lower()
    stuck_strings.marker = stuck_strings.marker.str.lower()

    pr3,markers = loadStuck3Ls(stuck_strings)
    print('3L prefixes:          ' + str(len(pr3)))

    # ----> Combine 3L and 4L+ prefixes <----
    pre = pd.concat([pre, pr3],ignore_index=True)
    pre = pre.sort_values(by=['prefix','L']).reset_index(drop=True)
    pre = pre.drop_duplicates().reset_index(drop=True)


    # ----> Drop inactive prefixes <----
    N1 = len(pre[~pre.prefix.str.slice(stop=3).isin(pre.prefix[pre.L==3])])
    pre = pre[pre.prefix.str.slice(stop=3).isin(pre.prefix[pre.L==3])]
    pre, N2 = applyMarkers(pre,'prefix',markers)

    print('Outdated Prefixes:    ' + str(N1+N2))
    print('Total Prefixes:       '+  str(len(pre)))

    # ----> Write CSV <----
    pre.replace('\~','_',regex=True)\
        .to_csv('./word_segments/my-segments/prefixes_current.csv', index=False)


    pre.replace('\_','~', regex=True)
    return pre,markers

#-! Load all 3L prefixes + markers names -----------------------#
def loadStuck3Ls(stucks, abcs=abcs_):

    stucks = stucks.replace('\_','~',regex=True)
    new_pres = pd.DataFrame(columns=['prefix','L'])


    for i in stucks.prefix:
        dat = pd.DataFrame(columns=['pr','e'])

        L3 = i[2].lower()
        L3_i = abcs[abcs.Letter == L3].index.tolist()[0]

        dat['e']  = abcs[abcs.index >= L3_i].reset_index(drop=True).squeeze()
        dat['pr'] = dat.assign(pr = i[0:2])

        dat['prefix'] = dat.pr + dat.e
        dat['L'] = 3

        new_pres = pd.concat([new_pres,dat],ignore_index=True)

    new_pres.prefix = new_pres.prefix.str.lower()
    new_pres = new_pres.drop(['pr','e'],axis=1).sort_values(by='prefix').reset_index(drop=True)

    return new_pres,stucks

#-! Load Active Marker Names -----------------------------------#
def loadActiveMarkers(stucks_path):
    markers = pd.read_csv(stucks_path)
    markers = markers.replace('\_','~',regex=True)
    markers.prefix = markers.prefix.str.lower()
    markers.marker = markers.marker.str.lower()
    return markers

#-! Apply Active Marker Names ----------------------------------#
def applyMarkers(namebits,bit_label,markers,abcs_=abcs_):
    # ----> Prepare input name strings <----
    strs = pd.DataFrame( {
        'bits': namebits[bit_label].copy(),
        'L':    namebits.L.copy()
    })

    # ----> Prepare 3L sticky strings ('starts') <----
    marky_bits = pd.DataFrame( {
        'bits': markers.prefix.copy(),
        'L':    1000
    })
    marky_bits.index = 'p' + marky_bits.index.astype(str)

    # ----> Prepare marker names ('stops') <----
    marky_marks = pd.DataFrame({
        'bits': markers.marker.copy(),
        'L':    1000
    })
    marky_marks.index = 'm' + marky_marks.index.astype(str)

    # ----> Smoosh the things together <----
    yar = pd.concat([marky_bits,strs,marky_marks])\
            .sort_values(by=['bits','L'])

    # ----> Reindex and rename <----
    yar = yar.reset_index()
    yar = yar.rename(columns={'index':'flag'})
    yar.flag = yar.flag.astype(str)
    yar['L'] = yar.bits.str.len()

    # ----> Find the start and stop points <----
    starts = yar[yar.flag.str.contains('p')]\
                .index.tolist()
    stops  = yar[yar.flag.str.contains('m')]\
                .index.tolist()

    lims = pd.DataFrame({'start': starts, \
                         'stop':  stops})

    # ---> Make List of indicies to drop < ----
    for i in lims.index:
        yeet = np.arange( lims.start[i], lims.stop[i])

        if i == 0:
            yardrop = yeet
        else:
            yardrop = np.insert(yardrop,len(yardrop),yeet)

    yar = yar.copy().drop(yardrop,axis=0) # Drop names

    if bit_label == 'Neopet':
        yar[~yar['flag']=='p0'] # Drop marker from already-generated names

    yar = yar.drop('flag',1).reset_index(drop=True) # Drop flag column
    yar = yar.rename(columns={'bits': bit_label})

    return yar, len(yardrop)

#-! Importing Denam's Suffixes ----------------------------------------------##
def LoadDenamSuffixes():
    suffix = pd.read_csv('./data/word_segments/from-denam/3L.csv',names=['suffix'])
    suffix['L'] = 3

    suf = ['abc','def','ghi','jkl','mno','pqr','stu','vwxyz']
    for i in suf:
        dat = pd.read_csv('./word_segments/4L_'+i+'.csv',names=['suffix'])
        dat['L'] = dat.suffix.str.len()

        suffix = suffix.append(dat, ignore_index=True)

    return suffix


######################################################### Loading Name Bits ####

def loadPrefixes(f_sticky, f_prefix):
    # ---> Load Prefixes
    pres_ = pd.read_csv(f_prefix)
    pres_ = pres_.replace('\_','~', regex=True)
    marks = loadActiveMarkers(f_sticky)

    pres = pres_.copy()[~pres_.prefix.str.contains('~')].reset_index(drop=True)
    print('Prefixes Loaded: '+ str(len(pres_)))
    return pres, pres_, marks

def loadSuffixes(f_suffix):
    # ---> Load suffixes
    sufs = pd.read_csv(f_suffix)
    print('Suffixes Loaded: '+ str(len(sufs)))
    return sufs

# ---> Load default prefix/suffix set
pres, pres_, marks = loadPrefixes(f_sticky,f_prefix)
sufs = loadSuffixes(f_suffix)
################################################################################
pres_max = pres.L.max()
sufs_max = sufs.L.max()
v_s = abcs[abcs.Letter.isin(['a','e','i','o','u','y'])]
c_s = abcs[~abcs.Letter.isin(['a','e','i','o','u','y'])]

############################################################### nameBuilder ####
class nameBuilder:
    # A thing that lets you "build" a name by defining the 'bits' the name is made out of
    # 'prefix' bit will sample from prefix data
    # 'suffix' bit will sample from suffix data
    # any other input string will be used for all names
    #     (e.g., 'ay' is first 'bit' --> all names will start with 'Ay'

    # ----> Set up
    def __init__(self,N=300):

        self.constructor = pd.DataFrame(columns=['bit','L','letters'])

        # Set up dataframe variables
        self.N_names = N
        self.segments = False
        self.names = False   #created in once .construct() is called

        self.stats = {'time':'','format':'','name_data':''}



    # ----> adds prefix 'bit' to constructor
    # def add_prefix(self, L=(3, pres_max), lettrs = ('a','z')):
    #
    #     if type(L) == int:
    #         L = ( L, L ) #set lmin and Lmax
    #     if type(lettrs) == str:
    #         lettrs = (lettrs,lettrs)
    #
    #     if L[0] < 3:
    #         error('Prefixes must be at least 3 letters long!')
    #         return
    #
    #     self.constructor = self.constructor.append({
    #         'bit':      'prefix',
    #         'L':        ( L[0], L[1] ),
    #         'letters':  (lettrs[0],lettrs[1])
    #         },ignore_index=True)
    #
    #
    # # ----> adds suffix 'bit' to constructor
    # def add_suffix(self, L=(1,sufs_max),lettrs = ('a','z')):
    #
    #     if type(L) == int:
    #         L = (L, L)
    #     elif type(L) != tuple:
    #         return ('L must be int or tuple')
    #
    #     if type(lettrs) == str:
    #         lettrs = (lettrs,lettrs)
    #     elif type(lettrs) != tuple:
    #         return('L must be string or tuple)')
    #
    #
    #     self.constructor = self.constructor.append({
    #         'bit':      'suffix',
    #         'L':        ( L[0], L[1] ),
    #         'letters':  ( lettrs[0],  lettrs[1] )
    #         }, ignore_index=True)
    #     return

    # ----> adds user-defined string 'bit'
    def add_bit(self,bit,L=False,ltrs = False,
                pres_max = pres_max, sufs_max = sufs_max):
        #'prefix','suffix','c_','v_'
        if L == False:
            if bit =='prefix':
                L_ = (3,pres_max)
            elif bit =='suffix':
                L_ = (1,sufs_max)
            elif bit in ['c_','v_','l_']:
                L_ = 1
            else:
                L_ = len(bit)
        else:
            L_ = L

        if ltrs == False:
            if bit in ['prefix','suffix','c_','v_','l_']:
                ltrs_ = ('a','z')
            else:
                ltrs_ = ltrs

        self.constructor = self.constructor.append( {
            'bit': bit,
            'L': L_,
            'letters': ltrs_
            }, ignore_index=True)



    def edit_bit(self,idx,bit=False,L=False,ltrs=False):
        copy = self.constructor.loc[idx]
        if bit != False:
            copy.bit = bit

        if L != False:
            copy.L = L

        if ltrs != False:
            copy.letters = ltrs

        self.constructor.loc[idx] = copy

        print('Bit updated!')
        print('Constructor matrix is now:')
        print(self.constructor)


    def del_bit(self,idx):
        self.constructor = self.constructor.drop(index=idx)

        print('Bit deleted!')
        print('Constructor matrix is now:')
        print(self.constructor)

    def swap_bits(self,idx1,idx2):
        copy = self.constructor.copy()
        self.constructor.loc[idx2] = copy.loc[idx1]
        self.constructor.loc[idx1] = copy.loc[idx2]


    # ----> Constructs name from constructor matrix
    def tileSet(self, N=300, pres=pres, sufs=sufs, abcs=abcs_,
                vs = v_s, cs = c_s):
        if type(N) == int:
            self.N_names = N

        self.segments = pd.DataFrame(index=range(0,self.N_names))

        # ---> iterate through name 'bits'
        name_format = '|'
        for i in self.constructor.index:

            bit   = self.constructor.at[i,'bit']


            seggi = bit + '_' + str(i)
            name_format += bit + '|'


            # ---> Sample from chosen data
            if bit in ['prefix','suffix','c_','v_','l_']:
                if bit in ['c_','v_','l_']:
                    rep=True
                else:
                    Lmin  = self.constructor.at[i,'L'][0]
                    Lmax  = self.constructor.at[i,'L'][1]
                    rep = False

                let = [ self.constructor.at[i,'letters'][0].lower(),
                        self.constructor.at[i,'letters'][1].lower() ]

                #df[~df.col.str.get(0).isin(['t', 'c'])]
                az  = abcs_[abcs_.Letter.isin(let)].index.tolist()
                bcs = abcs_.Letter[az[0]:az[1]+1].tolist()

                # ---> Choose data to sample
                if bit == 'prefix':
                    samply = pres[pres.L <= Lmax]
                    samply = samply.rename(columns={'prefix': 'bit'})

                elif bit == 'suffix':
                    samply = sufs[sufs.L <= Lmax]
                    samply = samply.rename(columns={'suffix': 'bit'})

                elif bit == 'c_':
                    samply = cs.rename(columns={'Letter':'bit'})
                elif bit == 'v_':
                    samply = vs.rename(columns={'Letter':'bit'})
                elif bit == 'l_':
                    samply = abcs.rename(columns={'Letter':'bit'})

                else:
                    samply = []



                samply = samply[samply.bit.str.get(0).isin(bcs)]

                # ---> reduce # of generated names if sampling data is too small
                if (len(samply) < self.N_names) and rep == False:

                    self.segments = self.segments.drop(\
                                        index=range(len(samply),self.N_names))
                    self.N_names = len(samply)



                self.segments[seggi] = samply.bit.sample(n = self.N_names,
                                                         replace=rep).tolist()

            # ---> or copy bit for entire column

            else:
                self.segments[seggi] = bit


        self.stats['format'] = name_format.strip() # updates word stats

        # ---> turn name segments into names
        self.names = pd.DataFrame(index = self.segments.index,
                                  columns=['L','Neopet'])
        self.names.Neopet = ''

        for i in self.segments.columns:
            self.names.Neopet +=  self.segments[i]


        # ---> Get name lengths, sort, and clean up
        self.names.L = self.names.Neopet.str.len()
        self.names = self.names.drop_duplicates()\
                         .sort_values(by=['L','Neopet'])\
                         .reset_index(drop=True)

        # ---> Capitalize the names
        self.names.Neopet = self.names.Neopet.str.capitalize()

        # ---> Apply webpage function
        self.update_stats()

        return self.names


    # ---> updates name statistics
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

        print('Constructor\n'+'------------------')
        print(self.constructor)

        print('------------------')
        print('\n' + 'Name Lengths' +
              '\n' + '--------------')
        print(self.stats['name_data'])
        print('--------------')
        print('Last Update @ ' + self.stats['time'])

    def to_webpage(self,link_to='petpage'):
        htmile.make_page(self.names,link_to)
        self.update_stats()

print('Done loading the nameBuilder!')

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
