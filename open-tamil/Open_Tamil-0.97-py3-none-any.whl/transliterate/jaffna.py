## -*- coding: utf-8 -*-
# (C) 2013 Muthiah Annamalai
#
class Transliteration:
    """
     Implementation of Jaffna library transliteration tables
     first used in Gaim En->Ta Plugin (2006+) by Varun Soundarajan, <s.varun@gmail.com>
     and later used in TamilKaruvi (2007) by your's truly.
    """
    table = {}

    # mix of consonants and compound - uyirmei - letters
    table["njau"]=u"ஞௌ"
    table["njai"]=u"ஞை"
    table["njee"]=u"ஞே"
    table["njoo"]=u"ஞோ"
    table["njaa"]=u"ஞா"
    table["njuu"]=u"ஞூ"
    table["njii"]=u"ஞீ"
    table["nja"]=u"ஞ"
    table["nji"]=u"ஞி"
    table["njI"]=u"ஞீ"
    table["njA"]=u"ஞா"
    table["nje"]=u"ஞெ"
    table["njE"]=u"ஞே"
    table["njo"]=u"ஞொ"
    table["njO"]=u"ஞோ"
    table["nju"]=u"ஞு"
    table["njU"]=u"ஞூ"
    table["nj"]=u"ஞ்"
    table["ngau"]=u"ஙௌ"
    table["ngai"]=u"ஙை"
    table["ngee"]=u"ஙே"
    table["ngoo"]=u"ஙோ"
    table["ngaa"]=u"ஙா"
    table["nguu"]=u"ஙூ"
    table["ngii"]=u"ஙீ"
    table["nga"]=u"ங"
    table["ngi"]=u"ஙி"
    table["ngI"]=u"ஙீ"
    table["ngA"]=u"ஙா"
    table["nge"]=u"ஙெ"
    table["ngE"]=u"ஙே"
    table["ngo"]=u"ஙொ"
    table["ngO"]=u"ஙோ"
    table["ngu"]=u"ஙு"
    table["ngU"]=u"ஙூ"
    table["ng"]=u"ங்"
    table["shau"]=u"ஷௌ"
    table["shai"]=u"ஷை"
    table["shee"]=u"ஷே"
    table["shoo"]=u"ஷோ"
    table["shaa"]=u"ஷா"
    table["shuu"]=u"ஷூ"
    table["shii"]=u"ஷீ"
    table["sha"]=u"ஷ"
    table["shi"]=u"ஷி"
    table["shI"]=u"ஷீ"
    table["shA"]=u"ஷா"
    table["she"]=u"ஷெ"
    table["shE"]=u"ஷே"
    table["sho"]=u"ஷொ"
    table["shO"]=u"ஷோ"
    table["shu"]=u"ஷு"
    table["shU"]=u"ஷூ"
    table["sh"]=u"ஷ்"
    table[" nau"]=u" நௌ"
    table[" nai"]=u" நை"
    table[" nee"]=u" நே"
    table[" noo"]=u" நோ"
    table[" naa"]=u" நா"
    table[" nuu"]=u" நூ"
    table[" nii"]=u" நீ"
    table[" na"]=u" ந"
    table[" ni"]=u" நி"
    table[" nI"]=u" நீ"
    table[" nA"]=u" நா"
    table[" ne"]=u" நெ"
    table[" nE"]=u" நே"
    table[" no"]=u" நொ"
    table[" nO"]=u" நோ"
    table[" nu"]=u" நு"
    table[" nU"]=u" நூ"
    table[" nth"]=u" ந்"
    table["-nau"]=u"நௌ"
    table["-nai"]=u"நை"
    table["-nee"]=u"நே"
    table["-noo"]=u"நோ"
    table["-naa"]=u"நா"
    table["-nuu"]=u"நூ"
    table["-nii"]=u"நீ"
    table["-na"]=u"ந"
    table["-ni"]=u"நி"
    table["-nI"]=u"நீ"
    table["-nA"]=u"நா"
    table["-ne"]=u"நெ"
    table["-nE"]=u"நே"
    table["-no"]=u"நொ"
    table["-nO"]=u"நோ"
    table["-nu"]=u"நு"
    table["-nU"]=u"நூ"
    table["n-au"]=u"நௌ"
    table["n-ai"]=u"நை"
    table["n-ee"]=u"நே"
    table["n-oo"]=u"நோ"
    table["n-aa"]=u"நா"
    table["n-uu"]=u"நூ"
    table["n-ii"]=u"நீ"
    table["n-a"]=u"ந"
    table["n-i"]=u"நி"
    table["n-I"]=u"நீ"
    table["n-A"]=u"நா"
    table["n-e"]=u"நெ"
    table["n-E"]=u"நே"
    table["n-o"]=u"நொ"
    table["n-O"]=u"நோ"
    table["n-u"]=u"நு"
    table["n-U"]=u"நூ"
    table["wau"]=u"நௌ"
    table["wai"]=u"நை"
    table["wee"]=u"நே"
    table["woo"]=u"நோ"
    table["waa"]=u"நா"
    table["wuu"]=u"நூ"
    table["wii"]=u"நீ"
    table["wa"]=u"ந"
    table["wi"]=u"நி"
    table["wI"]=u"நீ"
    table["wA"]=u"நா"
    table["we"]=u"நெ"
    table["wE"]=u"நே"
    table["wo"]=u"நொ"
    table["wO"]=u"நோ"
    table["wu"]=u"நு"
    table["wU"]=u"நூ"
    table[" n"]=u" ந்"
    table["n-"]=u"ந்"
    table["-n"]=u"ந்"
    table["w"]=u"ந்"
    table["nthau"]=u"ந்தௌ"
    table["nthai"]=u"ந்தை"
    table["nthee"]=u"ந்தே"
    table["nthoo"]=u"ந்தோ"
    table["nthaa"]=u"ந்தா"
    table["nthuu"]=u"ந்தூ"
    table["nthii"]=u"ந்தீ"
    table["ntha"]=u"ந்த"
    table["nthi"]=u"ந்தி"
    table["nthI"]=u"ந்தீ"
    table["nthA"]=u"ந்தா"
    table["nthe"]=u"ந்தெ"
    table["nthE"]=u"ந்தே"
    table["ntho"]=u"ந்தொ"
    table["nthO"]=u"ந்தோ"
    table["nthu"]=u"ந்து"
    table["nthU"]=u"ந்தூ"
    table["nth"]=u"ந்"
    table["dhau"]=u"தௌ"
    table["dhai"]=u"தை"
    table["dhee"]=u"தே"
    table["dhoo"]=u"தோ"
    table["dhaa"]=u"தா"
    table["dhuu"]=u"தூ"
    table["dhii"]=u"தீ"
    table["dha"]=u"த"
    table["dhi"]=u"தி"
    table["dhI"]=u"தீ"
    table["dhA"]=u"தா"
    table["dhe"]=u"தெ"
    table["dhE"]=u"தே"
    table["dho"]=u"தொ"
    table["dhO"]=u"தோ"
    table["dhu"]=u"து"
    table["dhU"]=u"தூ"
    table["dh"]=u"த்"
    table["chau"]=u"சௌ"
    table["chai"]=u"சை"
    table["chee"]=u"சே"
    table["choo"]=u"சோ"
    table["chaa"]=u"சா"
    table["chuu"]=u"சூ"
    table["chii"]=u"சீ"
    table["cha"]=u"ச"
    table["chi"]=u"சி"
    table["chI"]=u"சீ"
    table["chA"]=u"சா"
    table["che"]=u"செ"
    table["chE"]=u"சே"
    table["cho"]=u"சொ"
    table["chO"]=u"சோ"
    table["chu"]=u"சு"
    table["chU"]=u"சூ"
    table["ch"]=u"ச்"
    table["zhau"]=u"ழௌ"
    table["zhai"]=u"ழை"
    table["zhee"]=u"ழே"
    table["zhoo"]=u"ழோ"
    table["zhaa"]=u"ழா"
    table["zhuu"]=u"ழூ"
    table["zhii"]=u"ழீ"
    table["zha"]=u"ழ"
    table["zhi"]=u"ழி"
    table["zhI"]=u"ழீ"
    table["zhA"]=u"ழா"
    table["zhe"]=u"ழெ"
    table["zhE"]=u"ழே"
    table["zho"]=u"ழொ"
    table["zhO"]=u"ழோ"
    table["zhu"]=u"ழு"
    table["zhU"]=u"ழூ"
    table["zh"]=u"ழ்"
    table["zau"]=u"ழௌ"
    table["zai"]=u"ழை"
    table["zee"]=u"ழே"
    table["zoo"]=u"ழோ"
    table["zaa"]=u"ழா"
    table["zuu"]=u"ழூ"
    table["zii"]=u"ழீ"
    table["za"]=u"ழ"
    table["zi"]=u"ழி"
    table["zI"]=u"ழீ"
    table["zA"]=u"ழா"
    table["ze"]=u"ழெ"
    table["zE"]=u"ழே"
    table["zo"]=u"ழொ"
    table["zO"]=u"ழோ"
    table["zu"]=u"ழு"
    table["zU"]=u"ழூ"
    table["z"]=u"ழ்"
    table["jau"]=u"ஜௌ"
    table["jai"]=u"ஜை"
    table["jee"]=u"ஜே"
    table["joo"]=u"ஜோ"
    table["jaa"]=u"ஜா"
    table["juu"]=u"ஜூ"
    table["jii"]=u"ஜீ"
    table["ja"]=u"ஜ"
    table["ji"]=u"ஜி"
    table["jI"]=u"ஜீ"
    table["jA"]=u"ஜா"
    table["je"]=u"ஜெ"
    table["jE"]=u"ஜே"
    table["jo"]=u"ஜொ"
    table["jO"]=u"ஜோ"
    table["ju"]=u"ஜு"
    table["jU"]=u"ஜூ"
    table["j"]=u"ஜ்"
    table["thau"]=u"தௌ"
    table["thai"]=u"தை"
    table["thee"]=u"தே"
    table["thoo"]=u"தோ"
    table["thaa"]=u"தா"
    table["thuu"]=u"தூ"
    table["thii"]=u"தீ"
    table["tha"]=u"த"
    table["thi"]=u"தி"
    table["thI"]=u"தீ"
    table["thA"]=u"தா"
    table["the"]=u"தெ"
    table["thE"]=u"தே"
    table["tho"]=u"தொ"
    table["thO"]=u"தோ"
    table["thu"]=u"து"
    table["thU"]=u"தூ"
    table["th"]=u"த்"
    table["-hau"]=u"ஹௌ"
    table["-hai"]=u"ஹை"
    table["-hee"]=u"ஹே"
    table["-hoo"]=u"ஹோ"
    table["-haa"]=u"ஹா"
    table["-huu"]=u"ஹூ"
    table["-hii"]=u"ஹீ"
    table["-ha"]=u"ஹ"
    table["-hi"]=u"ஹி"
    table["-hI"]=u"ஹீ"
    table["-hA"]=u"ஹா"
    table["-he"]=u"ஹெ"
    table["-hE"]=u"ஹே"
    table["-ho"]=u"ஹொ"
    table["-hO"]=u"ஹோ"
    table["-hu"]=u"ஹு"
    table["-hU"]=u"ஹூ"
    table["-h"]=u"ஹ்"
    table["hau"]=u"கௌ"
    table["hai"]=u"கை"
    table["hee"]=u"கே"
    table["hoo"]=u"கோ"
    table["haa"]=u"கா"
    table["huu"]=u"கூ"
    table["hii"]=u"கீ"
    table["ha"]=u"க"
    table["hi"]=u"கி"
    table["hI"]=u"கீ"
    table["hA"]=u"கா"
    table["he"]=u"கெ"
    table["hE"]=u"கே"
    table["ho"]=u"கொ"
    table["hO"]=u"கோ"
    table["hu"]=u"கு"
    table["hU"]=u"கூ"
    table["h"]=u"க்"
    table["kau"]=u"கௌ"
    table["kai"]=u"கை"
    table["kee"]=u"கே"
    table["koo"]=u"கோ"
    table["kaa"]=u"கா"
    table["kuu"]=u"கூ"
    table["kii"]=u"கீ"
    table["ka"]=u"க"
    table["ki"]=u"கி"
    table["kI"]=u"கீ"
    table["kA"]=u"கா"
    table["ke"]=u"கெ"
    table["kE"]=u"கே"
    table["ko"]=u"கொ"
    table["kO"]=u"கோ"
    table["ku"]=u"கு"
    table["kU"]=u"கூ"
    table["k"]=u"க்"
    table["-sau"]=u"ஸௌ"
    table["-sai"]=u"ஸை"
    table["-see"]=u"ஸே"
    table["-soo"]=u"ஸோ"
    table["-saa"]=u"ஸா"
    table["-suu"]=u"ஸூ"
    table["-sii"]=u"ஸீ"
    table["-sa"]=u"ஸ"
    table["-si"]=u"ஸி"
    table["-sI"]=u"ஸீ"
    table["-sA"]=u"ஸா"
    table["-se"]=u"ஸெ"
    table["-sE"]=u"ஸே"
    table["-so"]=u"ஸொ"
    table["-sO"]=u"ஸோ"
    table["-su"]=u"ஸு"
    table["-sU"]=u"ஸூ"
    table["-s"]=u"ஸ்"
    table["Sau"]=u"ஸௌ"
    table["Sai"]=u"ஸை"
    table["See"]=u"ஸே"
    table["Soo"]=u"ஸோ"
    table["Saa"]=u"ஸா"
    table["Suu"]=u"ஸூ"
    table["Sii"]=u"ஸீ"
    table["Sa"]=u"ஸ"
    table["Si"]=u"ஸி"
    table["SI"]=u"ஸீ"
    table["SA"]=u"ஸா"
    table["Se"]=u"ஸெ"
    table["SE"]=u"ஸே"
    table["So"]=u"ஸொ"
    table["SO"]=u"ஸோ"
    table["Su"]=u"ஸு"
    table["SU"]=u"ஸூ"
    table["S"]=u"ஸ்"
    table["rau"]=u"ரௌ"
    table["rai"]=u"ரை"
    table["ree"]=u"ரே"
    table["roo"]=u"ரோ"
    table["raa"]=u"ரா"
    table["ruu"]=u"ரூ"
    table["rii"]=u"ரீ"
    table["ra"]=u"ர"
    table["ri"]=u"ரி"
    table["rI"]=u"ரீ"
    table["rA"]=u"ரா"
    table["re"]=u"ரெ"
    table["rE"]=u"ரே"
    table["ro"]=u"ரொ"
    table["rO"]=u"ரோ"
    table["ru"]=u"ரு"
    table["rU"]=u"ரூ"
    table["r"]=u"ர்"
    table["Rau"]=u"றௌ"
    table["Rai"]=u"றை"
    table["Ree"]=u"றே"
    table["Roo"]=u"றோ"
    table["Raa"]=u"றா"
    table["Ruu"]=u"றூ"
    table["Rii"]=u"றீ"
    table["Ra"]=u"ற"
    table["Ri"]=u"றி"
    table["RI"]=u"றீ"
    table["RA"]=u"றா"
    table["Re"]=u"றெ"
    table["RE"]=u"றே"
    table["Ro"]=u"றொ"
    table["RO"]=u"றோ"
    table["Ru"]=u"று"
    table["RU"]=u"றூ"
    table["R"]=u"ற்"
    table["tau"]=u"டௌ"
    table["tai"]=u"டை"
    table["tee"]=u"டே"
    table["too"]=u"டோ"
    table["taa"]=u"டா"
    table["tuu"]=u"டூ"
    table["tii"]=u"டீ"
    table["ta"]=u"ட"
    table["ti"]=u"டி"
    table["tI"]=u"டீ"
    table["tA"]=u"டா"
    table["te"]=u"டெ"
    table["tE"]=u"டே"
    table["to"]=u"டொ"
    table["tO"]=u"டோ"
    table["tu"]=u"டு"
    table["tU"]=u"டூ"
    table["t"]=u"ட்"
    table["sau"]=u"சௌ"
    table["sai"]=u"சை"
    table["see"]=u"சே"
    table["soo"]=u"சோ"
    table["saa"]=u"சா"
    table["suu"]=u"சூ"
    table["sii"]=u"சீ"
    table["sa"]=u"ச"
    table["si"]=u"சி"
    table["sI"]=u"சீ"
    table["sA"]=u"சா"
    table["se"]=u"செ"
    table["sE"]=u"சே"
    table["so"]=u"சொ"
    table["sO"]=u"சோ"
    table["su"]=u"சு"
    table["sU"]=u"சூ"
    table["s"]=u"ச்"
    table["pau"]=u"பௌ"
    table["pai"]=u"பை"
    table["pee"]=u"பே"
    table["poo"]=u"போ"
    table["paa"]=u"பா"
    table["puu"]=u"பூ"
    table["pii"]=u"பீ"
    table["pa"]=u"ப"
    table["pi"]=u"பி"
    table["pI"]=u"பீ"
    table["pA"]=u"பா"
    table["pe"]=u"பெ"
    table["pE"]=u"பே"
    table["po"]=u"பொ"
    table["pO"]=u"போ"
    table["pu"]=u"பு"
    table["pU"]=u"பூ"
    table["p"]=u"ப்"
    table["bau"]=u"பௌ"
    table["bai"]=u"பை"
    table["bee"]=u"பே"
    table["boo"]=u"போ"
    table["baa"]=u"பா"
    table["buu"]=u"பூ"
    table["bii"]=u"பீ"
    table["ba"]=u"ப"
    table["bi"]=u"பி"
    table["bI"]=u"பீ"
    table["bA"]=u"பா"
    table["be"]=u"பெ"
    table["bE"]=u"பே"
    table["bo"]=u"பொ"
    table["bO"]=u"போ"
    table["bu"]=u"பு"
    table["bU"]=u"பூ"
    table["b"]=u"ப்"
    table["mau"]=u"மௌ"
    table["mai"]=u"மை"
    table["mee"]=u"மே"
    table["moo"]=u"மோ"
    table["maa"]=u"மா"
    table["muu"]=u"மூ"
    table["mii"]=u"மீ"
    table["ma"]=u"ம"
    table["mi"]=u"மி"
    table["mI"]=u"மீ"
    table["mA"]=u"மா"
    table["me"]=u"மெ"
    table["mE"]=u"மே"
    table["mo"]=u"மொ"
    table["mO"]=u"மோ"
    table["mu"]=u"மு"
    table["mU"]=u"மூ"
    table["m"]=u"ம்"
    table["yau"]=u"யௌ"
    table["yai"]=u"யை"
    table["yee"]=u"யே"
    table["yoo"]=u"யோ"
    table["yaa"]=u"யா"
    table["yuu"]=u"யூ"
    table["yii"]=u"யீ"
    table["ya"]=u"ய"
    table["yi"]=u"யி"
    table["yI"]=u"யீ"
    table["yA"]=u"யா"
    table["ye"]=u"யெ"
    table["yE"]=u"யே"
    table["yo"]=u"யொ"
    table["yO"]=u"யோ"
    table["yu"]=u"யு"
    table["yU"]=u"யூ"
    table["y"]=u"ய்"
    table["dau"]=u"டௌ"
    table["dai"]=u"டை"
    table["dee"]=u"டே"
    table["doo"]=u"டோ"
    table["daa"]=u"டா"
    table["duu"]=u"டூ"
    table["dii"]=u"டீ"
    table["da"]=u"ட"
    table["di"]=u"டி"
    table["dI"]=u"டீ"
    table["dA"]=u"டா"
    table["de"]=u"டெ"
    table["dE"]=u"டே"
    table["do"]=u"டொ"
    table["dO"]=u"டோ"
    table["du"]=u"டு"
    table["dU"]=u"டூ"
    table["d"]=u"ட்"
    table["nau"]=u"னௌ"
    table["nai"]=u"னை"
    table["nee"]=u"னே"
    table["noo"]=u"னோ"
    table["naa"]=u"னா"
    table["nuu"]=u"னூ"
    table["nii"]=u"னீ"
    table["na"]=u"ன"
    table["ni"]=u"னி"
    table["nI"]=u"னீ"
    table["nA"]=u"னா"
    table["ne"]=u"னெ"
    table["nE"]=u"னே"
    table["no"]=u"னொ"
    table["nO"]=u"னோ"
    table["nu"]=u"னு"
    table["nU"]=u"னூ"
    table["n"]=u"ன்"
    table["Nau"]=u"ணௌ"
    table["Nai"]=u"ணை"
    table["Nee"]=u"ணே"
    table["Noo"]=u"ணோ"
    table["Naa"]=u"ணா"
    table["Nuu"]=u"ணூ"
    table["Nii"]=u"ணீ"
    table["Na"]=u"ண"
    table["Ni"]=u"ணி"
    table["NI"]=u"ணீ"
    table["NA"]=u"ணா"
    table["Ne"]=u"ணெ"
    table["NE"]=u"ணே"
    table["No"]=u"ணொ"
    table["NO"]=u"ணோ"
    table["Nu"]=u"ணு"
    table["NU"]=u"ணூ"
    table["N"]=u"ண்"
    table["lau"]=u"லௌ"
    table["lai"]=u"லை"
    table["lee"]=u"லே"
    table["loo"]=u"லோ"
    table["laa"]=u"லா"
    table["luu"]=u"லூ"
    table["lii"]=u"லீ"
    table["la"]=u"ல"
    table["li"]=u"லி"
    table["lI"]=u"லீ"
    table["lA"]=u"லா"
    table["le"]=u"லெ"
    table["lE"]=u"லே"
    table["lo"]=u"லொ"
    table["lO"]=u"லோ"
    table["lu"]=u"லு"
    table["lU"]=u"லூ"
    table["l"]=u"ல்"
    table["Lau"]=u"ளௌ"
    table["Lai"]=u"ளை"
    table["Lee"]=u"ளே"
    table["Loo"]=u"ளோ"
    table["Laa"]=u"ளா"
    table["Luu"]=u"ளூ"
    table["Lii"]=u"ளீ"
    table["La"]=u"ள"
    table["Li"]=u"ளி"
    table["LI"]=u"ளீ"
    table["LA"]=u"ளா"
    table["Le"]=u"ளெ"
    table["LE"]=u"ளே"
    table["Lo"]=u"ளொ"
    table["LO"]=u"ளோ"
    table["Lu"]=u"ளு"
    table["LU"]=u"ளூ"
    table["L"]=u"ள்"
    table["vau"]=u"வௌ"
    table["vai"]=u"வை"
    table["vee"]=u"வே"
    table["voo"]=u"வோ"
    table["vaa"]=u"வா"
    table["vuu"]=u"வூ"
    table["vii"]=u"வீ"
    table["va"]=u"வ"
    table["vi"]=u"வி"
    table["vI"]=u"வீ"
    table["vA"]=u"வா"
    table["ve"]=u"வெ"
    table["vE"]=u"வே"
    table["vo"]=u"வொ"
    table["vO"]=u"வோ"
    table["vu"]=u"வு"
    table["vU"]=u"வூ"
    table["v"]=u"வ்"
    table["gau"]=u"கௌ"
    table["gai"]=u"கை"
    table["gee"]=u"கே"
    table["goo"]=u"கோ"
    table["gaa"]=u"கா"
    table["guu"]=u"கூ"
    table["gii"]=u"கீ"
    table["ga"]=u"க"
    table["gi"]=u"கி"
    table["gI"]=u"கீ"
    table["gA"]=u"கா"
    table["ge"]=u"கெ"
    table["gE"]=u"கே"
    table["go"]=u"கொ"
    table["gO"]=u"கோ"
    table["gu"]=u"கு"
    table["gU"]=u"கூ"
    table["g"]=u"க்"
    table["au"]=u"ஔ"
    table["ai"]=u"ஐ"
    table["aa"]=u"ஆ"
    table["ee"]=u"ஏ"
    table["ii"]=u"ஈ"
    table["uu"]=u"ஊ"
    table["oo"]=u"ஓ"

    # numerals in Tamil
    table["-1000"]=u"௲"
    table["-100"]=u"௱"
    table["-10"]=u"௰"
    table["-1"]=u"௧"
    table["-2"]=u"௨"
    table["-3"]=u"௩"
    table["-4"]=u"௪"
    table["-5"]=u"௫"
    table["-6"]=u"௬"
    table["-7"]=u"௭"
    table["-8"]=u"௮"
    table["-9"]=u"௯"

    # vowels
    table["i"]=u"இ"
    table["I"]=u"ஈ"
    table["a"]=u"அ"
    table["A"]=u"ஆ"
    table["e"]=u"எ"
    table["E"]=u"ஏ"
    table["i"]=u"இ"
    table["I"]=u"ஈ"
    table["u"]=u"உ"
    table["U"]=u"ஊ"
    table["o"]=u"ஒ"
    table["O"]=u"ஓ"
    table["x"]=u"௯"
    table["q"]=u"ஃ"
