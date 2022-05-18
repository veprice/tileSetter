import pandas as pd
import csv


'''HTML generating functions'''
#--! Generate URLs related to the pet ----------------------------- #
def get_pet_links(names,img_no='1'):

    # image URL
    names['img'] = 'http://pets.neopets.com/cpn/' +\
                    names.Neopet + '/1/'+img_no+'.png'

    # URLs to important places
    names['petpage'] = 'http://neopets.com/~' + names.Neopet
    names['pound'] = 'http://neopets.com/pound/adopt.phtml?search=' + names.Neopet
    names['lookup'] = 'http://neopets.com/petlookup.phtml?pet=' + names.Neopet

    return names

#--! Generate Neopet tiles ---------------------------------------- #
def get_pet_tiles(names,link_to='petpage',tiyg=False):

    # Create tiles
    ps = div.wrap(p.wrap(names.Neopet),class_="pet",
                    style = "background: url('"+ names.img + "');")

    # Make tiles circles if updating Tiyg's petpage
    a_style = ''
    if tiyg == True:
        a_style = "border-radius:80px;"

    # Add pet tile HTML column to 'names'
    names['pet_div'] = a.wrap(  ps,href=names[link_to],
                                style=a_style )
    return names

#--! Sort pets into <divs> by name length ------------------------- #
def make_L_divs(names):
        divdict = {}
        for i in names.L.unique():
            nameslice = names[names.L == i]

            i_name = str(i) + ' Letters'
            iL_div =  [ h2.wrap(i_name,wrap_by='block') ]
            iL_div += nameslice.pet_div.values.tolist()
            iL_div = pd.Series(iL_div)
            Ldiv = div.wrap(iL_div,wrap_by='block',class_='petgroup')

            divdict[i_name] = Ldiv.explode()
        return divdict

#--! Unpack webpage from dictionary to Series --------------------- #
def unpack_HTML(unpack_me):
        # unpacks HTML from dictionary into pandas series
        page = []
        for keys,values in unpack_me.items():
            page += values.tolist()
            page += ['\n']

        page = pd.Series(page)
        return page

'''TileSetters'''
#--! General Tilesetting Function ---------------------------------- #
def tileSet(names,linkto='petpage',local_page=True):
    css = '<link rel="stylesheet" type="text/css" href="style.css">'
    css = pd.Series(css)
    sort_pets_by = {'by':['L','Neopet']}

    names0 = names.copy()
    names0['Neopet'] = names0.Neopet.str.replace('~','_')
    names1 = get_pet_links(names0, img_no='1') # get pet links
    names2 = get_pet_tiles(names1, link_to=linkto) # get pet tile HTML

    page = {'css': css}

    divs = make_L_divs(names2) # sort pet tiles into divs based on name length

    page.update(divs)

    html = unpack_HTML(page)

    if local_page==True:
        html.to_csv('./HTML/tileSet.html', sep=',', header=False,
                    index=False, quoting=csv.QUOTE_NONE,
                    escapechar='\n')
        output = html
        print('HTML Updated!')
    else:
        yey = html
        yey = yey.str.replace('\t','')
        yey = yey.str.replace('\n','')
        yey_html = ''
        for i in yey[1:]:
            yey_html += i

        output = yey_html

    return output

#-! HTML tag template ----------------------------- #
class Tagger:
    def __init__(self, tag, single=False,**attrs):
        self.tag = tag
        self.ats = self.check_for_class(attrs)
        self.single = single

        if single==True:
            self.openr = ' />'
            self.tagclosed = ''
        else:
            self.openr = '>'
            self.tagclosed = '</' + tag + '>'

    def check_for_class(self,attributes):
        if 'class_' in attributes.keys():
            attributes['class'] = attributes.pop('class_')
        return attributes

    def wrap(self, to_wrap, wrap_by='lines', **attrs):
        attrs = self.check_for_class(attrs)
        #print(attrs)
        tagclosed = self.tagclosed

        if wrap_by == 'lines':
            wrapper = pd.DataFrame()
            tagopen = self.open_tag(attrs.copy())
            #print(tagopen)


            if type(tagopen) == pd.Series:
                wrapper['open'] = tagopen
            elif type(tagopen) == str:
                open = pd.Series(tagopen,index = range(0,len(to_wrap)))
                wrapper['open'] = open

            wrapper['content'] = '\t' + to_wrap
            wrapper['closed'] = tagclosed
            #print(wrapper.stack().explode().swaplevel(0,1))
            wrapper['tag'] = wrapper.open.astype(str) + \
                             wrapper.content.astype(str) + \
                             wrapper.closed.astype(str)
            wrapped = wrapper['tag']#wrapper['tag']


        elif wrap_by == 'block':

            content = to_wrap
            if type(to_wrap) == list:
                content = pd.Series(to_wrap)
            if type(content) == pd.Series:
                content = '\t'+content
                content = content.values.tolist()
            elif type(content) == str:
                content = [ '\t'+content ]
            else:
                print('Unable to block wrap.')
                return

            wrapper = [ self.open_tag(attrs.copy()) ] + content + [ tagclosed ]
            wrapped = pd.Series(wrapper)

        return wrapped

    def open_tag(self,attrs):

        ats = self.ats.copy()
        ats.update(attrs.copy())
        tag_open = '<' + self.tag
        for attribute,value in ats.items():
            if type(value) == str:
                tag_open += ' {}="{}"'.format(attribute,value)
            elif type(value) == pd.Series:

                tag_open += ' ' + attribute + '="' + value + '"'
        tag_open += self.openr

        return tag_open

    def add_attributes(self,**attrs):
        check = self.check_for_class(attrs)
        self.ats.update(check)

    def copy(self):
        new_boi = self
        return new_boi

a = Tagger('a', href='')
img = Tagger('img', single=True, src='' )
div = Tagger('div')
p = Tagger('p')
h2 = Tagger('h2')
h1 = Tagger('h1')
br = Tagger('br',single=True)


'''Deprecated Code; here for reference'''
# def get_links(names, server='', which_links = ['petpage'],img_no='1'):
#
#     names['img'] = 'http://pets.neopets.com/cpn/' +\
#                     names.Neopet + '/1/'+img_no+'.png'
#
#     if 'petpage' in which_links:
#         names['petpage'] = server + '/~' + names.Neopet
#     elif 'pound' in which_links:
#         names['pound'] = server + '/pound/adopt.phtml?search=' + names.Neopet
#     elif 'lookup' in which_links:
#         names['lookup'] = server + 'petlookup.phtml?pet=' + names.Neopet
#
#     return names
#
#
# #-! Page Building Class ------------------------------------------#
# class tileSetPage:
#     def __init__(self,page_type=0):
#         # self.names = names.sort_values(by=['L','Neopet'], key=lambda x: x.str.lower())
#         query = 'What type of page do you want to tileset?\n' +\
#                 '1: Pound Search Page\n' +\
#                 '2: Stuck Pet Database\n' +\
#                 '3: Untaken Name Database\n' +\
#                 '4: Petpage\n'
#
#         page_type = int(input(query))
#
#
#         if page_type == 1:
#             self.page_type = '1: Pound Search Page\n'
#
#             self.builder = nb.nameBuilder()
#             self.builder.add_bit('prefix',L=(3,5))
#             self.builder.add_bit('v_')
#             self.builder.add_bit('l_')
#             print('Name Builder Initizalized with constructor:')
#             print(self.builder.constructor)
#
#             server = 'http://neopets.com'
#             which_links = ['petpage']
#             img_no = '1'
#
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             save_to = '../HTML/tileSet.html'
#             sort_pets_by = {'by':['L','Neopet']}
#             div_type = 'name_length'
#
#         elif page_type == 2:
#             self.page_type = '2: Stuck Pet Database\n'
#             self.builder = pdb.dbChecker(db=pdb.pets)
#             server = 'http://neopets.com'
#             which_links = ['pound']
#             img_no = "1"
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             save_to = '../HTML/petCheck.html'
#             sort_pets_by = {'by': 'Neopet', 'key':lambda x: x.str.lower()}
#             div_type = 'abcs'
#
#         elif page_type == 3:
#             self.page_type = '3: Untaken Name Database\n'
#             self.builder = pdb.dbChecker(db=pdb.names)
#             server = 'http://neopets.com/'
#             which_links = ['petpage']
#             img_no = '1'
#             save_to = '../HTML/nameCheck.html'
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             sort_pets_by = {'by':['L','Neopet']}
#             div_type = 'abcs'
#
#         elif page_type == 4:
#             self.page_type = '4: Petpage\n'
#             get_rands = nb.nameBuilder()
#             get_rands.add_bit('suffix',L=(3,4))
#             get_rands.add_bit('v_')
#             get_rands.add_bit('l_')
#
#             get_cura = pdb.dbChecker(db=pdb.names)
#             get_stuck = pdb.dbChecker(db=pdb.pets)
#
#             self.buildys = {'curated' : get_cura,
#                             'random'   : get_rands,
#                             'stuck'   : get_stuck }
#
#             self.builder = ''
#
#             self.ps = {'curated':   'A selection of quality names curated by Cady.',
#                        'stuck':     'These are some VWN pets that are currently <b>stuck in the pound</b>! Perfect for lab rats, custom trade fodder, or a new friend with whom to explore Neopia.',
#                        'random':     'A selection of randomly-generated names that have not been reviewed for quality. There\'s definitely junk here, but there are also some gems!'}
#
#             server = ''
#             which_links = ['petpage','pound']
#             img_no = '3'
#             save_to = '../HTML/names_petpage/auto_gen.html'
#             css = pd.read_csv(  '../HTML/names_petpage/css.css',
#                                 sep='\n',squeeze=True, header=None   )
#             css = css.squeeze()
#             sort_pets_by = {'by':'Neopet', 'key':lambda x: x.str.lower()}
#             div_type = 'abcs'
#
#         else:
#             print('Page type not recognized. Please try again.')
#             return
#
#         self.save_to = save_to
#         self.link_data = {  'server' :      server,
#                             'which_links':   which_links,
#                             'img_no':       img_no }
#         self.sort_vals = sort_pets_by
#         self.div_type = div_type
#
#         self.css = { 'css' : css }
#         self.page = self.css
#
#         print('Chosen page type: ' + self.page_type)
#         print('Saving page to: ' +self.save_to)
#
#         if page_type <=3:
#             self.refresh()
#         elif page_type == 4:
#             self.PetPage()
#
#
#     def PetPage(self):
#         self.page = self.css.copy()
#
#         # ---> Make header & nav links
#         title = h1.wrap('Names By Cady',wrap_by='block', style='position:absolute;')
#
#         self.page['head'] = div.wrap(title,wrap_by='block',
#                             id='head',style='position:fixed;')
#         nav_links = pd.Series(['curated','random','stuck'])
#         nav = a.wrap( nav_links.str.capitalize(), href='#' + nav_links)
#
#         nav = nav + ' • '
#
#         self.page['nav'] = div.wrap(nav,wrap_by='block',
#                                     id='nav',style='position:fixed;')
#
#         container = {}
#
#         for section,builder in self.buildys.items():
#             div_str = section
#             #### Curated Names Block
#             self.builder = builder
#             if section == 'curated':
#                 self.link_data['which_links'][0] = 'petpage'
#                 div_names = self.refresh(to_local=False,star=False,N=200,L = 5) # get names
#             elif section == 'stuck':
#                 self.link_data['which_links'][0] = 'pound'
#                 div_names = self.refresh(to_local=False, N=120,
#                                          star=False,status='pound',nameQ='VWN')
#             else:
#                 self.link_data['which_links'][0] = 'petpage'
#                 div_names = self.refresh(to_local=False,N=200)
#
#             # put names into alphebetically ordered blocks
#             div_dict = {}
#             div_dict = self.makeAbcDivs(div_names,bumper=True,id_str=div_str)
#
#             # make abc subsection nav
#             abc_hrefs = pd.Series(div_dict.keys()).str.upper()
#             abc_nav = a.wrap(abc_hrefs, wrap_by='lines',
#                                 href='#'+div_str+abc_hrefs.str[0])
#             abc_nav += pd.Series(['•','•','•',''])
#
#             abc_nav = p.wrap(abc_nav,wrap_by='block',class_='abcnav')
#
#             # blurb right after navigation
#             p1 = p.wrap(self.ps[section],wrap_by='block')
#             p2 = p.wrap(' All names and pets are rotated regularly, so check back if you don\'t see any here that you like!', wrap_by='block')
#
#             # Put it all into the sectino header
#             sec_header = pd.concat([abc_nav,p1,p2]).reset_index(drop=True)
#             sec_header = div.wrap(sec_header,wrap_by='block',class_='bumper')
#
#             # combine section header with name blocks
#             div_dict = self.unpack_HTML(div_dict)
#             box = pd.concat([sec_header,div_dict])
#
#
#
#             # wrap it all up in a 'text' div, append to container block
#             container[section] = div.wrap(box,wrap_by='block',
#                                          class_='text', id=section)
#             print(section+' HTML done.')
#         # Unpack container into a Series and div-wrap it
#         wrapped_container = div.wrap(   self.unpack_HTML(container),
#                                         wrap_by='block', id='container',
#                                         style='position:fixed;'         )
#
#         self.page['container'] = wrapped_container
#
#
#         # Unpack entire page
#         page = self.unpack_HTML(self.page)
#
#         page.to_csv(self.save_to,
#                         sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
#                         escapechar='\n',na_rep=" ")
#
#
#         print('Petpage saved to:\n'+self.save_to)
#
#
#     def localPage(self,names):
#
#         self.page = self.css.copy()
#
#         if self.div_type == 'abcs':
#             divs = self.makeAbcDivs(names)
#         elif self.div_type == 'name_length':
#             divs = self.makeLDivs(names)
#         else:
#             self.page['pets'] = names.pet_div.squeeze()
#
#         self.page.update(divs)
#
#
#
#         page = self.unpack_HTML(self.page)
#
#         page.to_csv(self.save_to,
#                         sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
#                         escapechar='\n')
#
#         print('Page Updated!')
#         return page
#
#
#
#     def makeAbcDivs(self,names,bumper=False,id_str=''):
#         divdict = {}
#         let_range = [['a','d'],['f','k'],['l','p'],['q','t'],['u','z']]
#         for n,i in enumerate(let_range):
#
#             i_name = i[0] + '-' + i[1]
#             abc_range = nb.abcs[nb.abcs.Letter.isin(i)].index.tolist()
#             letter_list = nb.abcs.Letter[abc_range[0]:abc_range[1]+1].values.tolist()
#             letter_list += nb.abcs.Letter[abc_range[0]:abc_range[1]+1]\
#                                   .str.upper().values.tolist()
#             nameslice = names[names.Neopet.str.get(0).isin(letter_list)]
#
#             iABC_div =  [h2.wrap(i_name.upper(), wrap_by='block')]
#             if bumper==True:
#                 iABC_div = div.wrap(iABC_div,wrap_by='block',
#                                     class_='bumper',
#                                     id=id_str+i_name[0].upper())
#                 iABC_div = iABC_div.tolist()
#             iABC_div += nameslice.pet_div.values.tolist()
#             iABC_div = pd.Series(iABC_div)
#
#             ABCdiv = div.wrap(iABC_div,wrap_by='block',class_='petgroup')
#             if len(nameslice) > 0 :
#                 divdict[i_name] = ABCdiv.explode()
#         return divdict
#
#     def makeLDivs(self,names):
#         divdict = {}
#         for i in names.L.unique():
#             nameslice = names[names.L == i]
#
#             i_name = str(i) + ' Letters'
#             iL_div =  [ h2.wrap(i_name,wrap_by='block') ]
#             iL_div += nameslice.pet_div.values.tolist()
#             iL_div = pd.Series(iL_div)
#             Ldiv = div.wrap(iL_div,wrap_by='block',class_='petgroup')
#
#             divdict[i_name] = Ldiv.explode()
#         return divdict
#
#     def unpack_HTML(self,unpack_me):
#         # unpacks HTML from dictionary into pandas series
#         page = []
#         for keys,values in unpack_me.items():
#             page += values.tolist()
#             page += ['\n']
#
#         page = pd.Series(page)
#         # page.to_csv(self.save_to,
#         #                 sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
#         #                 escapechar='\n')
#         return page
# #
#     def get_petDivs(self, names, link_to='petpage'):
#         #a_txt = names.Neopet + '<br>' + img.wrap('',src=names.img)
#         imgs = img.wrap('',src=names.img)
#         brs = br.wrap(imgs)
#         a_s = a.wrap(to_wrap=names.Neopet + brs, href=names[link_to])
#         names['pet_div'] = div.wrap(a_s,class_='pet')
#         #print(names['pet_div'][0])
#         return names
#
#     def get_petAs(self,names,link_to='petpage'):
#
#         ps = div.wrap(p.wrap(names.Neopet),class_="pet",
#                         style = "background: url('"+ names.img + "');")
#
#         if self.page_type == '4: Petpage\n':
#             a_style = "border-radius:80px;"
#         else:
#             a_style = "border-radius:0px"
#
#         names['pet_div'] = a.wrap(  ps,href=names[link_to],
#                                     style=a_style)
#         return names
#
#     def refresh(self,to_local=True,**kwargs):
#         names = self.builder.tileSet(**kwargs)
#
#         names['Neopet'] = names.Neopet.str.replace('~','_')
#
#         names = names.sort_values(**self.sort_vals)
#         names = get_links(names, **self.link_data)
#
#         names = self.get_petAs(names, link_to=self.link_data['which_links'][0])
#
#         if to_local == True:
#             self.localPage(names)
#         else:
#             return names





#
# import pandas as pd
# import csv
#
# from dataLoader import f_webpage, f_css
# import nameBuilder as nb
# import petDB as pdb
#
# pagefile = f_webpage
# #print(pagefile)
#
# def get_links(names, server='', which_links = ['petpage']):
#
#     names['img'] = 'http://pets.neopets.com/cpn/' + names.Neopet + '/1/1.png'
#
#     if 'petpage' in which_links:
#         names['petpage'] = server + '/~' + names.Neopet
#     elif 'pound' in which_links:
#         names['pound'] = server + '/pound/adopt.phtml?search=' + names.Neopet
#     elif 'lookup' in which_links:
#         names['lookup'] = server + 'petlookup.phtml?pet=' + names.Neopet
#
#     return names
#
#
# #-! Page Building Class ------------------------------------------#
# class tileSetPage:
#     def __init__(self,page_type):
#         # self.names = names.sort_values(by=['L','Neopet'], key=lambda x: x.str.lower())
#         self.page_type = page_type
#
#         if self.page_type == 'name_search':
#
#             self.builder = nb.nameBuilder()
#             self.builder.constructor = pd.DataFrame(\
#                                           {'bit': ['prefix','v_','c_','v_'],
#                                             'L'  : [(3,5),1,1,1],
#                                             'letters':[('a','z'),('a','z'),
#                                                        ('a','z'),('a','z')]  } )
#
#             print('Name Builder Initizalized with constructor:')
#             print(self.builder.constructor)
#
#             server = 'http://neopets.com'
#             which_links = ['petpage']
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             save_to = '../HTML/tileSet.html'
#             sort_pets_by = {'by':['L','Neopet']}
#             div_type = 'name_length'
#
#         elif self.page_type == 'pet_check':
#             self.builder = pdb.dbChecker(db=pdb.pets)
#             server = 'http://neopets.com'
#             which_links = ['pound']
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             save_to = '../HTML/petCheck.html'
#             sort_pets_by = {'by': 'Neopet', 'key':lambda x: x.str.lower()}
#             div_type = 'abcs'
#
#         elif self.page_type == 'name_check':
#             self.builder = pdb.dbChecker(db=pdb.names)
#             server = 'http://neopets.com/'
#             which_links = ['petpage']
#             save_to = '../HTML/nameCheck.html'
#             css = '<link rel="stylesheet" type="text/css" href="style.css">'
#             css = pd.Series(css)
#             sort_pets_by = {'by':['L','Neopet']}
#             div_type = 'abcs'
#
#         elif self.page_type == 'petpage':
#
#             self.build_rands = nb.nameBuilder()
#             self.build_rands.constructor = pd.DataFrame(\
#                                           {'bit': ['prefix','v_','c_','v_'],
#                                             'L'  : [(3,5),1,1,1],
#                                             'letters':[('a','z'),('a','z'),
#                                                        ('a','z'),('a','z')]  } )
#             server = ''
#             which_links = ['petpage','pound']
#             save_to = '../HTML/names_petpage/auto_gen.html'
#             css = pd.read_csv(  '../HTML/names_petpage/css.css',
#                                 sep='\n', header=None   )
#             sort_pets_by = {'by':'Neopet', 'key':lambda x: x.str.lower()}
#             div_type = 'abcs'
#
#
#         else:
#             print('Page type not recognized. Please try again.')
#             return
#
#         self.save_to = save_to
#         self.link_data = {  'server' :      server,
#                             'which_links':   which_links }
#         self.sort_vals = sort_pets_by
#         self.div_type = div_type
#
#         self.css = { 'css' : css }
#         self.page = self.css
#
#         print('Chosen page type: ' + self.page_type)
#
#
#
#
#
#     def localPage(self,names):
#         self.page = self.page.copy()
#         if self.div_type == 'abcs':
#             self.makeAbcDivs(names)
#         elif self.div_type == 'name_length':
#             self.makeLDivs(names)
#         else:
#             self.page['pets'] = names.pet_div.squeeze()
#
#         self.make_page()
#
#
#
#     def makeAbcDivs(self,names,):
#         let_range = [['a','f'],['g','k'],['l','p'],['q','t'],['u','z']]
#         for i in let_range:
#             i_name = i[0] + '-' + i[1]
#             abc_range = nb.abcs[nb.abcs.Letter.isin(i)].index.tolist()
#             letter_list = nb.abcs.Letter[abc_range[0]:abc_range[1]+1].values.tolist()
#             letter_list += nb.abcs.Letter[abc_range[0]:abc_range[1]+1]\
#                                   .str.upper().values.tolist()
#             nameslice = names[names.Neopet.str.get(0).isin(letter_list)]
#
#             iABC_div = [ h2.wrap(i_name.upper(), wrap_by='block') ]
#             iABC_div += nameslice.pet_div.values.tolist()
#             iABC_div = pd.Series(iABC_div)
#
#             ABCdiv = div.wrap(iABC_div,wrap_by='block',class_='petgroup')
#             if len(nameslice) > 0 :
#                 self.page[i_name] = ABCdiv.explode()
#         return
#
#     def makeLDivs(self,names):
#         for i in names.L.unique():
#             nameslice = names[names.L == i]
#
#             i_name = str(i) + ' Letters'
#             iL_div =  [ h2.wrap(i_name,wrap_by='block') ]
#             iL_div += nameslice.pet_div.values.tolist()
#             iL_div = pd.Series(iL_div)
#             Ldiv = div.wrap(iL_div,wrap_by='block',class_='petgroup')
#
#             self.page[i_name] = Ldiv.explode()
#
#         return i_name, Ldiv
#
#     def make_page(self):
#         page = []
#         for keys,values in self.page.items():
#             page += values.tolist()
#             page += ['\n']
#         page = pd.Series(page)
#         page.to_csv(self.save_to,
#                         sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
#                         escapechar='\n')
#         return page
# #
#     def get_petDivs(self, names, link_to='petpage'):
#         #a_txt = names.Neopet + '<br>' + img.wrap('',src=names.img)
#         imgs = img.wrap('',src=names.img)
#         brs = br.wrap(imgs)
#         a_s = a.wrap(to_wrap=names.Neopet + brs, href=names[link_to])
#         names['pet_div'] = div.wrap(a_s,class_='pet')
#         #print(names['pet_div'][0])
#         return names
#
#     def refresh(self,**kwargs):
#         names = self.builder.tileSet(**kwargs)
#
#         names['Neopet'] = names.Neopet.str.replace('~','_')
#
#         names = names.sort_values(**self.sort_vals)
#         names = get_links(names, **self.link_data)
#         names = self.get_petDivs(names, link_to=self.link_data['which_links'][0])
#         #print(names)
#         self.localPage(names)
#
#
# #-! HTML tag template ----------------------------- #
# class Tagger:
#     def __init__(self, tag, single=False,**attrs):
#         self.tag = tag
#         self.ats = self.check_for_class(attrs)
#         self.single = single
#
#         if single==True:
#             self.openr = ' />'
#             self.tagclosed = ''
#         else:
#             self.openr = '>'
#             self.tagclosed = '</' + tag + '>'
#
#     def check_for_class(self,attributes):
#         if 'class_' in attributes.keys():
#             attributes['class'] = attributes.pop('class_')
#         return attributes
#
#     def wrap(self, to_wrap, wrap_by='lines', **attrs):
#         attrs = self.check_for_class(attrs)
#         #print(attrs)
#         tagclosed = self.tagclosed
#
#         if wrap_by == 'lines':
#             wrapper = pd.DataFrame()
#             tagopen = self.open_tag(attrs.copy())
#             #print(tagopen)
#
#
#             if type(tagopen) == pd.Series:
#                 wrapper['open'] = tagopen
#             elif type(tagopen) == str:
#                 open = pd.Series(tagopen,index = range(0,len(to_wrap)))
#                 wrapper['open'] = open
#
#             wrapper['content'] = '\t' + to_wrap
#             wrapper['closed'] = tagclosed
#             #print(wrapper.stack().explode().swaplevel(0,1))
#             wrapper['tag'] = wrapper.open.astype(str) + \
#                              wrapper.content.astype(str) + \
#                              wrapper.closed.astype(str)
#             wrapped = wrapper['tag']#wrapper['tag']
#
#
#         elif wrap_by == 'block':
#
#             content = to_wrap
#             if type(to_wrap) == list:
#                 content = pd.Series(to_wrap)
#             if type(content) == pd.Series:
#                 content = '\t'+content
#                 content = content.values.tolist()
#             elif type(content) == str:
#                 content = [ '\t'+content ]
#             else:
#                 print('Unable to block wrap.')
#                 return
#
#             wrapper = [ self.open_tag(attrs.copy()) ] + content + [ tagclosed ]
#             wrapped = pd.Series(wrapper)
#
#         return wrapped
#
#     def open_tag(self,attrs):
#
#         ats = self.ats.copy()
#         ats.update(attrs.copy())
#         tag_open = '<' + self.tag
#         for attribute,value in ats.items():
#             if type(value) == str:
#                 tag_open += ' {}="{}"'.format(attribute,value)
#             elif type(value) == pd.Series:
#
#                 tag_open += ' ' + attribute + '="' + value + '"'
#         tag_open += self.openr
#
#         return tag_open
#
#     def add_attributes(self,**attrs):
#         check = self.check_for_class(attrs)
#         self.ats.update(check)
#
#     def copy(self):
#         new_boi = self
#         return new_boi
#
#
# a = Tagger('a', href='')
# img = Tagger('img', single=True, src='' )
# div = Tagger('div')
# p = Tagger('p')
# h2 = Tagger('h2')
# h1 = Tagger('h1')
# br = Tagger('br',single=True)
# # class tileSetPage:
# #     def __init__(self):
# #         # self.names = names.sort_values(by=['L','Neopet'], key=lambda x: x.str.lower())
# #
# #         self.link_data = {  'server' :      'http://neopets.com',
# #                             'which_links':   ['petpage']}
# #         css = '<link rel="stylesheet" type="text/css" href="style.css">'
# #         self.page = { 'css' : pd.Series(css) }
# #
# #         self.save_to = '../HTML/tileSet.html'
# #
# #         self.builder = nb.nameBuilder()
# #
# #     def buildPage(self,names):
# #         names['Neopet'] = names.Neopet.str.replace('~','_')
# #         names = names.sort_values(by=['L','Neopet'])
# #         names = get_links(names, **self.link_data)
# #         names = self.get_petDivs(names, link_to='petpage')
# #
# #
# #         for i in names.L.unique():
# #             nameLs = names[names.L == i]
# #             div_name,tiles = self.makeLDiv(nameLs,i)
# #             self.page[div_name] = tiles.explode()
# #         page = self.make_page()
# #
# #
# #     def makeLDiv(self,names,i):
# #         i_name = str(i) + ' Letters'
# #         iL_div =  [ h2.wrap(i_name,wrap_by='block') ]
# #         iL_div += names.pet_div.values.tolist()
# #         iL_div = pd.Series(iL_div)
# #
# #         Ldiv = div.wrap(iL_div,wrap_by='block',class_='letter')
# #         #print(Ldiv)
# #
# #         return i_name, Ldiv
# #
# #
# #     def make_page(self):
# #
# #         page = []
# #         for keys,values in self.page.items():
# #             page += values.tolist()
# #             page += ['\n']
# #
# #         page = pd.Series(page)
# #
# #         page.to_csv(self.save_to,
# #                         sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
# #                         escapechar='\n')
# #
# #         return page
# # #
# #     def get_petDivs(self, names, link_to='petpage'):
# #         #a_txt = names.Neopet + '<br>' + img.wrap('',src=names.img)
# #         imgs = img.wrap('',src=names.img)
# #         brs = br.wrap(imgs)
# #         a_s = a.wrap(to_wrap=names.Neopet + brs, href=names[link_to])
# #         names['pet_div'] = div.wrap(a_s,class_='pet')
# #         #print(names['pet_div'][0])
# #         return names
# #
# #     def refresh(self,N=300):
# #         names = self.builder.tileSet(N=N)
# #         self.buildPage(names)
#
#
# def make_page(names, f_css = f_css, f_webpage = pagefile ):
#
#     css_tag = '<link rel="stylesheet" type="text/css"  href="'+ f_css +'">'
#     # prep s
#     names['Neopet'] = names.Neopet.str.replace('~','_')
#     names = names.sort_values(by=['L','Neopet'],key=lambda x: x.str.lower())
#
#
#
#     # ---> generate img + link urls + pet divs
#     link_data = { 'server' : 'http://neopets.com',
#                   'which_link': 'petpage' }
#     names = get_links(names, **link_data)
#     names = get_petDivs(names)
#
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
#         # linkme = nameLs.Neopet + '<br>' + img_wrap(nameLs.img)
#         # divp = div_wrap(a_wrap(linkme,nameLs[linky]))
#
#
#         page += names.div_p.values.tolist()
#         page += ['</div>\n']
#
#     # ---> Save webpage code using Panda's .to_csv
#     webpage = pd.Series(page)
#     f_webpage = './HTML/test_page.html'
#     webpage.to_csv(f_webpage,
#                     sep=',',header=False,index=False,quoting=csv.QUOTE_NONE)
#     return
#
# # #-! Get links for names ----------------------------#
# # def get_links(names, server='', which_links = ['petpage']):
# #
# #     names['img'] = 'http://pets.neopets.com/cpn/' + names.Neopet + '/1/1.png'
# #
# #     if 'petpage' in which_links:
# #         names['petpage'] = server + '/~' + names.Neopet
# #     elif 'pound' in which_links:
# #         names['pound'] = server + '/pound/adopt.phtml?search=' + names.Neopet
# #     elif 'lookup' in which_links:
# #         names['lookup'] = server + 'petlookup.phtml?pet=' + names.Neopet
# #
# #     return names
#
#
# #-! Page Building Class ------------------------------------------#
# # class tileSetPage:
# #     def __init__(self):
# #         # self.names = names.sort_values(by=['L','Neopet'], key=lambda x: x.str.lower())
# #
# #         self.link_data = {  'server' :      'http://neopets.com',
# #                             'which_links':   ['petpage']}
# #         css = '<link rel="stylesheet" type="text/css" href="style.css">'
# #         self.page = { 'css' : pd.Series(css) }
# #
# #         self.save_to = '../HTML/tileSet.html'
# #
# #         self.builder = nb.nameBuilder()
# #
# #     def buildPage(self,names):
# #         names['Neopet'] = names.Neopet.str.replace('~','_')
# #         names = names.sort_values(by=['L','Neopet'])
# #         names = get_links(names, **self.link_data)
# #         names = get_petDivs(names, link_to='petpage')
# #
# #
# #         for i in names.L.unique():
# #             nameLs = names[names.L == i]
# #             div_name,tiles = self.makeLDiv(nameLs,i)
# #             self.page[div_name] = tiles.explode()
# #         page = self.make_page()
# #
# #
# #     def makeLDiv(self,names,i):
# #         i_name = str(i) + ' Letters'
# #         iL_div =  [ h2.wrap(i_name,wrap_by='block') ]
# #         iL_div += names.pet_div.values.tolist()
# #         iL_div = pd.Series(iL_div)
# #
# #         Ldiv = div.wrap(iL_div,wrap_by='block',class_='letter')
# #         #print(Ldiv)
# #
# #         return i_name, Ldiv
# #
# #
# #     def make_page(self):
# #
# #         page = []
# #         for keys,values in self.page.items():
# #             page += values.tolist()
# #             page += ['\n']
# #
# #         page = pd.Series(page)
# #
# #         page.to_csv(self.save_to,
# #                         sep=',',header=False,index=False,quoting=csv.QUOTE_NONE,
# #                         escapechar='\n')
# #
# #         return page
# # #
# #     def get_petDivs(self, names, link_to='petpage'):
# #         #a_txt = names.Neopet + '<br>' + img.wrap('',src=names.img)
# #         imgs = img.wrap('',src=names.img)
# #         brs = br.wrap(imgs)
# #         a_s = a.wrap(to_wrap=names.Neopet + brs, href=names[link_to])
# #         names['pet_div'] = div.wrap(a_s,class_='pet')
# #         #print(names['pet_div'][0])
# #         return names
# #
# #     def refresh(self,N=300):
# #         names = self.builder.tileSet(N=N)
# #         self.buildPage(names)
#
# #-! Get Pet Divs ------------------------------------#
# # def get_petDivs(names):
# #
# #     imgs = tag_wrap('img', tag_params = { 'src':  names.img } )
# #
# #     a_data = {'tag': 'a',
# #               'content': names.Neopet + '<br>\n' + imgs,
# #               'tag_params': { 'href': names.link }}
# #
# #     as   = tag_wrap(**a_data)
# #
# #     div_data = {'tag': 'div',
# #                 'content': as,
# #                 'tag_params': {'class':'pet'}   }
# #
# #     names['pet_div'] = tag_wrap( **tag_data )
# #
# #     return names
#
# #-! HTML wrapper functions --------------------------#
# def tag_wrap(tag='div', content='', tag_params = {}):
#     tagopen = '<' + tag
#     for i in tag_params:
#         tagopen += ' {}="{}"'.format(name, qty)
#     if tag == 'img':
#         content = ''
#         tagclosed = ' />'
#     else:
#         tagopen += '> \n\t'
#         tagclosed = '</' + tag + '>'
#     return tagopen + content + tagclosed
#
# #-! HTML tag template ----------------------------- #
# # class Tagger:
# #     def __init__(self, tag, single=False,**attrs):
# #         self.tag = tag
# #         self.ats = self.check_for_class(attrs)
# #         self.single = single
# #
# #         if single==True:
# #             self.openr = ' />'
# #             self.tagclosed = ''
# #         else:
# #             self.openr = '>'
# #             self.tagclosed = '</' + tag + '>'
# #
# #     def check_for_class(self,attributes):
# #         if 'class_' in attributes.keys():
# #             attributes['class'] = attributes.pop('class_')
# #         return attributes
# #
# #     def wrap(self, to_wrap, wrap_by='lines', **attrs):
# #         attrs = self.check_for_class(attrs)
# #         #print(attrs)
# #         tagclosed = self.tagclosed
# #
# #         if wrap_by == 'lines':
# #             wrapper = pd.DataFrame()
# #             tagopen = self.open_tag(attrs.copy())
# #             #print(tagopen)
# #
# #
# #             if type(tagopen) == pd.Series:
# #                 wrapper['open'] = tagopen
# #             elif type(tagopen) == str:
# #                 open = pd.Series(tagopen,index = range(0,len(to_wrap)))
# #                 wrapper['open'] = open
# #
# #             wrapper['content'] = '\t' + to_wrap
# #             wrapper['closed'] = tagclosed
# #             print(wrapper.stack().explode().swaplevel(0,1))
# #             wrapper['tag'] = wrapper.open.astype(str) + \
# #                              wrapper.content.astype(str) + \
# #                              wrapper.closed.astype(str)
# #             wrapped = wrapper['tag']#wrapper['tag']
# #
# #
# #         elif wrap_by == 'block':
# #
# #             content = to_wrap
# #             if type(to_wrap) == pd.Series:
# #                 content = '\t'+content
# #                 content = content.values.tolist()
# #             elif type(to_wrap) == str:
# #                 content = [ '\t'+content ]
# #             else:
# #                 print('Unable to block wrap.')
# #                 return
# #
# #             wrapper = [ self.open_tag(attrs.copy()) ] + content + [ tagclosed ]
# #             wrapped = pd.Series(wrapper)
# #
# #         return wrapped
# #
# #     def open_tag(self,attrs):
# #
# #         ats = self.ats.copy()
# #         ats.update(attrs.copy())
# #         tag_open = '<' + self.tag
# #         for attribute,value in ats.items():
# #             if type(value) == str:
# #                 tag_open += ' {}="{}"'.format(attribute,value)
# #             elif type(value) == pd.Series:
# #
# #                 tag_open += ' ' + attribute + '="' + value + '"'
# #         tag_open += self.openr
# #
# #         return tag_open
# #
# #     def add_attributes(self,**attrs):
# #         check = self.check_for_class(attrs)
# #         self.ats.update(check)
# #
# #     def copy(self):
# #         new_boi = self
# #         return new_boi
# #
# #
# # a = Tagger('a', href='')
# # img = Tagger('img', single=True, src='' )
# # div = Tagger('div')
# # p = Tagger('p')
# # h2 = Tagger('h2')
# # br = Tagger('br',single=True)
#
#
# # class LineTag:
# #     def __init__(self,tag,params={}):
# #         self.tag = tag
# #         self.params = params
# #
# #     def tag(self,params={}):
# #         params.update(self.params)
# #         tag = '<' + self.tag
# #         for attribute,value in params:
#
#
# # a = Tagger('a')
# # nav_a = Tagger('a',params = {'class':'nav'})
# # br = LineTag('br', single=True)
# # img = LineTag('img',single = True)
# # image_tags = img.wrap(attrs = {'src':link_col})
#
#
#
#
# # def a_wrap(to_wrap,link_url):
# #     tagopen0 = '<a href="'
# #     tagopen1 = '">'
# #     tagclosed = '</a>'
# #     return tagopen0 + link_url + tagopen1 + to_wrap + tagclosed
# #
# # def img_wrap(img_urls):
# #     tagopen = '<img src="'
# #     tagclosed = '" />'
# #     return tagopen + img_urls + tagclosed
