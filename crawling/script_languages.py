# encoding: utf-8

# THIS SCRIPT FILLS ALL LANGUAGE ENTRIES IN THE DATABASE

from BeautifulSoup import BeautifulSoup
from cinema.models import *
import re

input = """
<table class="splash">
<tr>
  <td><a href="/language/ar">Arabic</a></td>
  <td><a href="/language/bg">Bulgarian</a></td>
  <td><a href="/language/zh">Chinese</a></td>
  <td><a href="/language/hr">Croatian</a></td>
</tr>
<tr>
  <td><a href="/language/nl">Dutch</a></td>
  <td><a href="/language/en">English</a></td>
  <td><a href="/language/fi">Finnish</a></td>
  <td><a href="/language/fr">French</a></td>
</tr>
<tr>
  <td><a href="/language/de">German</a></td>
  <td><a href="/language/el">Greek</a></td>
  <td><a href="/language/he">Hebrew</a></td>
  <td><a href="/language/hi">Hindi</a></td>
</tr>
<tr>
  <td><a href="/language/hu">Hungarian</a></td>
  <td><a href="/language/is">Icelandic</a></td>
  <td><a href="/language/it">Italian</a></td>
  <td><a href="/language/ja">Japanese</a></td>
</tr>
<tr>
  <td><a href="/language/ko">Korean</a></td>
  <td><a href="/language/no">Norwegian</a></td>
  <td><a href="/language/fa">Persian</a></td>
  <td><a href="/language/pl">Polish</a></td>
</tr>
<tr>
  <td><a href="/language/pt">Portuguese</a></td>
  <td><a href="/language/pa">Punjabi</a></td>
  <td><a href="/language/ro">Romanian</a></td>
  <td><a href="/language/ru">Russian</a></td>
</tr>
<tr>
  <td><a href="/language/es">Spanish</a></td>
  <td><a href="/language/sv">Swedish</a></td>
  <td><a href="/language/tr">Turkish</a></td>
  <td><a href="/language/uk">Ukrainian</a></td>
</tr>
</table>

<h2>Less-Common Languages</h2>



<table class="splash">
<tr>
  <td><a href="/language/ab">Abkhazian</a></td>
  <td><a href="/language/qac">Aboriginal</a></td>
  <td><a href="/language/guq">Aché</a></td>
  <td><a href="/language/qam">Acholi</a></td>
</tr>
<tr>
  <td><a href="/language/af">Afrikaans</a></td>
  <td><a href="/language/qas">Aidoukrou</a></td>
  <td><a href="/language/ak">Akan</a></td>
  <td><a href="/language/sq">Albanian</a></td>
</tr>
<tr>
  <td><a href="/language/alg">Algonquin</a></td>
  <td><a href="/language/ase">American Sign Language</a></td>
  <td><a href="/language/am">Amharic</a></td>
  <td><a href="/language/apa">Apache languages</a></td>
</tr>
<tr>
  <td><a href="/language/an">Aragonese</a></td>
  <td><a href="/language/arc">Aramaic</a></td>
  <td><a href="/language/arp">Arapaho</a></td>
  <td><a href="/language/hy">Armenian</a></td>
</tr>
<tr>
  <td><a href="/language/as">Assamese</a></td>
  <td><a href="/language/aii">Assyrian Neo-Aramaic</a></td>
  <td><a href="/language/ath">Athapascan languages</a></td>
  <td><a href="/language/asf">Australian Sign Language</a></td>
</tr>
<tr>
  <td><a href="/language/awa">Awadhi</a></td>
  <td><a href="/language/ay">Aymara</a></td>
  <td><a href="/language/az">Azerbaijani</a></td>
  <td><a href="/language/ast">Bable</a></td>
</tr>
<tr>
  <td><a href="/language/qbd">Baka</a></td>
  <td><a href="/language/ban">Balinese</a></td>
  <td><a href="/language/bm">Bambara</a></td>
  <td><a href="/language/eu">Basque</a></td>
</tr>
<tr>
  <td><a href="/language/bsc">Bassari</a></td>
  <td><a href="/language/be">Belarusian</a></td>
  <td><a href="/language/bem">Bemba</a></td>
  <td><a href="/language/bn">Bengali</a></td>
</tr>
<tr>
  <td><a href="/language/ber">Berber languages</a></td>
  <td><a href="/language/bho">Bhojpuri</a></td>
  <td><a href="/language/qbi">Bicolano</a></td>
  <td><a href="/language/qbh">Bodo</a></td>
</tr>
<tr>
  <td><a href="/language/bs">Bosnian</a></td>
  <td><a href="/language/bzs">Brazilian Sign Language</a></td>
  <td><a href="/language/br">Breton</a></td>
  <td><a href="/language/bfi">British Sign Language</a></td>
</tr>
<tr>
  <td><a href="/language/my">Burmese</a></td>
  <td><a href="/language/yue">Cantonese</a></td>
  <td><a href="/language/ca">Catalan</a></td>
  <td><a href="/language/km">Central Khmer</a></td>
</tr>
<tr>
  <td><a href="/language/qax">Chaozhou</a></td>
  <td><a href="/language/ce">Chechen</a></td>
  <td><a href="/language/chr">Cherokee</a></td>
  <td><a href="/language/chy">Cheyenne</a></td>
</tr>
<tr>
  <td><a href="/language/hne">Chhattisgarhi</a></td>
  <td><a href="/language/kw">Cornish</a></td>
  <td><a href="/language/co">Corsican</a></td>
  <td><a href="/language/cr">Cree</a></td>
</tr>
<tr>
  <td><a href="/language/mus">Creek</a></td>
  <td><a href="/language/qal">Creole</a></td>
  <td><a href="/language/crp">Creoles and pidgins</a></td>
  <td><a href="/language/cro">Crow</a></td>
</tr>
<tr>
  <td><a href="/language/cs">Czech</a></td>
  <td><a href="/language/da">Danish</a></td>
  <td><a href="/language/prs">Dari</a></td>
  <td><a href="/language/dso">Desiya</a></td>
</tr>
<tr>
  <td><a href="/language/din">Dinka</a></td>
  <td><a href="/language/qaw">Djerma</a></td>
  <td><a href="/language/doi">Dogri</a></td>
  <td><a href="/language/dyu">Dyula</a></td>
</tr>
<tr>
  <td><a href="/language/dz">Dzongkha</a></td>
  <td><a href="/language/qbc">East-Greenlandic</a></td>
  <td><a href="/language/frs">Eastern Frisian</a></td>
  <td><a href="/language/egy">Egyptian (Ancient)</a></td>
</tr>
<tr>
  <td><a href="/language/eo">Esperanto</a></td>
  <td><a href="/language/et">Estonian</a></td>
  <td><a href="/language/ee">Ewe</a></td>
  <td><a href="/language/qbg">Faliasch</a></td>
</tr>
<tr>
  <td><a href="/language/fo">Faroese</a></td>
  <td><a href="/language/fil">Filipino</a></td>
  <td><a href="/language/qbn">Flemish</a></td>
  <td><a href="/language/fon">Fon</a></td>
</tr>
<tr>
  <td><a href="/language/fsl">French Sign Language</a></td>
  <td><a href="/language/ff">Fulah</a></td>
  <td><a href="/language/fvr">Fur</a></td>
  <td><a href="/language/gd">Gaelic</a></td>
</tr>
<tr>
  <td><a href="/language/gl">Galician</a></td>
  <td><a href="/language/ka">Georgian</a></td>
  <td><a href="/language/gsg">German Sign Language</a></td>
  <td><a href="/language/grb">Grebo</a></td>
</tr>
<tr>
  <td><a href="/language/grc">Greek, Ancient (to 1453)</a></td>
  <td><a href="/language/kl">Greenlandic</a></td>
  <td><a href="/language/gn">Guarani</a></td>
  <td><a href="/language/gu">Gujarati</a></td>
</tr>
<tr>
  <td><a href="/language/gnn">Gumatj</a></td>
  <td><a href="/language/gup">Gunwinggu</a></td>
  <td><a href="/language/ht">Haitian</a></td>
  <td><a href="/language/hak">Hakka</a></td>
</tr>
<tr>
  <td><a href="/language/bgc">Haryanvi</a></td>
  <td><a href="/language/qav">Hassanya</a></td>
  <td><a href="/language/ha">Hausa</a></td>
  <td><a href="/language/haw">Hawaiian</a></td>
</tr>
<tr>
  <td><a href="/language/hmn">Hmong</a></td>
  <td><a href="/language/qab">Hokkien</a></td>
  <td><a href="/language/hop">Hopi</a></td>
  <td><a href="/language/iba">Iban</a></td>
</tr>
<tr>
  <td><a href="/language/qag">Ibo</a></td>
  <td><a href="/language/icl">Icelandic Sign Language</a></td>
  <td><a href="/language/ins">Indian Sign Language</a></td>
  <td><a href="/language/id">Indonesian</a></td>
</tr>
<tr>
  <td><a href="/language/iu">Inuktitut</a></td>
  <td><a href="/language/ik">Inupiaq</a></td>
  <td><a href="/language/ga">Irish Gaelic</a></td>
  <td><a href="/language/jsl">Japanese Sign Language</a></td>
</tr>
<tr>
  <td><a href="/language/dyo">Jola-Fonyi</a></td>
  <td><a href="/language/ktz">Ju'hoan</a></td>
  <td><a href="/language/qbf">Kaado</a></td>
  <td><a href="/language/kea">Kabuverdianu</a></td>
</tr>
<tr>
  <td><a href="/language/kab">Kabyle</a></td>
  <td><a href="/language/xal">Kalmyk-Oirat</a></td>
  <td><a href="/language/kn">Kannada</a></td>
  <td><a href="/language/kpj">Karajá</a></td>
</tr>
<tr>
  <td><a href="/language/mjw">Karbi</a></td>
  <td><a href="/language/kar">Karen</a></td>
  <td><a href="/language/kk">Kazakh</a></td>
  <td><a href="/language/kca">Khanty</a></td>
</tr>
<tr>
  <td><a href="/language/kha">Khasi</a></td>
  <td><a href="/language/ki">Kikuyu</a></td>
  <td><a href="/language/rw">Kinyarwanda</a></td>
  <td><a href="/language/qar">Kirundi</a></td>
</tr>
<tr>
  <td><a href="/language/tlh">Klingon</a></td>
  <td><a href="/language/kfa">Kodava</a></td>
  <td><a href="/language/kok">Konkani</a></td>
  <td><a href="/language/kvk">Korean Sign Language</a></td>
</tr>
<tr>
  <td><a href="/language/khe">Korowai</a></td>
  <td><a href="/language/qaq">Kriolu</a></td>
  <td><a href="/language/kro">Kru</a></td>
  <td><a href="/language/kyw">Kudmali</a></td>
</tr>
<tr>
  <td><a href="/language/qbb">Kuna</a></td>
  <td><a href="/language/ku">Kurdish</a></td>
  <td><a href="/language/kwk">Kwakiutl</a></td>
  <td><a href="/language/ky">Kyrgyz</a></td>
</tr>
<tr>
  <td><a href="/language/lbj">Ladakhi</a></td>
  <td><a href="/language/lad">Ladino</a></td>
  <td><a href="/language/lo">Lao</a></td>
  <td><a href="/language/la">Latin</a></td>
</tr>
<tr>
  <td><a href="/language/lv">Latvian</a></td>
  <td><a href="/language/lif">Limbu</a></td>
  <td><a href="/language/ln">Lingala</a></td>
  <td><a href="/language/lt">Lithuanian</a></td>
</tr>
<tr>
  <td><a href="/language/nds">Low German</a></td>
  <td><a href="/language/lb">Luxembourgish</a></td>
  <td><a href="/language/mk">Macedonian</a></td>
  <td><a href="/language/qbm">Macro-Jê</a></td>
</tr>
<tr>
  <td><a href="/language/mag">Magahi</a></td>
  <td><a href="/language/mai">Maithili</a></td>
  <td><a href="/language/mg">Malagasy</a></td>
  <td><a href="/language/ms">Malay</a></td>
</tr>
<tr>
  <td><a href="/language/ml">Malayalam</a></td>
  <td><a href="/language/pqm">Malecite-Passamaquoddy</a></td>
  <td><a href="/language/qap">Malinka</a></td>
  <td><a href="/language/mt">Maltese</a></td>
</tr>
<tr>
  <td><a href="/language/mnc">Manchu</a></td>
  <td><a href="/language/cmn">Mandarin</a></td>
  <td><a href="/language/man">Mandingo</a></td>
  <td><a href="/language/mni">Manipuri</a></td>
</tr>
<tr>
  <td><a href="/language/mi">Maori</a></td>
  <td><a href="/language/arn">Mapudungun</a></td>
  <td><a href="/language/mr">Marathi</a></td>
  <td><a href="/language/mh">Marshallese</a></td>
</tr>
<tr>
  <td><a href="/language/mas">Masai</a></td>
  <td><a href="/language/mls">Masalit</a></td>
  <td><a href="/language/myn">Maya</a></td>
  <td><a href="/language/men">Mende</a></td>
</tr>
<tr>
  <td><a href="/language/mic">Micmac</a></td>
  <td><a href="/language/enm">Middle English</a></td>
  <td><a href="/language/nan">Min Nan</a></td>
  <td><a href="/language/min">Minangkabau</a></td>
</tr>
<tr>
  <td><a href="/language/mwl">Mirandese</a></td>
  <td><a href="/language/lus">Mizo</a></td>
  <td><a href="/language/moh">Mohawk</a></td>
  <td><a href="/language/mn">Mongolian</a></td>
</tr>
<tr>
  <td><a href="/language/moe">Montagnais</a></td>
  <td><a href="/language/qaf">More</a></td>
  <td><a href="/language/mfe">Morisyen</a></td>
  <td><a href="/language/qbl">Nagpuri</a></td>
</tr>
<tr>
  <td><a href="/language/nah">Nahuatl</a></td>
  <td><a href="/language/qba">Nama</a></td>
  <td><a href="/language/nv">Navajo</a></td>
  <td><a href="/language/nbf">Naxi</a></td>
</tr>
<tr>
  <td><a href="/language/nd">Ndebele</a></td>
  <td><a href="/language/nap">Neapolitan</a></td>
  <td><a href="/language/yrk">Nenets</a></td>
  <td><a href="/language/ne">Nepali</a></td>
</tr>
<tr>
  <td><a href="/language/ncg">Nisga'a</a></td>
  <td><a href="/language/zxx">None</a></td>
  <td><a href="/language/non">Norse, Old</a></td>
  <td><a href="/language/nai">North American Indian</a></td>
</tr>
<tr>
  <td><a href="/language/qbk">Nushi</a></td>
  <td><a href="/language/nyk">Nyaneka</a></td>
  <td><a href="/language/ny">Nyanja</a></td>
  <td><a href="/language/oc">Occitan</a></td>
</tr>
<tr>
  <td><a href="/language/oj">Ojibwa</a></td>
  <td><a href="/language/qaz">Ojihimba</a></td>
  <td><a href="/language/ang">Old English</a></td>
  <td><a href="/language/or">Oriya</a></td>
</tr>
<tr>
  <td><a href="/language/pap">Papiamento</a></td>
  <td><a href="/language/qaj">Parsee</a></td>
  <td><a href="/language/ps">Pashtu</a></td>
  <td><a href="/language/paw">Pawnee</a></td>
</tr>
<tr>
  <td><a href="/language/qai">Peul</a></td>
  <td><a href="/language/qah">Polynesian</a></td>
  <td><a href="/language/fuf">Pular</a></td>
  <td><a href="/language/tsz">Purepecha</a></td>
</tr>
<tr>
  <td><a href="/language/qu">Quechua</a></td>
  <td><a href="/language/qya">Quenya</a></td>
  <td><a href="/language/raj">Rajasthani</a></td>
  <td><a href="/language/qbj">Rawan</a></td>
</tr>
<tr>
  <td><a href="/language/rm">Romansh</a></td>
  <td><a href="/language/rom">Romany</a></td>
  <td><a href="/language/rtm">Rotuman</a></td>
  <td><a href="/language/rsl">Russian Sign Language</a></td>
</tr>
<tr>
  <td><a href="/language/qao">Ryukyuan</a></td>
  <td><a href="/language/qae">Saami</a></td>
  <td><a href="/language/sm">Samoan</a></td>
  <td><a href="/language/sa">Sanskrit</a></td>
</tr>
<tr>
  <td><a href="/language/sc">Sardinian</a></td>
  <td><a href="/language/qay">Scanian</a></td>
  <td><a href="/language/sr">Serbian</a></td>
  <td><a href="/language/qbo">Serbo-Croatian</a></td>
</tr>
<tr>
  <td><a href="/language/srr">Serer</a></td>
  <td><a href="/language/qad">Shanghainese</a></td>
  <td><a href="/language/qau">Shanxi</a></td>
  <td><a href="/language/sn">Shona</a></td>
</tr>
<tr>
  <td><a href="/language/shh">Shoshoni</a></td>
  <td><a href="/language/scn">Sicilian</a></td>
  <td><a href="/language/sjn">Sindarin</a></td>
  <td><a href="/language/sd">Sindhi</a></td>
</tr>
<tr>
  <td><a href="/language/si">Sinhala</a></td>
  <td><a href="/language/sio">Sioux</a></td>
  <td><a href="/language/sk">Slovak</a></td>
  <td><a href="/language/sl">Slovenian</a></td>
</tr>
<tr>
  <td><a href="/language/so">Somali</a></td>
  <td><a href="/language/son">Songhay</a></td>
  <td><a href="/language/snk">Soninke</a></td>
  <td><a href="/language/wen">Sorbian languages</a></td>
</tr>
<tr>
  <td><a href="/language/st">Sotho</a></td>
  <td><a href="/language/qbe">Sousson</a></td>
  <td><a href="/language/ssp">Spanish Sign Language</a></td>
  <td><a href="/language/srn">Sranan</a></td>
</tr>
<tr>
  <td><a href="/language/sw">Swahili</a></td>
  <td><a href="/language/gsw">Swiss German</a></td>
  <td><a href="/language/syl">Sylheti</a></td>
  <td><a href="/language/tl">Tagalog</a></td>
</tr>
<tr>
  <td><a href="/language/tg">Tajik</a></td>
  <td><a href="/language/tmh">Tamashek</a></td>
  <td><a href="/language/ta">Tamil</a></td>
  <td><a href="/language/tac">Tarahumara</a></td>
</tr>
<tr>
  <td><a href="/language/tt">Tatar</a></td>
  <td><a href="/language/te">Telugu</a></td>
  <td><a href="/language/qak">Teochew</a></td>
  <td><a href="/language/th">Thai</a></td>
</tr>
<tr>
  <td><a href="/language/bo">Tibetan</a></td>
  <td><a href="/language/qan">Tigrigna</a></td>
  <td><a href="/language/tli">Tlingit</a></td>
  <td><a href="/language/tpi">Tok Pisin</a></td>
</tr>
<tr>
  <td><a href="/language/to">Tonga (Tonga Islands)</a></td>
  <td><a href="/language/ts">Tsonga</a></td>
  <td><a href="/language/tsc">Tswa</a></td>
  <td><a href="/language/tn">Tswana</a></td>
</tr>
<tr>
  <td><a href="/language/tcy">Tulu</a></td>
  <td><a href="/language/tup">Tupi</a></td>
  <td><a href="/language/tk">Turkmen</a></td>
  <td><a href="/language/tyv">Tuvinian</a></td>
</tr>
<tr>
  <td><a href="/language/tzo">Tzotzil</a></td>
  <td><a href="/language/qat">Ungwatsi</a></td>
  <td><a href="/language/ur">Urdu</a></td>
  <td><a href="/language/uz">Uzbek</a></td>
</tr>
<tr>
  <td><a href="/language/vi">Vietnamese</a></td>
  <td><a href="/language/qaa">Visayan</a></td>
  <td><a href="/language/was">Washoe</a></td>
  <td><a href="/language/cy">Welsh</a></td>
</tr>
<tr>
  <td><a href="/language/wo">Wolof</a></td>
  <td><a href="/language/xh">Xhosa</a></td>
  <td><a href="/language/sah">Yakut</a></td>
  <td><a href="/language/yap">Yapese</a></td>
</tr>
<tr>
  <td><a href="/language/yi">Yiddish</a></td>
  <td><a href="/language/yo">Yoruba</a></td>
  <td><a href="/language/zu">Zulu</a></td>
</table>
"""

soup = BeautifulSoup(input)
countries = []
tables = soup.findAll('table')
for table in tables:
    trs = soup.findAll('tr')
    for tr in trs:
        all_a = tr.findAll('a')
        for item in all_a:
            name = item.string
            url = item['href']
            country = [name,url[10:]]
            countries.append(country)

for country in countries:
    Language.objects.create(name=country[0], identifier=country[1])
