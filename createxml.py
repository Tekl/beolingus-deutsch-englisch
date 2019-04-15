#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DIESES SCRIPT BITTE NICHT MANUELL AUSFÜHREN
# ES WIRD PER "MAKE" AUFGERUFEN

import os,sys,time,re,codecs,datetime,urllib,string,subprocess,pickle,email,time

def progress(a,b,c):
    sys.stdout.write(".")

def sort_by_value(d):
    """ Returns the keys of dictionary d sorted by their values """
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

def normalize(s):
    s = s.replace(u"ä","a")
    s = s.replace(u"ö","o")
    s = s.replace(u"ü","u")
    s = s.replace(u"Ä","A")
    s = s.replace(u"Ö","O")
    s = s.replace(u"Ü","U")
    return s

def temp_entities(s):
    s = s.replace(u"&","!!!-#amp#-!!!")
    s = s.replace(u"\"","!!!-#quot#-!!!")
    s = s.replace(u"<","!!!-#lt#-!!!")
    s = s.replace(u">","!!!-#gt#-!!!")
    return s

def real_entities(s):
    s = s.replace("!!!-#","&")
    s = s.replace("#-!!!",";")
    return s

def entities(s):
    s = s.replace(u"&","&amp;")
    s = s.replace(u"\"","&quot;")
    s = s.replace(u"<","&lt;")
    s = s.replace(u">","&gt;")
    return s

def strip_tags(value):
    r = re.compile(r'<[^>]*?>')
    return r.sub('', value).replace(u" "," ").strip()

def generate_id(element):
    id = re.sub(u'(?u)[\"<>,«»„“”‚‘’]','',element.lower())
    id = id.replace(" ","_")
    id = re.sub("(?u)_+","_",id)
    id = re.sub("(?u)(.)_$","\\1",id)
    id = str(lng) + "_" + id
    id = re.sub("(?u)_+","_",id)
    id = id[:127]
    return id

os.system("clear")

dict = "de-en"
dictFull = "BeoLingus De-En"
StopWordsDE_1 = "der|die|das|in|im|ein|wo|an|am|hat|hatte"
StopWordsDE_2 = "er/sie|er/sie/es|ich/er/sie/es|ich/er/sie|ich|er|sie|es|wir|werden|ihm|ihr|wird|wurde|ist/war|hat/hatte|ist|war|sich|jdn./etw.|etw.|jmd.|jdn."
StopWordsEN_1 = "to|in|into|the|a|an|on|has|had"
StopWordsEN_2 = "he/she|he/she/it|i/he/she/it|i/he/she|i|he|she|it|they|we|his|her|him|itself|herself|himself|would|will|has/had|is/was|was|is|of|sb./sth.|sth.|sbd.|sb."
Flags = {'de':u'🇩🇪','en':u'🇬🇧'}

print "Lexikon-Plugin ("+dictFull+") auf Basis von Beolingus.de"
print "CreateXML v2.0.0 von Wolfgang Reszel, 2019-04-10"
print
morphology = {}
for file in ["morphology-cache.txt","../Morphologie_Deutsch/morphology-cache.txt"]:
    if os.path.isfile(file):
        print "Morpholgie-Cache-Datei gefunden und geladen.\n"
        morphcache = open(file,'r')
        morphology = pickle.load(morphcache)
        morphcache.close()
        for id in morphology:
            morphology[id] = re.sub(r'^(Adjektiv,|Substantiv,|Verb,)','',morphology[id])
            morphology[id] = re.sub(r'^([^,]+)(Adjektiv,|Substantiv,|Verb,)',r'\1,',morphology[id])
        break

print "Aktuelle Wortliste wird herunterladen ..."

bundleVersion = datetime.datetime.today().strftime("%Y.%m.%d")
#bundleVersion = "2007.10.10"

urllib.urlcleanup()
download = urllib.urlretrieve("http://ftp.tu-chemnitz.de/pub/Local/urz/ding/"+dict+"-devel/"+dict+".txt.gz","de-en.txt.gz",progress)
if string.find(str(download[1]),"Error") > 0:
    print "\nHerunterladen fehlgeschlagen, bitte später noch mal versuchen\n"
    print download[1]
    exit()

timestamp = re.sub("(?s)^.*Last-Modified: ([^\n]+)\n.*$","\\1",str(download[1]))
downloadfiledate = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%d.%m.%Y")
downloadfileyear = datetime.datetime.fromtimestamp(time.mktime(email.Utils.parsedate(timestamp))).strftime("%Y")

print "\nHeruntergeladene Datei wird entpackt ..."
os.system('gzip -d -f '+dict+'.txt.gz')
# downloadfiledate = datetime.datetime.today().strftime("%d.%m.%Y")
# downloadfileyear = datetime.datetime.today().strftime("%Y")

print "\nDatei wird analysiert ..."
sourcefile = codecs.open(dict+'.txt','r','UTF-8')
sourcefile_content = re.sub(u'\u0085', '' , sourcefile.read())
sourcefile_content = re.sub(' ', ' ' , sourcefile_content).splitlines()


result = {}
dvalues = {}
titles = {}
formatted = {}
lengths = {}
linkwords = {}
seealsos = {}
lngs = {}
wordcount = 0

speedvar = ""

for line in sorted(sourcefile_content):
    if line[0] == "#" or line.strip() == "":
        continue

    #speedup
    if speedvar != "":
        if speedvar in line: #[:6]:
            print line
            pass
        else:
            continue

    line = line.strip()
    line = line.replace(":: ::","::")
    line = line.replace("| ::","|")
    line = line.replace("; ", " ; ")
    line = re.sub("(\([^();]+) *; ([^();]+) *; ([^();]+) *; ([^();]+\))",r"\1, \2, \3, \4", line)
    line = re.sub("(\{[^{};]+) *; ([^{};]+) *; ([^{};]+) *; ([^{};]+\})",r"\1, \2, \3, \4", line)
    line = re.sub("(\([^();]+) *; ([^();]+) *; ([^();]+\))",r"\1, \2, \3", line)
    line = re.sub("(\{[^{};]+) *; ([^{};]+) *; ([^{};]+\})",r"\1, \2, \3", line)
    line = re.sub("(\([^();]+) *; ([^();]+\))",r"\1, \2", line)
    line = re.sub("(\{[^{};]+) *; ([^{};]+\})",r"\1, \2", line)
    #print line
    wordlist = line.split("::")
    wordlist[0] = re.sub('"([^"]+)"',r'„\1“'.decode("utf-8"),wordlist[0])
    wordlist[1] = re.sub('"([^"]+)"',r'“\1”'.decode("utf-8"),wordlist[1])
    wordlist[0] = re.sub('\'([^\']+)\'',r'‚\1‘'.decode("utf-8"),wordlist[0])
    wordlist[1] = re.sub('\'([^\']+)\'',r'‘\1’'.decode("utf-8"),wordlist[1])
    wordlist[0] = re.sub('\'',r'’'.decode("utf-8"),wordlist[0])
    wordlist[1] = re.sub('\'',r'’'.decode("utf-8"),wordlist[1])

    for lng in range(2):
        if lng == 0:
            source = re.split('\|',wordlist[0])
            destination = re.split('\|',wordlist[1])
        else:
            source = re.split('\|',wordlist[1])
            destination = re.split('\|',wordlist[0])
        #print destination

        index = 0
        fachgebiet = ''
        fachgebietListe = re.findall('(\[[^\]]+\])', wordlist[0])
        if len(fachgebietListe) > 0:
            fachgebiet = fachgebietListe[0]

        for sourceelement in source:
            sourceelement = sourceelement.strip()
            if sourceelement == "":
                continue

            #print index
            #print destination[index]

            translations = destination[index] #entities(destination[index])
            translations = translations.replace(u"<",u"‹")
            translations = translations.replace(u">",u"›")
            translations = temp_entities(translations)

            #print translations

            translations = re.sub(' /([^/;]+)\s*;\s*([^/;]+)/', u' /\\1, \\2/',translations)
            translations = re.sub(' /([^/]+)/', u' <span class="s3">= \\1</span>',translations)
            translations = re.sub('(\([^()]+\))', u' <span class="s1">\\1</span>',translations)
            translations = re.sub('(\{[^{}]+\})', u' <i class="s2">\\1</i>',translations)
            translations = re.sub('(\[[^\[\]]+\])', u' <span class="s2">\\1</span>',translations)
            translations = re.sub(u'(‹[^‹›]+›)', u' <span class="s2">\\1</span>',translations)
            translations = re.sub(' +', ' ',translations)
            translations = translations.replace(" ; ", "; ").strip()
            translations = translations.replace(" , ", ", ").strip()
            translations = re.sub('> *<',u'> <',translations).strip()

            sourceelement2 = re.sub(' /([^/;]+)\s*;\s*([^/;]+)/',r" ; \1 ; \2", sourceelement)
            sourceelement2 = re.sub(" /([^/]+)/",r" ; \1", sourceelement2)

            elements = re.split(u" ; ",sourceelement2)

            sourceelement = sourceelement.replace(" ; ", "; ").strip()

            id = ''
            for element in elements:
                if element == "":
                    continue

                if fachgebiet != "":
                    if fachgebiet not in element:
                        element = element.strip() + " " + fachgebiet.strip()

                #if id == "":
                id = generate_id(element)

                if lng == 0:
                    lngs[id] = "de"
                else:
                    lngs[id] = "en"

                dvalue = re.sub('\([^)]+\)|\{[^}]+\}|\[[^]]+\]|<[^<>]+>',"",element).strip()
                if dvalue == "":
                    dvalue = re.sub('\{[^}]+\}|\[[^]]+\]|<[^<>]+>',"",element).strip()
                    dvalue = re.sub('\(|\)',"",dvalue).strip()
                if dvalue == "":
                    continue

                dvalue = re.sub('(.+)(\([^\(\)]+|\))$',"\\1",dvalue).strip()
                dvalue = re.sub('(.+)(\{[^\{\}]+|\})$',"\\1",dvalue).strip()
                dvalue = re.sub('(.+)(\[[^\[\]]+|\])$',"\\1",dvalue).strip()

                # normalization
                # prepare index string // remove all kinds of additional descriptions
                id_norm = dvalue
                id_norm = re.sub('(\([^)]+\))', r'',id_norm)
                id_norm = re.sub('(\{[^}]+\})', r'',id_norm)
                id_norm = re.sub('(\[[^]]+\])', r'',id_norm)
                if lng == 0:
                    id_norm = re.sub('^\s*('+StopWordsDE_1+')\s+', '',id_norm)
                    id_norm2 = re.sub('(^|\s)('+StopWordsDE_2+')(\s|$)', r'\1',id_norm)
                    if id_norm2 != "":
                        id_norm = id_norm2
                    id_norm3 = re.sub('(^|\s)('+StopWordsDE_2+')(\s|$)', r'\1',id_norm)
                    if id_norm3 != "":
                        id_norm = id_norm3
                else:
                    id_norm = re.sub('^\s*('+StopWordsEN_1+')\s+', '',id_norm)
                    id_norm2 = re.sub('(^|\s)('+StopWordsEN_2+')(\s|$)', r'\1',id_norm)
                    if id_norm2 != "":
                        id_norm = id_norm2
                    id_norm3 = re.sub('(^|\s)('+StopWordsEN_2+')(\s|$)', r'\1',id_norm)
                    if id_norm3 != "":
                        id_norm = id_norm3

                id_norm = re.sub('  ', r' ', id_norm) # remove
                id_norm = re.sub('  ', r' ', id_norm) # remove
                id_norm = id_norm.strip()   # .lower()
                id_norm = ' '.join(id_norm.split()[:16]) #id_norm[:64]
                if id_norm.endswith("-"): id_norm = id_norm[:-1]
                if id_norm == "":
                    dvalue2 = dvalue
                else:
                    dvalue2 = id_norm

                dvalue = entities(re.sub(u'(?u)[«»„“”‚‘’]','',dvalue))
                dvalue2 = entities(re.sub(u'(?u)[«»„“”‚‘’]','',dvalue2))
                dvalue = ' '.join(dvalue.split()[:16]) #dvalue[:64]
                dvalue2 = ' '.join(dvalue2.split()[:16]) #dvalue2[:64]

                #print normalize(dvalue).lower()

                if fachgebiet != "":
                    if fachgebiet not in sourceelement:
                        sourceelement = sourceelement + fachgebiet

                formattedsource = re.sub(' /([^/;]+)\s*;\s*([^/;]+)/', u' /\\1, \\2/',temp_entities(sourceelement))
                formattedsource = re.sub('\s+/([^/]+)/', u' <span class="s3">= \\1</span>',formattedsource)
                formattedsource = re.sub('(\([^()]+\))', u' <span class="s1">\\1</span>',formattedsource)
                formattedsource = re.sub('(\[[^\[\]]+\])', u' <span class="s2">\\1</span>',formattedsource)
                formattedsource = re.sub('(\{[^{}]+\})', u' <i class="s2">\\1</i>',formattedsource)
                formattedsource = re.sub(u'(‹[^‹›]+›)', u' <span class="s2">\\1</span>',formattedsource)
                formattedsource = re.sub('^([^<>;]+)(;|<|$)', r'<b>\1</b>\2',formattedsource)
                formattedsource = re.sub(' +', ' ',formattedsource)
                formattedsource = re.sub('> *<',u'> <',formattedsource).strip()
                formattedsource = formattedsource.replace(" </","</")

                #print formattedsource

                if result.has_key(id):
                    for srcElement in formattedsource.split(" ; "):
                        if strip_tags(srcElement)+";" not in strip_tags(formatted[id])+";":
                            srcElement = re.sub(r'</?b>','',srcElement)
                            formatted[id] = formatted[id] + '; '+srcElement.strip()
                    if "<p>" + translations.replace(u" "," ").lower() + "</p>" not in result[id].replace(u" "," ").lower():
                        result[id] = result[id] + "\n<p>" + translations + "</p>"
                    if '<d:index d:value="'+normalize(dvalue.lower())+'"' not in normalize(dvalues[id].lower()):
                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+dvalue+'" d:title="'+dvalue+'"/>'
                    if '<d:index d:value="'+normalize(dvalue2.lower())+'"' not in normalize(dvalues[id].lower()):
                        dvalues[id] = dvalues[id] + '\n<d:index d:value="'+dvalue2+'" d:title="'+dvalue2+'"/>'
                else:
                    lengths[id] = len(element)
                    result[id] = "<p>" + translations + "</p>"
                    dvalues[id] = '<d:index d:value="'+dvalue+'" d:title="'+dvalue+'"/>'
                    if dvalue != dvalue2:
                        if '<d:index d:value="'+normalize(dvalue2.lower())+'"' not in normalize(dvalues[id].lower()):
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="'+dvalue2+'" d:title="'+dvalue2+u' → '+dvalue+'"/>'
                    linkwords[id] = urllib.quote_plus(re.sub('\([^)]+\)|{[^}]+}|\[[^\]]+\]| /([^/]+)/|<[^<>]+>',"",element).strip().encode("utf-8"))
                    titles[id] = temp_entities(element)
                    formatted[id] = formattedsource
                    dvalueSplit = dvalue.split()
                    seealsos[id] = ""

                #print dvalue
                #print " "+dvalue2

                # resolve he/she/it
                dvalue3 = re.sub("^([a-zA-Z]+/[a-zA-Z/]+) .*$","\\1",dvalue)
                if dvalue3 != dvalue:
                    for dvalueSub in dvalue3.split("/"):
                        dvalue4 = dvalueSub+re.sub("^([a-zA-Z]+/[a-zA-Z/]+)( .*)$", "\\2", dvalue)
                        if '<d:index d:value="'+normalize(dvalue4.lower())+'"' not in normalize(dvalues[id].lower()):
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="'+dvalue4+'" d:title="'+dvalue4+'"/>'
                        if lng == 0:
                            dvalue4 = re.sub('^\s*('+StopWordsDE_1+')\s+', '',dvalue4)
                            dvalue42 = re.sub('(^|\s)('+StopWordsDE_2+')(\s|$)', r'\1',dvalue4)
                            if dvalue42 != "":
                                dvalue4 = dvalue42
                            dvalue43 = re.sub('(^|\s)('+StopWordsDE_2+')(\s|$)', r'\1',dvalue4)
                            if dvalue43 != "":
                                dvalue4 = dvalue43
                        else:
                            dvalue4 = re.sub('^\s*('+StopWordsEN_1+')\s+', '',dvalue4)
                            dvalue42 = re.sub('(^|\s)('+StopWordsEN_2+')(\s|$)', r'\1',dvalue4)
                            if dvalue42 != "":
                                dvalue4 = dvalue42
                            dvalue43 = re.sub('(^|\s)('+StopWordsEN_2+')(\s|$)', r'\1',dvalue4)
                            if dvalue43 != "":
                                dvalue4 = dvalue43
                        if '<d:index d:value="'+normalize(dvalue4.lower())+'"' not in normalize(dvalues[id].lower()):
                            dvalues[id] = dvalues[id] + '\n<d:index d:value="'+dvalue4+'" d:title="'+dvalue4+'"/>'

                for sElements in source:
                    #print sElements
                    sElements = re.sub(' /([^/;]+)\s*;\s*([^/;]+)/',r" ; \1 ; \2", sElements)
                    sElements = re.sub(" /([^/]+)/",r" ; \1", sElements)
                    for sElement in sElements.split(" ; "):
                        seealso = re.sub('\([^)]+\)|\{[^}]+\}|\[[^]]+\]| /([^/]+)/|<[^<>]+>',"",sElement).strip()
                        if seealso == "":
                            seealso = re.sub('\{[^}]+\}|\[[^]]+\]| /([^/]+)/|<[^<>]+>',"",sElement).strip()
                            seealso = re.sub('\(|\)',"",seealso).strip()
                        seealso = re.sub('(.+)(\([^\(\)]+|\))$',"\\1",seealso).strip()
                        seealso = re.sub('(.+)(\{[^\{\}]+|\})$',"\\1",seealso).strip()
                        seealso = re.sub('(.+)(\[[^\[\]]+|\])$',"\\1",seealso).strip()
                        seealso = seealso.replace(" , ",", ")
                        if re.search("(\W|^)"+re.escape(seealso)+"(\W|$)",formattedsource):
                            if seealsos[id] != "":
                                seealsos[id] = re.sub("(^|, )"+re.escape(seealso)+"($|, )","\\1",seealsos[id])
                                seealsos[id] = re.sub(", $|^, ","",seealsos[id])
                            continue
                        if dvalue in seealso or seealso in seealsos[id] or seealso == "" or "," in seealso or ";" in seealso:
                            continue

                        seealso = temp_entities(seealso)

                        if seealsos[id] == "":
                            seealsos[id] = '<a href="x-dictionary:d:'+seealso+'">'+seealso+'</a>'
                        else:
                            seealsos[id] = seealsos[id].strip() + ", " + '<a href="x-dictionary:d:'+seealso+'">'+seealso+'</a>'

                if morphology.has_key(dvalue2) and lng == 0:
                    for x in morphology[dvalue2].split(","):
                        x = temp_entities(x)
                        if u'<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()):
                            if x[:len(dvalue)].lower() == dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+'"/>'
                if morphology.has_key(dvalue) and lng == 0:
                    for x in morphology[dvalue].split(","):
                        x = temp_entities(x)
                        if u'<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()):
                            if x[:len(dvalue)].lower() == dvalue.lower():
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+'"/>'
                            else:
                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+'"/>'

                dvalueSplit = dvalue.split()
                for i in dvalueSplit:
                    if len(i) > 1:
                        devalueHyphenSplit = i.split("-")
                        for j in range(1,len(devalueHyphenSplit)):
                            if len(devalueHyphenSplit[j]) > 1:
                                if '<d:index d:value="'+normalize(devalueHyphenSplit[j].lower())+'"' not in normalize(dvalues[id].lower()):
                                    dvalues[id] = dvalues[id] + '\n<d:index d:value="'+temp_entities(devalueHyphenSplit[j])+u'" d:title="'+temp_entities(devalueHyphenSplit[j])+u'⇒ '+dvalue+'"/>'
                                if morphology.has_key(devalueHyphenSplit[j]):
                                    for x in morphology[devalueHyphenSplit[j]].split(","):
                                        x = temp_entities(x)
                                        if u'<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()):
                                            if x[:len(dvalue)].lower() == dvalue.lower():
                                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+'"/>'
                                            else:
                                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+'"/>'
                        if '<d:index d:value="'+normalize(i.lower())+'"' not in normalize(dvalues[id].lower()):
                            if i[0] != "-" and i[len(i)-1] != "-":
                                if dvalue[:len(i)].lower() != i.lower():
                                    dvalues[id] = dvalues[id] + '\n<d:index d:value="'+temp_entities(i)+u'" d:title="'+temp_entities(i)+u' ⇒ '+dvalue+'"/>'
                                if morphology.has_key(i):
                                    for x in morphology[i].split(","):
                                        x = temp_entities(x)
                                        if u'<d:index d:value="'+normalize(x.lower())+u'"' not in normalize(dvalues[id].lower()):
                                            if x[:len(dvalue)].lower() == dvalue.lower():
                                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' → '+dvalue+'"/>'
                                            else:
                                                dvalues[id] = dvalues[id] + '\n<d:index d:value="'+x+u'" d:title="'+x+u' ⇒ '+dvalue+'"/>'

            index+=1

sourcefile.close()

print "\nXML-Datei wird erzeugt ..."
destfile = codecs.open(dictFull+'.xml','w','utf-8')
destfile.write("""<?xml version="1.0" encoding="utf-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">""")

for id in sorted(lengths):
    newid = re.sub(u'(?u)_?\([^)]+\)|_?\{[^}]+\}|_?\[[^]]+\]|_?<[^<>]+>',"",id[2:]).strip()
    if newid == "":
        newid = re.sub(u'(?u)_\([^)]+\)|_\{[^}]+\}|_\[[^]]+\]|_<[^<>]+>',"",id[2:]).strip()
    if lngs[id] == 'de':
        newid = re.sub('^('+StopWordsDE_1+')_+', '',newid)
        newid2 = re.sub('(^|_)('+StopWordsDE_2+')(_|$)', r'\1',newid)
        if newid2 != "":
            newid = newid2
        newid3 = re.sub('(^|_)('+StopWordsDE_2+')(_|$)', r'\1',newid)
        if newid3 != "":
            newid = newid3
    else:
        newid = re.sub('^('+StopWordsEN_1+')_+', '',newid)
        newid2 = re.sub('(^|_)('+StopWordsEN_2+')(_|$)', r'\1',newid)
        if newid2 != "":
            newid = newid2
        newid3 = re.sub('(^|_)('+StopWordsEN_2+')(_|$)', r'\1',newid)
        if newid3 != "":
            newid = newid3
    if newid == "":
        newid = id
    if newid != id:
        if lengths.has_key(newid):
            addvalues = dvalues[id].split('\n')
            for addvalue in addvalues:
                if addvalue not in dvalues[newid]:
                    dvalues[newid] = dvalues[newid]+'\n'+addvalue
            addalsos = seealsos[id].split(', ')
            for addalso in addalsos:
                if addalso not in seealsos[newid]:
                    seealsos[newid] = seealsos[newid]+', '+addalso
            #titles[newid] = titles[newid]+titles[id]
            formattedNEWID = re.sub('^.*(<b>.+?</b>).*$','\\1',formatted[newid])
            formattedID = re.sub('^.*(<b>.+?</b>).*$','\\1',formatted[id])
            linkwords[newid] = linkwords[newid]+linkwords[id]
            if len(formattedID) < len(formattedNEWID):
                formattedTMP = formatted[newid]
                formatted[newid] = formatted[id]
                result[newid] = result[id]+'\n<h2><span class="flag" title="'+lngs[id]+'">'+Flags[lngs[id]]+'</span>'+formattedTMP+'</h2>\n'+result[newid]
            else:
                resultNEWID = re.sub(r'(?mu)^.*(<b>.+</b>).*$','\\1',result[newid])
                if len(formattedID) < len(resultNEWID) and '<b>' in result[newid]:
                    result[newid] = result[newid].replace('<h2>','<h2><span class="flag" title="'+lngs[id]+'">'+Flags[lngs[id]]+'</span>'+formatted[id]+'</h2>\n'+result[id]+'<h2>',1)
                else:
                    result[newid] = result[newid]+'\n<h2><span class="flag" title="'+lngs[id]+'">'+Flags[lngs[id]]+'</span>'+formatted[id]+'</h2>\n'+result[id]
        else:
            lengths[newid] = lengths[id]
            dvalues[newid] = dvalues[id]
            seealsos[newid] = seealsos[id]
            formatted[newid] = formatted[id]
            result[newid] = result[id]
            titles[newid] = titles[id]
            linkwords[newid] = linkwords[id]
            lngs[newid] = lngs[id]
        del lengths[id]
        del dvalues[id]
        del seealsos[id]
        del formatted[id]
        del result[id]
        del titles[id]
        del linkwords[id]
        del lngs[id]
        id = newid

for id in sort_by_value(lengths):
    wordcount+=1
    if seealsos[id] != "":
        seealsos[id] = u'<div class="seealso"><b>Siehe auch:</b> ' + seealsos[id] + '</div>'
    formatted[id] = '<h2><span class="flag" title="'+lngs[id]+'">'+Flags[lngs[id]]+'</span>'+formatted[id]+'</h2>'
    #dvaluesClean = id+"-><br/>"+re.sub('<d:index d:value="([^"]+)" d:title="([^"]+)"/>',"\\1 ::: \\2<br/>",dvalues[id])
    #destfile.write( re.sub("  +| *\n *","", u"""
    destfile.write( re.sub("","", u"""
<d:entry id="%s" d:title="%s" class="d">
%s
%s
%s
%s
<div class="c" d:priority="2"><span><a href="https://www.beolingus.de/dings.cgi?query=%s">Aus BeoLingus.de</a> · © %s TU Chemnitz</span></div>
</d:entry>""" % (entities(id), real_entities(titles[id]), real_entities(dvalues[id]), real_entities(formatted[id]), real_entities(result[id]), real_entities(seealsos[id]), real_entities(linkwords[id]), downloadfileyear) ) )

destfile.write( u"""
<d:entry id="front_back_matter" d:title="Vorderer/hinterer Teil">
    <h1><b>BeoLingus Deutsch-Englisch</b></h1>
    <div><small><b>Version: %s</b></small></div>
    <p>
        <img src="Images/beolingus.png" align="right" style="padding-left:10px" alt=""/>
        Dieses Wörterbuch basiert auf dem Online-Wörterbuch<br/>
        <a href="https://www.beolingus.de">www.beolingus.de</a> der TU Chemnitz. (Stand: %s, %s Einträge)
    </p>
    <p>
        <b>Updates</b> finden Sie unter <a href="https://www.tekl.de">www.tekl.de</a>.<br/>
        Support und den Quellcode finden Sie unter <a href="https://github.com/Tekl/beolingus-deutsch-englisch"><b>github.com/Tekl/beolingus-deutsch-englisch</b></a>.
    </p>
    <p>
        Das Python-Skript zur Umwandlung der BeoLingus-Wortliste in eine Apple Lexikon-Datei wurde von Wolfgang Reszel entwickelt.
    </p>
    <p>
        Die Wortform-Datei (Morphologie), durch welche auch die Suche nach Worten im Plural möglich ist, wurde mit dem Windows-Tool <a href="https://morphy.wolfganglezius.de">Morphy</a> erstellt.
    </p>
    <p>
        <img src="Images/gplv3-88x31.png" align="left" style="padding-right:10px" alt=""/>
        <b>Lizenz:</b>
        Dieses Lexikon-Plug-in unterliegt der <a href="https://www.gnu.org/licenses/gpl.html">GPLv3</a><br/>
        Die Wortliste von BeoLingus unterliegt der
        <a href="https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt">GPLv2</a><br/>
    </p>
</d:entry>
</d:dictionary>""" % (bundleVersion, downloadfiledate, wordcount )  )
destfile.close()

print "\nHeruntergeladene Datei wird gelöscht ..."
os.system('rm '+dict+'.txt')

print "\nVersionsnummern werden angepasst ..."

rtfFiles = ['installer/finishup_de.rtfd/TXT.rtf','installer/finishup_en.rtfd/TXT.rtf','installer/LIESMICH.rtfd/TXT.rtf','installer/README.rtfd/TXT.rtf','LIESMICH.md','README.md','Makefile']
for filename in rtfFiles:
	print filename
	if '.rtf' in filename:
		pmdocFile = codecs.open(filename,'r','windows-1252')
	else:
		pmdocFile = codecs.open(filename,'r','UTF-8')
	pmdoc = pmdocFile.read()
	pmdoc = re.sub("Version: .\d+.\d+.\d+", "Version: "+ bundleVersion, pmdoc)
	pmdoc = re.sub(" 20\d+.\d+.\d+\"", " "+ bundleVersion+"\"", pmdoc)
	pmdoc = re.sub(" v20\d+.\d+.\d+\"", " v"+ bundleVersion+"\"", pmdoc)
	if filename == 'Makefile':
		pmdoc = re.sub("([_ ])v20\d+.\d+.\d+", "\\1v"+ bundleVersion+"", pmdoc)
		pmdoc = re.sub("/20\d+.\d+.\d+/", "/"+ bundleVersion+"/", pmdoc)
	pmdoc = re.sub(u"20\d\d Wolfgang Reszel", datetime.datetime.today().strftime("%Y")+" Wolfgang Reszel", pmdoc)
	pmdocFile.close()
	if '.rtf' in filename:
		pmdocFile = codecs.open(filename,'w','windows-1252')
	else:
		pmdocFile = codecs.open(filename,'w','UTF-8')
	pmdocFile.write( pmdoc )
	pmdocFile.close()

print "Info.plist"
plistFile = codecs.open('Info.plist','r','UTF-8')
plist = plistFile.read()
plist = re.sub("(?u)(<key>CFBundleVersion</key>\s+<string>)[^<]+(</string>)", "\\g<1>"+bundleVersion+"\\2", plist)
plist = re.sub("(?u)(<key>CFBundleShortVersionString</key>\s+<string>)[^<]+(</string>)", "\\g<1>"+bundleVersion+"\\2", plist)
plist = re.sub(u"© \d\d\d\d ", u"© "+ datetime.datetime.today().strftime("%Y")+u" ", plist)
plist = re.sub(u"\d\d\d\d TU ", datetime.datetime.today().strftime("%Y")+u" TU ", plist)
plistFile.close()
plistFile = codecs.open('Info.plist','w','UTF-8')
plistFile.write( plist )
plistFile.close()

print "\nXML-Datei wird ausgewertet (Making) ... [" + speedvar + "]\n-----------------------------------------------------"
