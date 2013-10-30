# encoding: utf-8

# THIS SCRIPT FILLS ALL COUNTRY ENTRIES IN THE DATABASE

from BeautifulSoup import BeautifulSoup
from cinema.models import *
import re

input = """
<h2>Common Countries</h2>

<table class="splash">
<tr>
  <td><a href="/country/ar">Argentina
</a></td>
  <td><a href="/country/au">Australia
</a></td>
  <td><a href="/country/at">Austria
</a></td>
  <td><a href="/country/be">Belgium
</a></td>
</tr>
<tr>
  <td><a href="/country/br">Brazil
</a></td>
  <td><a href="/country/bg">Bulgaria
</a></td>
  <td><a href="/country/ca">Canada
</a></td>
  <td><a href="/country/cn">China
</a></td>
</tr>
<tr>
  <td><a href="/country/co">Colombia
</a></td>
  <td><a href="/country/cr">Costa Rica
</a></td>
  <td><a href="/country/cz">Czech Republic
</a></td>
  <td><a href="/country/dk">Denmark
</a></td>
</tr>
<tr>
  <td><a href="/country/fi">Finland
</a></td>
  <td><a href="/country/fr">France
</a></td>
  <td><a href="/country/de">Germany
</a></td>
  <td><a href="/country/gr">Greece
</a></td>
</tr>
<tr>
  <td><a href="/country/hk">Hong Kong
</a></td>
  <td><a href="/country/hu">Hungary
</a></td>
  <td><a href="/country/is">Iceland
</a></td>
  <td><a href="/country/in">India
</a></td>
</tr>
<tr>
  <td><a href="/country/ir">Iran
</a></td>
  <td><a href="/country/ie">Ireland
</a></td>
  <td><a href="/country/it">Italy
</a></td>
  <td><a href="/country/jp">Japan
</a></td>
</tr>
<tr>
  <td><a href="/country/my">Malaysia
</a></td>
  <td><a href="/country/mx">Mexico
</a></td>
  <td><a href="/country/nl">Netherlands
</a></td>
  <td><a href="/country/nz">New Zealand
</a></td>
</tr>
<tr>
  <td><a href="/country/pk">Pakistan
</a></td>
  <td><a href="/country/pl">Poland
</a></td>
  <td><a href="/country/pt">Portugal
</a></td>
  <td><a href="/country/ro">Romania
</a></td>
</tr>
<tr>
  <td><a href="/country/ru">Russia
</a></td>
  <td><a href="/country/sg">Singapore
</a></td>
  <td><a href="/country/za">South Africa
</a></td>
  <td><a href="/country/es">Spain
</a></td>
</tr>
<tr>
  <td><a href="/country/se">Sweden
</a></td>
  <td><a href="/country/ch">Switzerland
</a></td>
  <td><a href="/country/th">Thailand
</a></td>
  <td><a href="/country/gb">United Kingdom
</a></td>
</tr>
<tr>
  <td><a href="/country/us">United States
</a></td>
</table>

<h2>Less-Common Countries</h2>



<table class="splash">
<tr>
  <td><a href="/country/af">Afghanistan
</a></td>
  <td><a href="/country/ax">Åland Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/al">Albania
</a></td>
  <td><a href="/country/dz">Algeria
</a></td>
</tr>
<tr>
  <td><a href="/country/as">American Samoa
</a></td>
  <td><a href="/country/ad">Andorra
</a></td>
</tr>
<tr>
  <td><a href="/country/ao">Angola
</a></td>
  <td><a href="/country/ai">Anguilla
</a></td>
</tr>
<tr>
  <td><a href="/country/aq">Antarctica
</a></td>
  <td><a href="/country/ag">Antigua and Barbuda
</a></td>
</tr>
<tr>
  <td><a href="/country/am">Armenia
</a></td>
  <td><a href="/country/aw">Aruba
</a></td>
</tr>
<tr>
  <td><a href="/country/az">Azerbaijan
</a></td>
  <td><a href="/country/bs">Bahamas
</a></td>
</tr>
<tr>
  <td><a href="/country/bh">Bahrain
</a></td>
  <td><a href="/country/bd">Bangladesh
</a></td>
</tr>
<tr>
  <td><a href="/country/bb">Barbados
</a></td>
  <td><a href="/country/by">Belarus
</a></td>
</tr>
<tr>
  <td><a href="/country/bz">Belize
</a></td>
  <td><a href="/country/bj">Benin
</a></td>
</tr>
<tr>
  <td><a href="/country/bm">Bermuda
</a></td>
  <td><a href="/country/bt">Bhutan
</a></td>
</tr>
<tr>
  <td><a href="/country/bo">Bolivia
</a></td>
  <td><a href="/country/ba">Bosnia and Herzegovina
</a></td>
</tr>
<tr>
  <td><a href="/country/bw">Botswana
</a></td>
  <td><a href="/country/bv">Bouvet Island
</a></td>
</tr>
<tr>
  <td><a href="/country/io">British Indian Ocean Territory
</a></td>
  <td><a href="/country/vg">British Virgin Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/bn">Brunei Darussalam
</a></td>
  <td><a href="/country/bf">Burkina Faso
</a></td>
</tr>
<tr>
  <td><a href="/country/bumm">Burma
</a></td>
  <td><a href="/country/bi">Burundi
</a></td>
</tr>
<tr>
  <td><a href="/country/kh">Cambodia
</a></td>
  <td><a href="/country/cm">Cameroon
</a></td>
</tr>
<tr>
  <td><a href="/country/cv">Cape Verde
</a></td>
  <td><a href="/country/ky">Cayman Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/cf">Central African Republic
</a></td>
  <td><a href="/country/td">Chad
</a></td>
</tr>
<tr>
  <td><a href="/country/cl">Chile
</a></td>
  <td><a href="/country/cx">Christmas Island
</a></td>
</tr>
<tr>
  <td><a href="/country/cc">Cocos (Keeling) Islands
</a></td>
  <td><a href="/country/km">Comoros
</a></td>
</tr>
<tr>
  <td><a href="/country/cg">Congo
</a></td>
  <td><a href="/country/ck">Cook Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/ci">Côte d'Ivoire
</a></td>
  <td><a href="/country/hr">Croatia
</a></td>
</tr>
<tr>
  <td><a href="/country/cu">Cuba
</a></td>
  <td><a href="/country/cy">Cyprus
</a></td>
</tr>
<tr>
  <td><a href="/country/cshh">Czechoslovakia
</a></td>
  <td><a href="/country/cd">Democratic Republic of the Congo
</a></td>
</tr>
<tr>
  <td><a href="/country/dj">Djibouti
</a></td>
  <td><a href="/country/dm">Dominica
</a></td>
</tr>
<tr>
  <td><a href="/country/do">Dominican Republic
</a></td>
  <td><a href="/country/ddde">East Germany
</a></td>
</tr>
<tr>
  <td><a href="/country/ec">Ecuador
</a></td>
  <td><a href="/country/eg">Egypt
</a></td>
</tr>
<tr>
  <td><a href="/country/sv">El Salvador
</a></td>
  <td><a href="/country/gq">Equatorial Guinea
</a></td>
</tr>
<tr>
  <td><a href="/country/er">Eritrea
</a></td>
  <td><a href="/country/ee">Estonia
</a></td>
</tr>
<tr>
  <td><a href="/country/et">Ethiopia
</a></td>
  <td><a href="/country/fk">Falkland Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/fo">Faroe Islands
</a></td>
  <td><a href="/country/yucs">Federal Republic of Yugoslavia
</a></td>
</tr>
<tr>
  <td><a href="/country/fm">Federated States of Micronesia
</a></td>
  <td><a href="/country/fj">Fiji
</a></td>
</tr>
<tr>
  <td><a href="/country/gf">French Guiana
</a></td>
  <td><a href="/country/pf">French Polynesia
</a></td>
</tr>
<tr>
  <td><a href="/country/tf">French Southern Territories
</a></td>
  <td><a href="/country/ga">Gabon
</a></td>
</tr>
<tr>
  <td><a href="/country/gm">Gambia
</a></td>
  <td><a href="/country/ge">Georgia
</a></td>
</tr>
<tr>
  <td><a href="/country/gh">Ghana
</a></td>
  <td><a href="/country/gi">Gibraltar
</a></td>
</tr>
<tr>
  <td><a href="/country/gl">Greenland
</a></td>
  <td><a href="/country/gd">Grenada
</a></td>
</tr>
<tr>
  <td><a href="/country/gp">Guadeloupe
</a></td>
  <td><a href="/country/gu">Guam
</a></td>
</tr>
<tr>
  <td><a href="/country/gt">Guatemala
</a></td>
  <td><a href="/country/gg">Guernsey
</a></td>
</tr>
<tr>
  <td><a href="/country/gn">Guinea
</a></td>
  <td><a href="/country/gw">Guinea-Bissau
</a></td>
</tr>
<tr>
  <td><a href="/country/gy">Guyana
</a></td>
  <td><a href="/country/ht">Haiti
</a></td>
</tr>
<tr>
  <td><a href="/country/hm">Heard Island and McDonald Islands
</a></td>
  <td><a href="/country/va">Holy See (Vatican City State)
</a></td>
</tr>
<tr>
  <td><a href="/country/hn">Honduras
</a></td>
  <td><a href="/country/id">Indonesia
</a></td>
</tr>
<tr>
  <td><a href="/country/iq">Iraq
</a></td>
  <td><a href="/country/im">Isle of Man
</a></td>
</tr>
<tr>
  <td><a href="/country/il">Israel
</a></td>
  <td><a href="/country/jm">Jamaica
</a></td>
</tr>
<tr>
  <td><a href="/country/je">Jersey
</a></td>
  <td><a href="/country/jo">Jordan
</a></td>
</tr>
<tr>
  <td><a href="/country/kz">Kazakhstan
</a></td>
  <td><a href="/country/ke">Kenya
</a></td>
</tr>
<tr>
  <td><a href="/country/ki">Kiribati
</a></td>
  <td><a href="/country/xko">Korea
</a></td>
</tr>
<tr>
  <td><a href="/country/xkv">Kosovo
</a></td>
  <td><a href="/country/kw">Kuwait
</a></td>
</tr>
<tr>
  <td><a href="/country/kg">Kyrgyzstan
</a></td>
  <td><a href="/country/la">Laos
</a></td>
</tr>
<tr>
  <td><a href="/country/lv">Latvia
</a></td>
  <td><a href="/country/lb">Lebanon
</a></td>
</tr>
<tr>
  <td><a href="/country/ls">Lesotho
</a></td>
  <td><a href="/country/lr">Liberia
</a></td>
</tr>
<tr>
  <td><a href="/country/ly">Libya
</a></td>
  <td><a href="/country/li">Liechtenstein
</a></td>
</tr>
<tr>
  <td><a href="/country/lt">Lithuania
</a></td>
  <td><a href="/country/lu">Luxembourg
</a></td>
</tr>
<tr>
  <td><a href="/country/mo">Macao
</a></td>
  <td><a href="/country/mg">Madagascar
</a></td>
</tr>
<tr>
  <td><a href="/country/mw">Malawi
</a></td>
  <td><a href="/country/mv">Maldives
</a></td>
</tr>
<tr>
  <td><a href="/country/ml">Mali
</a></td>
  <td><a href="/country/mt">Malta
</a></td>
</tr>
<tr>
  <td><a href="/country/mh">Marshall Islands
</a></td>
  <td><a href="/country/mq">Martinique
</a></td>
</tr>
<tr>
  <td><a href="/country/mr">Mauritania
</a></td>
  <td><a href="/country/mu">Mauritius
</a></td>
</tr>
<tr>
  <td><a href="/country/yt">Mayotte
</a></td>
  <td><a href="/country/md">Moldova
</a></td>
</tr>
<tr>
  <td><a href="/country/mc">Monaco
</a></td>
  <td><a href="/country/mn">Mongolia
</a></td>
</tr>
<tr>
  <td><a href="/country/me">Montenegro
</a></td>
  <td><a href="/country/ms">Montserrat
</a></td>
</tr>
<tr>
  <td><a href="/country/ma">Morocco
</a></td>
  <td><a href="/country/mz">Mozambique
</a></td>
</tr>
<tr>
  <td><a href="/country/mm">Myanmar
</a></td>
  <td><a href="/country/na">Namibia
</a></td>
</tr>
<tr>
  <td><a href="/country/nr">Nauru
</a></td>
  <td><a href="/country/np">Nepal
</a></td>
</tr>
<tr>
  <td><a href="/country/an">Netherlands Antilles
</a></td>
  <td><a href="/country/nc">New Caledonia
</a></td>
</tr>
<tr>
  <td><a href="/country/ni">Nicaragua
</a></td>
  <td><a href="/country/ne">Niger
</a></td>
</tr>
<tr>
  <td><a href="/country/ng">Nigeria
</a></td>
  <td><a href="/country/nu">Niue
</a></td>
</tr>
<tr>
  <td><a href="/country/nf">Norfolk Island
</a></td>
  <td><a href="/country/kp">North Korea
</a></td>
</tr>
<tr>
  <td><a href="/country/vdvn">North Vietnam
</a></td>
  <td><a href="/country/mp">Northern Mariana Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/no">Norway
</a></td>
  <td><a href="/country/om">Oman
</a></td>
</tr>
<tr>
  <td><a href="/country/pw">Palau
</a></td>
  <td><a href="/country/xpi">Palestine
</a></td>
</tr>
<tr>
  <td><a href="/country/ps">Palestinian Territory
</a></td>
  <td><a href="/country/pa">Panama
</a></td>
</tr>
<tr>
  <td><a href="/country/pg">Papua New Guinea
</a></td>
  <td><a href="/country/py">Paraguay
</a></td>
</tr>
<tr>
  <td><a href="/country/pe">Peru
</a></td>
  <td><a href="/country/ph">Philippines
</a></td>
</tr>
<tr>
  <td><a href="/country/pn">Pitcairn
</a></td>
  <td><a href="/country/pr">Puerto Rico
</a></td>
</tr>
<tr>
  <td><a href="/country/qa">Qatar
</a></td>
  <td><a href="/country/mk">Republic of Macedonia
</a></td>
</tr>
<tr>
  <td><a href="/country/re">Réunion
</a></td>
  <td><a href="/country/rw">Rwanda
</a></td>
</tr>
<tr>
  <td><a href="/country/bl">Saint Barthélemy
</a></td>
  <td><a href="/country/sh">Saint Helena
</a></td>
</tr>
<tr>
  <td><a href="/country/kn">Saint Kitts and Nevis
</a></td>
  <td><a href="/country/lc">Saint Lucia
</a></td>
</tr>
<tr>
  <td><a href="/country/mf">Saint Martin (French part)
</a></td>
  <td><a href="/country/pm">Saint Pierre and Miquelon
</a></td>
</tr>
<tr>
  <td><a href="/country/vc">Saint Vincent and the Grenadines
</a></td>
  <td><a href="/country/ws">Samoa
</a></td>
</tr>
<tr>
  <td><a href="/country/sm">San Marino
</a></td>
  <td><a href="/country/st">Sao Tome and Principe
</a></td>
</tr>
<tr>
  <td><a href="/country/sa">Saudi Arabia
</a></td>
  <td><a href="/country/sn">Senegal
</a></td>
</tr>
<tr>
  <td><a href="/country/rs">Serbia
</a></td>
  <td><a href="/country/csxx">Serbia and Montenegro
</a></td>
</tr>
<tr>
  <td><a href="/country/sc">Seychelles
</a></td>
  <td><a href="/country/xsi">Siam
</a></td>
</tr>
<tr>
  <td><a href="/country/sl">Sierra Leone
</a></td>
  <td><a href="/country/sk">Slovakia
</a></td>
</tr>
<tr>
  <td><a href="/country/si">Slovenia
</a></td>
  <td><a href="/country/sb">Solomon Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/so">Somalia
</a></td>
  <td><a href="/country/gs">South Georgia and the South Sandwich Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/kr">South Korea
</a></td>
  <td><a href="/country/suhh">Soviet Union
</a></td>
</tr>
<tr>
  <td><a href="/country/lk">Sri Lanka
</a></td>
  <td><a href="/country/sd">Sudan
</a></td>
</tr>
<tr>
  <td><a href="/country/sr">Suriname
</a></td>
  <td><a href="/country/sj">Svalbard and Jan Mayen
</a></td>
</tr>
<tr>
  <td><a href="/country/sz">Swaziland
</a></td>
  <td><a href="/country/sy">Syria
</a></td>
</tr>
<tr>
  <td><a href="/country/tw">Taiwan
</a></td>
  <td><a href="/country/tj">Tajikistan
</a></td>
</tr>
<tr>
  <td><a href="/country/tz">Tanzania
</a></td>
  <td><a href="/country/tl">Timor-Leste
</a></td>
</tr>
<tr>
  <td><a href="/country/tg">Togo
</a></td>
  <td><a href="/country/tk">Tokelau
</a></td>
</tr>
<tr>
  <td><a href="/country/to">Tonga
</a></td>
  <td><a href="/country/tt">Trinidad and Tobago
</a></td>
</tr>
<tr>
  <td><a href="/country/tn">Tunisia
</a></td>
  <td><a href="/country/tr">Turkey
</a></td>
</tr>
<tr>
  <td><a href="/country/tm">Turkmenistan
</a></td>
  <td><a href="/country/tc">Turks and Caicos Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/tv">Tuvalu
</a></td>
  <td><a href="/country/vi">U.S. Virgin Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/ug">Uganda
</a></td>
  <td><a href="/country/ua">Ukraine
</a></td>
</tr>
<tr>
  <td><a href="/country/ae">United Arab Emirates
</a></td>
  <td><a href="/country/um">United States Minor Outlying Islands
</a></td>
</tr>
<tr>
  <td><a href="/country/uy">Uruguay
</a></td>
  <td><a href="/country/uz">Uzbekistan
</a></td>
</tr>
<tr>
  <td><a href="/country/vu">Vanuatu
</a></td>
  <td><a href="/country/ve">Venezuela
</a></td>
</tr>
<tr>
  <td><a href="/country/vn">Vietnam
</a></td>
  <td><a href="/country/wf">Wallis and Futuna
</a></td>
</tr>
<tr>
  <td><a href="/country/xwg">West Germany
</a></td>
  <td><a href="/country/eh">Western Sahara
</a></td>
</tr>
<tr>
  <td><a href="/country/ye">Yemen
</a></td>
  <td><a href="/country/xyu">Yugoslavia
</a></td>
</tr>
<tr>
  <td><a href="/country/zrcd">Zaire
</a></td>
  <td><a href="/country/zm">Zambia
</a></td>
</tr>
<tr>
  <td><a href="/country/zw">Zimbabwe
</a></td>
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
            country = [name[:-1],url[9:]]
            countries.append(country)

for country in countries:
    Country.objects.create(name=country[0], identifier=country[1])
