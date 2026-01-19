#pokemon

class Mon:
    def __init__(self, name, type, type2 , hp, at, de, sp_at, sp_de, spd,):
        self.name = name
        self.type = type
        self.type2 = type2
        self.hp = hp
        self.at = at   
        self.de = de
        self.sp_at = sp_at   
        self.sp_de = sp_de
        self.spd = spd


    def call(self):
        return f"{self.name}"
    
#ok so the stats 
mon1=Mon("""bulbasaur""","""grass""","""poison""",45,49,49,65,65,45)
mon2=Mon("""ivysaur""","""grass""","""poison""",60,62,63,80,80,60)
mon3=Mon("""venusaur""","""grass""","""poison""",80,82,83,100,100,80)
mon4=Mon("""charmander""","""fire""","nil",39,52,43,60,50,65)
mon5=Mon("""charmeleon""","""fire""","nil",58,64,58,80,65,80)
mon6=Mon("""charizard""","""fire""","""flying""",78,84,78,109,85,100)
mon7=Mon("""squirtle""","""water""","nil",44,48,65,50,64,43)
mon8=Mon("""wartortle""","""water""","nil",59,63,80,65,80,58)
mon9=Mon("""blastoise""","""water""","nil",79,83,100,85,105,78)
mon10=Mon("""caterpie""","""bug""","nil",45,30,35,20,20,45)
mon11=Mon("""metapod""","""bug""","nil",50,20,55,25,25,30)
mon12=Mon("""butterfree""","""bug""","""flying""",60,45,50,90,80,70)
mon13=Mon("""weedle""","""bug""","""poison""",40,35,30,20,20,50)
mon14=Mon("""kakuna""","""bug""","""poison""",45,25,50,25,25,35)
mon15=Mon("""beedrill""","""bug""","""poison""",65,90,40,45,80,75)
mon16=Mon("""pidgey""","""normal""","""flying""",40,45,40,35,35,56)
mon17=Mon("""pidgeotto""","""normal""","""flying""",63,60,55,50,50,71)
mon18=Mon("""pidgeot""","""normal""","""flying""",83,80,75,70,70,101)
mon19=Mon("""rattata""","""normal""","nil",30,56,35,25,35,72)
mon20=Mon("""raticate""","""normal""","nil",55,81,60,50,70,97)
mon21=Mon("""spearow""","""normal""","""flying""",40,60,30,31,31,70)
mon22=Mon("""fearow""","""normal""","""flying""",65,90,65,61,61,100)
mon23=Mon("""ekans""","""poison""","nil",35,60,44,40,54,55)
mon24=Mon("""arbok""","""poison""","nil",60,95,69,65,79,80)
mon25=Mon("""pikachu""","""electric""","nil",35,55,40,50,50,90)
mon26=Mon("""raichu""","""electric""","nil",60,90,55,90,80,110)
mon27=Mon("""sandshrew""","""ground""","nil",50,75,85,20,30,40)
mon28=Mon("""sandslash""","""ground""","nil",75,100,110,45,55,65)
mon29=Mon("""nidoran-f""","""poison""","nil",55,47,52,40,40,41)
mon30=Mon("""nidorina""","""poison""","nil",70,62,67,55,55,56)
mon31=Mon("""nidoqueen""","""poison""","""ground""",90,92,87,75,85,76)
mon32=Mon("""nidoran-m""","""poison""","nil",46,57,40,40,40,50)
mon33=Mon("""nidorino""","""poison""","nil",61,72,57,55,55,65)
mon34=Mon("""nidoking""","""poison""","""ground""",81,102,77,85,75,85)
mon35=Mon("""clefairy""","""fairy""","nil",70,45,48,60,65,35)
mon36=Mon("""clefable""","""fairy""","nil",95,70,73,95,90,60)
mon37=Mon("""vulpix""","""fire""","nil",38,41,40,50,65,65)
mon38=Mon("""ninetales""","""fire""","nil",73,76,75,81,100,100)
mon39=Mon("""jigglypuff""","""normal""","""fairy""",115,45,20,45,25,20)
mon40=Mon("""wigglytuff""","""normal""","""fairy""",140,70,45,85,50,45)
mon41=Mon("""zubat""","""poison""","""flying""",40,45,35,30,40,55)
mon42=Mon("""golbat""","""poison""","""flying""",75,80,70,65,75,90)
mon43=Mon("""oddish""","""grass""","""poison""",45,50,55,75,65,30)
mon44=Mon("""gloom""","""grass""","""poison""",60,65,70,85,75,40)
mon45=Mon("""vileplume""","""grass""","""poison""",75,80,85,110,90,50)
mon46=Mon("""paras""","""bug""","""grass""",35,70,55,45,55,25)
mon47=Mon("""parasect""","""bug""","""grass""",60,95,80,60,80,30)
mon48=Mon("""venonat""","""bug""","""poison""",60,55,50,40,55,45)
mon49=Mon("""venomoth""","""bug""","""poison""",70,65,60,90,75,90)
mon50=Mon("""diglett""","""ground""","nil",10,55,25,35,45,95)
mon51=Mon("""dugtrio""","""ground""","nil",35,100,50,50,70,120)
mon52=Mon("""meowth""","""normal""","nil",40,45,35,40,40,90)
mon53=Mon("""persian""","""normal""","nil",65,70,60,65,65,115)
mon54=Mon("""psyduck""","""water""","nil",50,52,48,65,50,55)
mon55=Mon("""golduck""","""water""","nil",80,82,78,95,80,85)
mon56=Mon("""mankey""","""fighting""","nil",40,80,35,35,45,70)
mon57=Mon("""primeape""","""fighting""","nil",65,105,60,60,70,95)
mon58=Mon("""growlithe""","""fire""","nil",55,70,45,70,50,60)
mon59=Mon("""arcanine""","""fire""","nil",90,110,80,100,80,95)
mon60=Mon("""poliwag""","""water""","nil",40,50,40,40,40,90)
mon61=Mon("""poliwhirl""","""water""","nil",65,65,65,50,50,90)
mon62=Mon("""poliwrath""","""water""","""fighting""",90,95,95,70,90,70)
mon63=Mon("""abra""","""psychic""","nil",25,20,15,105,55,90)
mon64=Mon("""kadabra""","""psychic""","nil",40,35,30,120,70,105)
mon65=Mon("""alakazam""","""psychic""","nil",55,50,45,135,95,120)
mon66=Mon("""machop""","""fighting""","nil",70,80,50,35,35,35)
mon67=Mon("""machoke""","""fighting""","nil",80,100,70,50,60,45)
mon68=Mon("""machamp""","""fighting""","nil",90,130,80,65,85,55)
mon69=Mon("""bellsprout""","""grass""","""poison""",50,75,35,70,30,40)
mon70=Mon("""weepinbell""","""grass""","""poison""",65,90,50,85,45,55)
mon71=Mon("""victreebel""","""grass""","""poison""",80,105,65,100,70,70)
mon72=Mon("""tentacool""","""water""","""poison""",40,40,35,50,100,70)
mon73=Mon("""tentacruel""","""water""","""poison""",80,70,65,80,120,100)
mon74=Mon("""geodude""","""rock""","""ground""",40,80,100,30,30,20)
mon75=Mon("""graveler""","""rock""","""ground""",55,95,115,45,45,35)
mon76=Mon("""golem""","""rock""","""ground""",80,120,130,55,65,45)
mon77=Mon("""ponyta""","""fire""","nil",50,85,55,65,65,90)
mon78=Mon("""rapidash""","""fire""","nil",65,100,70,80,80,105)
mon79=Mon("""slowpoke""","""water""","""psychic""",90,65,65,40,40,15)
mon80=Mon("""slowbro""","""water""","""psychic""",95,75,110,100,80,30)
mon81=Mon("""magnemite""","""electric""","""steel""",25,35,70,95,55,45)
mon82=Mon("""magneton""","""electric""","""steel""",50,60,95,120,70,70)
mon83=Mon("""farfetchd""","""normal""","""flying""",52,90,55,58,62,60)
mon84=Mon("""doduo""","""normal""","""flying""",35,85,45,35,35,75)
mon85=Mon("""dodrio""","""normal""","""flying""",60,110,70,60,60,110)
mon86=Mon("""seel""","""water""","nil",65,45,55,45,70,45)
mon87=Mon("""dewgong""","""water""","""ice""",90,70,80,70,95,70)
mon88=Mon("""grimer""","""poison""","nil",80,80,50,40,50,25)
mon89=Mon("""muk""","""poison""","nil",105,105,75,65,100,50)
mon90=Mon("""shellder""","""water""","nil",30,65,100,45,25,40)
mon91=Mon("""cloyster""","""water""","""ice""",50,95,180,85,45,70)
mon92=Mon("""gastly""","""ghost""","""poison""",30,35,30,100,35,80)
mon93=Mon("""haunter""","""ghost""","""poison""",45,50,45,115,55,95)
mon94=Mon("""gengar""","""ghost""","""poison""",60,65,60,130,75,110)
mon95=Mon("""onix""","""rock""","""ground""",35,45,160,30,45,70)
mon96=Mon("""drowzee""","""psychic""","nil",60,48,45,43,90,42)
mon97=Mon("""hypno""","""psychic""","nil",85,73,70,73,115,67)
mon98=Mon("""krabby""","""water""","nil",30,105,90,25,25,50)
mon99=Mon("""kingler""","""water""","nil",55,130,115,50,50,75)
mon100=Mon("""voltorb""","""electric""","nil",40,30,50,55,55,100)
mon101=Mon("""electrode""","""electric""","nil",60,50,70,80,80,150)
mon102=Mon("""exeggcute""","""grass""","""psychic""",60,40,80,60,45,40)
mon103=Mon("""exeggutor""","""grass""","""psychic""",95,95,85,125,75,55)
mon104=Mon("""cubone""","""ground""","nil",50,50,95,40,50,35)
mon105=Mon("""marowak""","""ground""","nil",60,80,110,50,80,45)
mon106=Mon("""hitmonlee""","""fighting""","nil",50,120,53,35,110,87)
mon107=Mon("""hitmonchan""","""fighting""","nil",50,105,79,35,110,76)
mon108=Mon("""lickitung""","""normal""","nil",90,55,75,60,75,30)
mon109=Mon("""koffing""","""poison""","nil",40,65,95,60,45,35)
mon110=Mon("""weezing""","""poison""","nil",65,90,120,85,70,60)
mon111=Mon("""rhyhorn""","""ground""","""rock""",80,85,95,30,30,25)
mon112=Mon("""rhydon""","""ground""","""rock""",105,130,120,45,45,40)
mon113=Mon("""chansey""","""normal""","nil",250,5,5,35,105,50)
mon114=Mon("""tangela""","""grass""","nil",65,55,115,100,40,60)
mon115=Mon("""kangaskhan""","""normal""","nil",105,95,80,40,80,90)
mon116=Mon("""horsea""","""water""","nil",30,40,70,70,25,60)
mon117=Mon("""seadra""","""water""","nil",55,65,95,95,45,85)
mon118=Mon("""goldeen""","""water""","nil",45,67,60,35,50,63)
mon119=Mon("""seaking""","""water""","nil",80,92,65,65,80,68)
mon120=Mon("""staryu""","""water""","nil",30,45,55,70,55,85)
mon121=Mon("""starmie""","""water""","""psychic""",60,75,85,100,85,115)
mon122=Mon("""mr-mime""","""psychic""","""fairy""",40,45,65,100,120,90)
mon123=Mon("""scyther""","""bug""","""flying""",70,110,80,55,80,105)
mon124=Mon("""jynx""","""ice""","""psychic""",65,50,35,115,95,95)
mon125=Mon("""electabuzz""","""electric""","nil",65,83,57,95,85,105)
mon126=Mon("""magmar""","""fire""","nil",65,95,57,100,85,93)
mon127=Mon("""pinsir""","""bug""","nil",65,125,100,55,70,85)
mon128=Mon("""tauros""","""normal""","nil",75,100,95,40,70,110)
mon129=Mon("""magikarp""","""water""","nil",20,10,55,15,20,80)
mon130=Mon("""gyarados""","""water""","""flying""",95,125,79,60,100,81)
mon131=Mon("""lapras""","""water""","""ice""",130,85,80,85,95,60)
mon132=Mon("""ditto""","""normal""","nil",48,48,48,48,48,48)
mon133=Mon("""eevee""","""normal""","nil",55,55,50,45,65,55)
mon134=Mon("""vaporeon""","""water""","nil",130,65,60,110,95,65)
mon135=Mon("""jolteon""","""electric""","nil",65,65,60,110,95,130)
mon136=Mon("""flareon""","""fire""","nil",65,130,60,95,110,65)
mon137=Mon("""porygon""","""normal""","nil",65,60,70,85,75,40)
mon138=Mon("""omanyte""","""rock""","""water""",35,40,100,90,55,35)
mon139=Mon("""omastar""","""rock""","""water""",70,60,125,115,70,55)
mon140=Mon("""kabuto""","""rock""","""water""",30,80,90,55,45,55)
mon141=Mon("""kabutops""","""rock""","""water""",60,115,105,65,70,80)
mon142=Mon("""aerodactyl""","""rock""","""flying""",80,105,65,60,75,130)
mon143=Mon("""snorlax""","""normal""","nil",160,110,65,65,110,30)
mon144=Mon("""articuno""","""ice""","""flying""",90,85,100,95,125,85)
mon145=Mon("""zapdos""","""electric""","""flying""",90,90,85,125,90,100)
mon146=Mon("""moltres""","""fire""","""flying""",90,100,90,125,85,90)
mon147=Mon("""dratini""","""dragon""","""nil""",41,64,45,50,50,50)
mon148=Mon("""dragonair""","""dragon""","nil",61,84,65,70,70,70)
mon149=Mon("""dragonite""","""dragon""","""flying""",91,134,95,100,100,80)
mon150=Mon("""mewtwo""","""psychic""","""nil""",106,110,90,154,90,130)
mon151=Mon("""mew""","""psychic""","""nil""",100,100,100,100,100,100)

#moves
class Moves:
    def __init__(self,name,type,pp,pow,acc,attack,defence,spattack,spdefence,speed,evasion,enattack,endefence,enspattack,enspdefence,enspeed,emevasion,emaccuracy,weather,eneffect,hitpriority,secondacc,repeatedhit,maxhealth,critstage,desc):
        self.name = name 
        self.type = type
        self.pp = pp
        self.pow = pow
        self.acc = acc
        self.at = attack  
        self.de = defence
        self.sp_at = spattack   
        self.sp_de = spdefence
        self.spd = speed
        self.eva = evasion
        self.enat = enattack
        self.endf = endefence
        self.enspat = enspattack
        self.enspdef = enspdefence
        self.enspd = enspeed
        self.eneva = emevasion
        self.emac = emaccuracy
        self.weather = weather
        self.enefc = eneffect
        self.hitprio = hitpriority
        self.secondacc = secondacc
        self.rhit = repeatedhit
        self.mhp = maxhealth
        self.crits=critstage
        self.desc=desc



    def call(self):
        return f"{self.name} placeholder text"

move1 = Moves("""absorb""","grass",
        20,20,100,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        """nil""","""nil""","""no""",-1,"""no""",0,0,
        """the user recovers hp equal to 50% of the damage dealt."""
        ) #S
move2 = Moves("""acid""","poison",
        30,40,100,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        """nil""","""nil""","""no""",10,"""no""",0,0,
        """this move has a 10% chance to lower the target's defense by one stage."""
        )
move3 = Moves("""acid armor""","poison",40,-1,-1,
        0,2,0,0,0,0,0,
        0,0,-1,0,0,0,
        """nil""","""nil""","""no""",-1,"""no""",0,0,
        """this move raises the user's defense by two stages."""
        )
move4 = Moves("""aerial ace""","flying",
        20,60,-1,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        """nil""","""nil""","""no""",-1,"""no""",0,0,
        """this move never misses."""
        )
move4 = Moves("""stats testing""","flying",
        99,0,-1,0,0,0,
        1,1,1,1,1,1,1,1,1,1,
        """nil""","""heal_self""","""no""",-1,"""no""",0,0,
        """test stat changes"""
        )