import pandas as pd
import string.ascii_lowercase as alphabet
import pkg_resources
from .defaults import defaults

def load_segments(path=defaults['segment_path']):
    """
    Returns a dataframe containing default name segments used to build Neopet names.

    Args:
        path:   string containing filepath of name segment data file
                If path is not specificied, uses default data.

    Returns:
        Dataframe with the following columns:
        bit         str     string containing name segment
        L           int     length of name segment
        prefix      bool    True if segment is a "sticky" string

    """

    print('Loading name segments...')
    if path == '':
        # This is a stream-like object. If you want the actual info, call
        # stream.read()
        stream = pkg_resources.resource_stream(__name__, 'data/word-segments.csv')
    else:
        stream == path
    return pd.read_csv(stream, encoding='latin-1')

def load_stuck_strings(path=defaults['stuck_path']):
    """
    Returns a dataframe containing default name segments used to build Neopet names.

    Args:
        path:   string containing filepath of name segment data file
                If path is not specificied, uses default data.

    Returns:
        DataFrame with the following columns:
        prefix      str     A 3-letter "stuck" prefix
        marker      str     most recently 'unstuck' pet name with prefix
    """

    if path == '':
        # This is a stream-like object. If you want the actual info, call
        # stream.read()

        stream = pkg_resources.resource_stream(__name__, 'data/stuck-strings.csv')
    else:
        stream = path
    return pd.read_csv(stream, encoding='latin-1')

#--! Label Segments As Prefixes ------------------------------------- #
def update_pres(bit_df, stuck_csv=defaults['stuck_path'], abcs=alphabet):
    """
    Updates which prefixes are "sticky" in the name segment DataFrame

    Args:
        bit_df:     DataFrame containing name segments
                    -> Loaded using load_segments()
        stucks:     DataFrame containing "sticky" prefixes & markers
                    -> Loaded using load_stuck_strings()

    Returns:
        DataFrame with the following columns:
        bit         str     string containing name segment
        L           int     length of name segment
        prefix      bool    True if segment is a "sticky" string
    """

    inputQ = input('Would you like to update stuck prefixes? y/n\n')

    if inputQ == 'y':
        print('Updating stuck prefixes ...')

        stucks = load_stuck_strings()
        stucks = stucks.replace('\_','~',regex=True)
        stucks = stucks[~stucks.prefix.str.startswith('~')]\
                 .reset_index(drop=True)
        markers = stucks.marker.str.lower()

        bit_df['prefix'] = False
        N_tagged = ''
        for n,i in enumerate(markers):
            # Prints progress to command line
            N_tagged += markers[n][0:3].upper()
            if n>0 :
                if markers[n][0] != markers[n-1][0]:
                    print('Stuck ' + markers[n-1][0].upper() +
                          ' prefixes:\n\t' +
                          N_tagged[:-5].replace('~','\_') )
                    N_tagged = N_tagged[-3:]
                elif n == len(markers)-1:
                    print('Stuck ' + markers[n-1][0].upper() +
                          ' prefixes:\n\t' + N_tagged.replace('~','\_'))
            N_tagged += ', '

            # selects subset of bit_df that matches the 1st two letters
            sliced = bit_df[bit_df.bit.str.startswith(i[0:2])].copy()
            # Get regex filter string
            F = get_regex(i)

            # Tag prefixes that match regex as 'True'
            sliced.loc[sliced.bit.str.fullmatch(F),'prefix'] = True

            bit_df.update(sliced)
        print('Active prefixes updated!')
    else:
        print('Prefixes not updated.')

    return bit_df

#--! Regex Generator for Prefix Filtering --------------------------- #
def get_regex(marker, abcs=alphabet):
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


#-- Not currently in use but could be useful later ------------------ #
# #--! Import New Segments -------------------------------------------- #
# def new_segments(filepath,old_df=''):
#     # Imports a csv file containing a list of word/name new_segments
#     # Integrates segments into existing segment data
#
#     segments = pd.read_csv(filepath)
#     print('New word segments loaded.')
#     clean_seg = segment_cleaner(segments)
#     print('New word segments cleaned + determined length + cvc format')
#     labeled = label_pres(clean_seg)
#     print('New prefixes labeled.')
#
#     input1 = input('Would you like to merge new segments with existing segments? y/n\n')
#     if input1 == 'y':
#         output = merge_segments(labeled,old_df)
#         print('Merge accepted. Returning merged segment dataframe.')
#     elif input1 =='n':
#         print('Merge declined. Returning new segments only.')
#         output = labeled
#     else:
#         print('Invalid input. Defaulting to return new segments only.')
#     return output
#
# #--! Merge new segments into old segments --------------------------- #
# def merge_segments(new,old):
#     if old == '':
#         error('No existing word segment data found.')
#     else:
#         merged = pd.concat([new,old],ignore_index=True).sort_values(by='bit')
#         merged = merged.drop_duplicates().reset_index(drop=True)
#
#         input = ('Word segment data merged. Would you like to save? y/n')
#         if input == 'y':
#             fname = 'WS_' + str(dt.date.today) + '.csv'
#             merged.to_csv('./data/word-segments/' + fname,index=False)
#             merged.to_csv('./data/word-segments.csv',index=False)
#
#     return merged
#
# #--! Word Segment Cleaner ------------------------------------------- #
# def segment_cleaner(df):
#     # Takes in a series of word/name segments
#     # Returns dataframe with segments + length + cvc format
#
#     df = df.drop_duplicates().sort_values() # Drop duplicates
#     df = df[~df.str.contains(r'[_0-9]')].reset_index(drop=True) # Remove non-letters
#
#     Ls = df.str.len() # get length
#
#     # Construct dataframe
#     final = pd.DataFrame({})
#     final.insert(loc=0,column='bit',value=df)
#     final.insert(loc=1,column='L',value=Ls)
#     return final
#
# #--! Export Prefixes [ for Denam ] ---------------------------------- #
# def export_pres(bit_df,abcs=string.ascii_lowercase):
#     csv_list = ['abc','def','ghi','jkl','mno','pqr','stu']
#     pres = bit_df[bit_df.prefix == True]
#
#     for letters in csv_list:
#         preslice = pres.bit[pres.bit.str.contains(
#                         r'^['+letters[0]+'-'+letters[2]+']')]
#         preslice.to_csv('./data/prefixes/'+letters+'.csv',index=False)
#
#     return 'CSV files exported.'
