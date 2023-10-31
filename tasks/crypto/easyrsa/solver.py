from sympy import Symbol, solve, core
from Crypto.Util.number import long_to_bytes

# Вставляем все переменные
n = 17885706876286606590507011350415163496286911914047587537385347544452525473119208375291827372833974848381079097061586288661500787259325930573967791443676651260374551186601761680972194338287469766293468815752258095072191752219454922094949989071507556050918214617705651152150752309033833878799978225815203076994674258271289495602223107005667958151295974535424076077218896717799185092092956290235938517093844022253417069951507695779221913153846644945011620816966779587077712882735041498785119069945548749270577179526334144514417834441028989204032745023648739411449415376010848717307051311932960210517541305102474195110947
e = 65537
c = 3110059350991185116672224216445552500686706325170861739127656125785007206689106192234164445925123625282834482217104591179127445685236709261778484302335548469428798354834163054981259880695775985484155314401930584091690879899643847572562732540394463015616065494247164351169183655977736827300882302826260145788132273659288837072974423104894119295347439617202185781254204785193452997831439372110451842784828208991213876762803284868202732612884752319124155395500914789185602480792655493405013522284209524073182483744205728958902924529152365359036191835511271183391122508381269955237217464028493155760957435514581478020901
x = 10341484232596658129722048565383542225103838451652526678625553017697579979094716183664072531572766847747667428324550974340827119034233159217918847203494666265996994053473000151783504673634889702935123056125445656374090420638663982890677779519314074436863193361225638325917146287392947401633585565357119530036382838001805517171110485712620070229480139881298220789469608340509472100583468704690017550171769625055624748717714502513373971486106856403802963071514959013868716693349994628220886655364829896448591499245136434392877320090436908333007314402815469536237250304284168112093853100202723469843851835222174011627608

# Решаем вот такую систему
# n = p * q
# x = p**2 - q**2

# Выводим p
# p = n/q

# Подставляем p
# n**2 / q**2 - q**2 - x = 0

# Умножаем весь пример на q**2
# (n**2) / (q**2) - q**2 - x = 0 | * (q**2)
# n**2 - q**4 - x * q**2 = 0

# Задаем переменную, которую нужно будет найти, в данном случае q
q = Symbol('q')

# Записываем уравнение
eq = n**2 - q**4 - x * q**2

# Решаем уравнение для переменной q
solve = solve(eq, q)

# Находим нужный корень уравнения из нескольких корней
# Значение должно быть Integer и больше 0 
for i in solve:
	if isinstance(i, core.numbers.Integer):
		if i > 0:
			q = int(i)

# Вычисляем значение p
p = n // q

# Вычислями f(n)
phi = (p - 1) * (q - 1)

# Вычисляем закрытый ключ
d = pow(e, -1, phi)

# Расшифровываем сообщение
flag = pow(c, d, n)

print(len(str(flag)))
# Выводим флаг
print(long_to_bytes(flag))