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
        self.hitprio = bool(hitpriority)
        self.secondacc = secondacc
        self.rhit = bool(repeatedhit)
        self.mhp = maxhealth
        self.crits=critstage
        self.desc=desc



    def call(self):
        return f"{self.name:<20} - {self.desc}"
    def nameself(self):
        return f"{self.name:<20} - {self.type}"
move1 = Moves("""absorb""","grass",
                20,20,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """the user recovers hp equal to 50% of the damage dealt."""
                ) #S
move2 = Moves("""acid""","poison",
                30,40,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,10,False,0,0,
                """this move has a 10% chance to lower the target's defense by one stage."""
                )
move3 = Moves("""acid armor""","poison",40,-1,-1,
                0,2,0,0,0,0,0,
                0,0,-1,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move raises the user's defense by two stages."""
                )
move4 = Moves("""aerial ace""","flying",
                20,60,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move never misses."""
                )
move5 = Moves("""aeroblast""","flying",
                5,100,95,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move has an increased critical hit ratio."""
                )
move6 = Moves("""agility""","psychic",
                30,-1,-1,0,0,0,
                0,2,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move raises the user's speed by two stages."""
                )
move7 = Moves("""air cutter""","flying",
                25,55,95,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,1,
                """this move has an increased critical hit ratio."""
                )
move8 = Moves("""amnesia""","psychic",
                20,-1,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move raises the user's sp. def by two stages."""
                )
move9 = Moves("""ancientpower""","rock",
                5,60,100,1,1,1,
                1,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,10,False,0,0,
                """this move has a 10% chance to increase the user's attack, defense, sp. atk, sp. def, and speed by one stage each.""",
                )
move10 = Moves("""arm thrust""","fighting",
                20,15,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,"yes",0,0,
                """this move hits 2-5 times."""
                )
move11 = Moves("""aromatherapy""","grass",
                5,-1,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move cures every pokemon in the party of their status conditions."""
                ) #S
move12 = Moves("""assist""","""normal""",
                20,-1,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """the user will use a random move known by any pokémon on its team."""
                ) #S
move13 = Moves("""astonish""","ghost",
                15,30,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""flinch""",False,30,False,0,0,
                """this move has a 30% chance to make the target flinch."""
                )
move14 = Moves("""attract""","""normal""",
                15,-1,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """if the target is the opposite gender to the user, it will become infatuated."""
                ) #S
move15 = Moves("""aurora beam""","ice",
                20,65,100,0,0,0,
                0,0,0,1,0,0,0,0,0,0,
                """nil""","""nil""",False,10,False,0,0,
                """this move has a 10% chance to lower the target's attack by one stage."""
                )
move16 = Moves("""barrage""","normal",
                20,15,85,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,"yes",0,0,
                """this move hits 2-5 times."""
                )
move17 = Moves("""baton pass""","""normal""",
                40,-1,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """the user switches out; the pokémon that comes in copies all stat changes and minor status conditions."""
                ) #S
move18 = Moves("""beat up""","dark",
                10,10,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,False,0,0,
                """this move hits once per non-fainted pokémon, with each hit using the respective pokémon's attack stat for calculation."""
                ) #S
move19 = Moves("""belly drum""","""normal""",
                10,-1,-1,0,0,0,0,10,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,-50,0,"""the user cuts 50% of their max hp and increases its attack by six stages.""")
move20 = Moves("""bide""","""normal""",10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user charges for two turns, dealing damage equal to double the damage taken on both those turns on the third turn.""") #S
move21 = Moves("""bind""","""normal""",20,15,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""bound""",False,30,False,0,0,"""the target is bound for 2-5 turns.""")
move22 = Moves("""bite""","dark",25,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""flinch""",False,30,False,0,0,"""this move has a 30% chance to make the target flinch.""")
move23 = Moves("""blast burn""","fire",5,150,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after using this move, the user has to recharge for a turn.""") #rc #S
move24 = Moves("""blaze kick""","fire",10,85,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,30,False,0,0,"""this move has an increased critical hit ratio.""")
move25 = Moves("""blizzard""","ice",5,120,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""freeze""",False,10,False,0,0,"""this move has a 10% chance to freeze the target""")
move26 = Moves("""block""","""normal""",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target is prevented from escaping.""") #S
move27 = Moves("""body slam""","""normal""",15,85,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""paralyse""",False,30,False,0,0,"""this move has a 30% chance to paralyze the target.""")
move28 = Moves("""bone club""","ground",20,65,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""flinch""",False,10,False,0,0,"""this move has a 10% chance to make the target flinch.""")
move29 = Moves("""bone rush""","ground",10,25,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,"""yes""",0,0,"""this move hits 2-5 times.""")
move30 = Moves("""<PLACEHOLDER>""","""normal""",1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""placeholder move""")
move31 = Moves("""bonemerang""","ground",10,50,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move hits twice.""") #S
move32 = Moves("""bounce""","flying",5,85,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user jumps into the air on the first turn, evading most attacks, then attacks on the second turn. this move has a 30% chance to paralyze target.""") #do
move33 = Moves("""brick break""","fighting",15,75,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move removes the effects of reflect and light screen from the target's side.""") #S
move34 = Moves("""bubble""","water",30,20,100,0,0,0,0,0,0,0,0,0,0,-1,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to lower the target's speed by one stage.""")
move35 = Moves("""bubblebeam""","water",20,65,100,0,0,0,0,0,0,0,0,0,0,-1,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has a 10% chance to lower the target's speed by one stage.""")
move36 = Moves("""bulk up""","fighting",20,-1,-1,1,1,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's attack and defense by one stage each.""")
move37 = Moves("""bullet seed""","grass",30,10,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,"""yes""",0,0,"""this move hits 2-5 times.""")
move38 = Moves("""calm mind""","psychic",20,-1,-1,0,0,1,1,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's sp. atk and sp. def by one stage each.""")
move39 = Moves("""camouflage""","""normal""",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move changes the user's type according to the terrain the battle takes place.""") #S
move40 = Moves("""charge""","electric",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the power of the user's electric-type attacks on the next turn.""") #S
move41 = Moves("""charm""","""normal""",20,-1,100,0,0,0,0,0,0,-2,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's attack by two stages.""")
move42 = Moves("""clamp""","water",10,35,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""bound""",False,-1,False,0,0,"""the target is bound for 2-5 turns.""")
move43 = Moves("""comet punch""","""normal""",15,18,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,"""yes""",0,0,"""this move hits 2-5 times.""")
move44 = Moves("""confuse ray""","ghost",10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""confuse""",False,-1,False,0,0,"""this move confuses the target.""")
move45 = Moves("""confusion""","psychic",25,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""confuse""",False,10,False,0,0,"""this move has a 10% chance to confuse the target.""")
move46 = Moves("""constrict""","""normal""",35,10,100,0,0,0,0,0,0,0,0,0,0,-2,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to lower the target's speed by one stage.""")
move47 = Moves("""conversion""","""normal""",30,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user changes its type to the type of one of its four moves.""") #S
move48 = Moves("""conversion 2""","""normal""",30,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user changes its type to one that resists the last-used move on it.""") #S
move49 = Moves("""cosmic power""","psychic",20,-1,-1,0,1,0,1,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's defense and sp. def by one stage each.""")
move50 = Moves("""cotton spore""","grass",40,-1,85,0,0,0,0,0,0,0,0,0,0,-2,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's speed by two stages.""")
move51 = Moves("""counter""","fighting",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,"""last""",0,0,"""the user moves last, dealing double the damage it takes from a physical move back to the attacker.""") #S
move52 = Moves("""<PLACEHOLDER>""","""normal""",1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""placeholder move""")
move53 = Moves("""covet""","""normal""",40,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if the target is holding an item and the user is not, the user will steal the item.""") #S
move54 = Moves("""crabhammer""","water",10,90,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,1,"""this move has an increased critical hit ratio.""")
move55 = Moves("""cross chop""","fighting",5,100,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,1,"""this move has an increased critical hit ratio.""")
move56 = Moves("""crunch""","dark",15,80,100,0,0,0,0,0,0,0,0,0,-1,0,0,0,"""nil""","""nil""",False,20,False,0,0,"""this move has a 20% chance to lower the target's sp. def by one stage.""")
move57 = Moves("""crush claw""","""normal""",10,75,95,0,0,0,0,0,0,0,-1,0,0,0,0,0,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance to lower the target's defense by one stage.""")
'''
move62 = Moves("""cut""","""normal""",30,50,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."") "
move63 = Moves("""defense curl""","""normal""",40,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's defense by one stage and doubles the power of rollout and ice ball."") #S
move64 = Moves("""destiny bond""",ghost,5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if the user faints before its next turn after using this move, the attacker also faints."") #S
move65 = Moves(""""detect""""",fighting,5,-1,-1,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,"""nil""","''nil''","''no''",-1,"''no''",
"move72 =(""""double team""""","normal",15,-1,-1,0,0,0,0,0,1,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the user's evasion by one stage."")"
"move73 =(""""double-edge""""","normal",15,120,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user takes recoil damage equal to 1/3 of the damage dealt."") #recoil"
"move75 =(""""doubleslap""""","normal",10,15,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."")"
"move76 =(""""dragon claw""""",dragon,15,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move77 =(""""dragon dance""""",dragon,20,-1,-1,1,0,0,0,1,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the user's attack and speed by one stage each."")"
"move78 =(""""dragon rage""""",dragon,10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals exactly 40 damage."") #S"
"move79 =(""""dragonbreath""""",dragon,20,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,30,False,0,0,"""this move has a 30% chance to paralyze the target."")"
"move80 =(""""dream eater""""",psychic,15,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user recovers hp equal to 50% of the damage dealt. it can only be used on a sleeping target."") #S"
"move81 =(""""drill peck""""",flying,15,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move82 =(""""dynamicpunch""""",fighting,5,100,50,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,-1,False,0,0,"""this move confuses the target."")"
"move83 =(""""earthquake""""",ground,10,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals double damage to targets during the first turn of dig."") #S"
"move84 =(""""egg bomb""""","normal",10,100,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."") "
"move85 =(""""ember""""",fire,25,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move86 =(""""encore""""","normal",5,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move forces the target to only be able to use its last-used move for 2-6 turns."") #S"
"move87 =(""""endeavor""""","normal",5,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move brings the target down to the user's current hp. it fails if the user has greater hp than the opponent."") #S"
"move88 =(""""endure""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",yes,-1,False,0,0,"""this move typically goes first. the user will survive any attack with at least 1 hp for this turn. its success rate decreases with each subsequent use."") #S"
"move89 =(""""eruption""""",fire,5,150,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power decreases the less hp the user has."") #S"
"move90 =(""""explosion""""","normal",5,250,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,-999,0,"""this move causes the user to faint. the target's defense is halved during this attack."") #S"
"move91 =(""""extrasensory""""",psychic,30,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,10,False,0,0,"""this move has a 10% chance to confuse the target."")"
"move92 =(""""extremespeed""""","normal",5,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",yes,-1,False,0,0,"""this move typically goes first."")"
"move93 =(""""facade""""","normal",20,70,101,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move never misses."")
"move95 =(""""faint attack""""",dark,25,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move never misses."")"
"move96 =(""""fake out""""","normal",10,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,yes,-1,False,0,0,"""this move typically goes first and makes the target flinch. it can only be used on the first turn the user is in battle."")"
"move97 =(""""fake tears""""",dark,20,-1,100,0,0,0,0,0,0,0,0,0,-2,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move decreases the target's sp. def by two stages."")"
"move98 =(""""False swipe""""","normal",40,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move always leaves the target at at least 1hp."") #S"
"move99 =(""""featherdance""""",flying,15,-1,100,0,0,0,0,0,0,-2,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move decreases the target's attack by two stages."")"
"move100 =(""""fire blast""""",fire,5,120,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move101 =(""""fire punch""""",fire,15,75,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move102 =(""""fire spin""""",fire,15,15,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bound,False,-1,False,0,0,"""the target is bound for 2-5 turns."")"
"move103 =(""""fissure""""",ground,5,-1,30,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target immediately faints. this move fails if the user is at a lower level than the target."") #S"
"move104 =(""""flail""""","normal",15,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power increases the less hp the user has."") #S"
"move105 =(""""flame wheel""""",fire,25,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move106 =(""""flamethrower""""",fire,15,95,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move107 =(""""flash""""","normal",20,-1,70,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's accuracy by one stage."")"
"move108 =(""""flatter""""",dark,15,-1,100,0,0,0,0,0,0,0,0,1,0,0,0,0,"""nil""",confuse,False,-1,False,0,0,"""this move confuses the target and increases its sp. atk by one stage."")"
"move109 =(""""fly""""",flying,15,70,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user flies into the air on the first turn, evading most attacks, then attacks on the second turn."") #do"
"move110 =(""""focus energy""""","normal",30,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the user's critical hit ratio."") #S"
"move111 =(""""focus punch""""",fighting,20,150,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",last,-1,False,0,0,"""the user tightens its focus at the start of the turn, then attacks at the end of the turn. the move fails if the user is attacked while focusing."") #S"
"move112 =(""""follow me""""","normal",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move typically goes first. it makes the user the center of attention, making all opponent attacks redirect to it in a double battle."") #db"
"move113 =(""""foresight""""","normal",40,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target's evasion modifiers and ghost-type immunities are ig""no""red by the user."") #S"
,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,
"move115 =(""""frenzy plant""""",grass,5,150,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after using this move, the user has to recharge for a turn."") #rc #S"
"move116 =(""""frustration""""","normal",20,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power increases the lower the user's friendship is."") #S"
"move117 =(""""fury attack""""","normal",20,15,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."") "
"move118 =(""""fury cutter""""",bug,20,10,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power doubles with each subsequent use."") #S"
"move119 =(""""fury swipes""""","normal",15,18,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."")"
"move120 =(""""future sight""""",psychic,15,80,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move attacks the target two turns after is is used, using damage calculation from the turn it was used. its damage is typeless."")"
"move121 =(""""giga drain""""",grass,5,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,-1,False,0,0,"""the user recovers hp equal to 50% of the damage dealt."") #S"
"move122 =(""""glare""""","normal",30,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move paralyzes the target."")"
"move123 =(""""grasswhistle""""",grass,15,-1,55,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move puts the target to sleep."")"
"move124 =(""""growl""""","normal",40,-1,100,0,0,0,0,0,0,1,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's attack by one stage."")"
"move125 =(""""growth""""","normal",40,-1,-1,0,0,0,0,0,0,0,0,1,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's sp. atk by one stage."")"
"move126 =(""""grudge""""",ghost,5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if the user faints before its next turn after using this move, the pp of the finishing move is fully depleted."") #S"
"move127 =(""""guillotine""""","normal",5,-1,30,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target immediately faints. this move fails if the user is at a lower level than the target."") #S"
"move128 =(""""gust""""",flying,35,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move129 =(""""hail""""",ice,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,hail,"""nil""",False,-1,False,0,0,"""the user summons hail, replacing the current weather, for five turns."")"
"move130 =(""""harden""""","normal",30,-1,-1,0,1,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's defense by one stage."")"
"move131 =(""""haze""""",ice,30,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move removes all stat modifiers from all pokémon."") #S"
"move132 =(""""headbutt""""","normal",15,70,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,0,"""this move has a 30% chance to make the target flinch."")"
"move133 =(""""heal bell""""","normal",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move cures every pokemon in the party of their status conditions."") #S"
"move134 =(""""heat wave""""",fire,10,100,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,10,False,0,0,"""this move has a 10% chance to burn the target."")"
"move135 =(""""helping hand""""","normal",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move typically goes first. it increases the power of an ally's attack by 50 ."") #S"
,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,
"move137 =(""""hi jump kick""""",fighting,20,85,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if this move misses, the user takes damage equal to 50% of how much damage it would've dealt."") #S"
"move138 =(""""hidden power""""","normal",15,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's type and power is determined by the user's ivs."") #S"
"move139 =(""""horn attack""""","normal",25,65,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move140 =(""""horn drill""""","normal",5,-1,30,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target immediately faints. this move fails if the user is at a lower level than the target."") #S"
"move141 =(""""howl""""","normal",40,-1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's attack by one stage."")"
"move142 =(""""hydro can""no""n""""",water,5,150,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after using this move, the user has to recharge for a turn."") #rc"
"move143 =(""""hydro pump""""",water,5,120,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move144 =(""""hyper beam""""","normal",5,150,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after using this move, the user has to recharge for a turn."") #rc"
"move145 =(""""hyper fang""""","normal",15,80,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,10,False,0,0,"""this move has a 10% chance to make the target flinch."")"
"move146 =(""""hyper voice""""","normal",10,90,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move147 =(""""hyp""no""sis""""",psychic,20,-1,60,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move puts the target to sleep."")"
"move148 =(""""ice ball""""",ice,20,30,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user will repeatedly use this attack for up to five turns, with its base power doubling after each consecutive use."") #S"
"move149 =(""""ice beam""""",ice,1,95,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",freeze,False,10,False,0,0,"""this move has a 10% chance to freeze the target."")"
"move150 =(""""ice punch""""",ice,15,75,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",freeze,False,10,False,0,0,"""this move has a 10% chance to freeze the target."")"
"move151 =(""""icicle spear""""",ice,30,10,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."")"
"move152 =(""""icy wind""""",ice,15,55,95,0,0,0,0,0,0,0,0,0,0,-1,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's speed by one stage."")"
"move153 =(""""imprison""""",psychic,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move disables all moves the target shares with the user."") #S"
"move154 =(""""ingrain""""",grass,20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,6.25,0,"""after use, the user will recover 1/16 of their max hp, but they can""no""t be switched out."") #S"
"move155 =(""""iron defense""""",steel,15,-1,-1,0,2,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's defense by two stages."")"
"move156 =(""""iron tail""""",steel,15,100,75,0,0,0,0,0,0,0,-1,0,0,0,0,0,"""nil""","""nil""",False,30,False,0,0,"""this move has a 30% chance to lower the target's defense by one stage."")"
,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,
"move158 =(""""jump kick""""",fighting,20,70,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if this move misses, the user takes damage equal to 50% of how much damage it would've dealt."") #S"
"move159 =(""""karate chop""""",fighting,20,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,1,"""this move has an increased critical hit ratio."")"
"move160 =(""""kinesis""""",psychic,15,-1,80,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's accuracy by one stage."")"
"move161 =(""""k""no""ck off""""",dark,20,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move removes the target's held item for the rest of the battle."")"
"move162 =(""""leaf blade""""",grass,15,70,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move removes the target's held item for the rest of the battle."")"
"move163 =(""""leech life""""",bug,15,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user recovers hp equal to 50% of the damage dealt."")"
"move164 =(""""leech seed""""",grass,10,-1,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move seeds the target, draining 1/8 of its max hp each turn."")"
"move165 =(""""leer""""","normal",30,-1,100,0,0,0,0,0,0,0,-1,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's defense by one stage."")"
"move166 =(""""lick""""",ghost,30,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,30,False,0,0,"""this move has a 30% chance to paralyze the target."")"
"move167 =(""""light screen""""",psychic,30,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""all special damage taken on the user's side is halved for five 5 turns."") #S"
"move168 =(""""lock-on""""","normal",5,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, the user's next attack is guaranteed to hit its target."") #S"
"move169 =(""""lovely kiss""""","normal",10,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move puts the target to sleep."")"
"move170 =(""""low kick""""",fighting,20,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power increases depending on the target's weight."") #S"
"move171 =(""""luster purge""""",psychic,5,70,100,0,0,0,0,0,0,0,0,0,-1,0,0,0,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance of lowering the target's sp. def by one stage."")"
"move172 =(""""mach punch""""",fighting,30,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move typically goes first."") "
"move173 =(""""magic coat""""",psychic,15,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move typically goes first. the user will reflect one status move this turn, instead having the move hit the user."") #S"
"move174 =(""""magical leaf""""",grass,20,60,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move never misses."")"
"move175 =(""""magnitude""""",ground,30,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's randomly varies between seven levels of power, ranging from 10 to 150."") #S"
"move176 =(""""mean look""""","normal",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target is trapped and can""no""t escape."") #S"
"move177 =(""""meditate""""",psychic,40,-1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's attack by one stage."")"
"move178 =(""""mega drain""""",grass,10,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user recovers hp equal to 50% of the damage dealt."") #S"
,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,
"move180 =(""""mega kick""""","normal",5,120,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move181 =(""""mega punch""""","normal",20,80,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move182 =(""""megahorn""""",bug,10,120,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move183 =(""""memento""""",dark,10,-1,100,0,0,0,0,0,0,-2,-2,0,0,0,0,0,"""nil""","""nil""",False,-1,False,-999,0,"""this move makes the user faint and lowers the target's attack and sp. atk by two stages each."")"
"move184 =(""""metal claw""""",steel,35,50,95,1,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to raise the user's attack by one stage."")"
"move185 =(""""metal sound""""",steel,40,-1,85,0,0,0,0,0,0,0,0,0,-2,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's sp. def by two stages."")"
"move186 =(""""meteor mash""""",steel,10,100,85,2,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,20,False,0,0,"""this move has a 20% chance to raise the user's attack by one stage."")"
"move187 =(""""metro""no""me""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move activates any move in the game at random."") #S"
"move188 =(""""milk drink""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move189 =(""""mimic""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, this move will be replaced by the target's last-used move for the rest of the battle."") #S"
"move190 =(""""mind reader""""","normal",5,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, the user's next attack is guaranteed to hit its target."") #S"
"move191 =(""""minimize""""","normal",20,-1,-1,0,0,0,0,0,2,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the user's evasion by two stages."") "
"move192 =(""""mirror coat""""",psychic,20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user moves last, dealing double the damage it takes from a physical move back to the attacker."") #S"
"move193 =(""""mirror move""""",flying,20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user uses the last-used move of the target."") #S"
"move194 =(""""mist""""",ice,30,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user's side is immune to negative stat modifiers for five 5 turns."") #S"
"move195 =(""""mist ball""""",psychic,5,70,100,0,0,0,0,0,0,0,0,-1,0,0,0,0,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance to lower the target's sp. atk by 1 stage."")"
"move196 =(""""moonlight""""","normal",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move197 =(""""morning sun""""","normal",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move198 =(""""mud shot""""",ground,15,55,95,0,0,0,0,0,0,0,0,-1,0,0,0,0,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance to lower the target's sp. atk by 1 stage."")"
"move199 =(""""mud sport""""",ground,15,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user's side takes 50% damage from electric-type moves for five 5 turns."") #S"
"move200 =(""""mud-slap""""",ground,10,20,100,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's accuracy by 1 stage."")"
,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,
"move202 =(""""muddy water""""",water,10,95,85,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,30,False,0,0,"""this move has a 30% chance to lower the target's accuracy by 1 stage."")"
"move203 =(""""nature power""""","normal",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move turns into a different move depending on the terrain the battle takes place."") #S"
"move204 =(""""needle arm""""",grass,15,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,-1,False,30,0,"""this move has a 30% chance to make the target flinch."")"
"move205 =(""""night shade""""",ghost,15,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals damage equal to the user's level."") #S"
"move206 =(""""nightmare""""",ghost,15,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move causes a sleeping target to take damage equal to 25% of its max hp at the end of each turn it is asleep."") #S"
"move207 =(""""octazooka""""",water,10,65,85,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance to lower the target's accuracy by one stage."")"
"move208 =(""""odor sleuth""""","normal",40,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target's evasion modifiers and ghost-type immunities are ig""no""red by the user."") #S"
"move209 =(""""outrage""""",dragon,20,90,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move is used 2-3 turns in a row. the user becomes confused after the turn it finishes."") #S"
"move210 =(""""overheat""""",fire,5,140,90,0,0,0,0,0,0,0,0,-2,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, the user's sp. atk is lowered by two stages."")"
"move211 =(""""pain split""""","normal",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move sets the user and target's current hp to their combined average."") #S"
"move212 =(""""pay day""""","normal",20,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if this move is used, extra money will be collected after the battle."") #S"
"move213 =(""""peck""""",flying,35,35,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move214 =(""""perish song""""","normal",5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""when this move is used, all pokémon currently in play will be set to instantly faint in 3 turns. this effect is removed when the pokémon is switched out."") #S"
"move215 =(""""petal dance""""",grass,20,70,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move is used 2-3 turns in a row. the user becomes confused after the turn it finishes."") #S"
"move216 =(""""pin missile""""",bug,20,14,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."")"
"move217 =(""""poison fang""""",poison,15,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bpoison,False,30,False,0,0,"""this move has a 30% chance to badly poison the target."")"
"move218 =(""""poison gas""""",poison,40,-1,55,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move poisons the target."")"
"move219 =(""""poison sting""""",poison,35,15,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",poison,False,20,False,0,0,"""this move has a 20% chance to poison the target."")"
"move220 =(""""poison tail""""",poison,25,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",poison,False,10,False,0,1,"""this move has an increased critical hit ratio and a 10% chance to poison the target."")"
"move221 =(""""poisonpowder""""",poison,35,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move poisons the target."")"
"move222 =(""""pound""""","normal",35,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move223 =(""""powder s""no""w""""",ice,25,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",freeze,False,10,False,0,0,"""this move has a 10% chance of freezing the target."")"
"move224 =(""""present""""","normal",15,-2,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals -2 damage, and has a 20% chance to heal the target for 25% of their max hp."") #S"
"move225 =(""""protect""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user moves first and protects from most attacks. its success rate decreases with subsequent uses."") #S"
"move226 =(""""psybeam""""",psychic,20,65,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,10,False,0,0,"""this move has a 10% chance to confuse the target."")"
"move227 =(""""psych up""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user copies all stat modifiers of the target."") #S"
"move228 =(""""psychic""""",psychic,10,90,100,0,0,0,0,0,0,0,0,0,-1,0,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to lower the target's sp. def by one stage."")"
"move229 =(""""psycho boost""""",psychic,5,140,90,0,0,-2,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, the user's sp. atk is lowered by two stages."")"
"move230 =(""""psywave""""",psychic,15,-2,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals -2 damage depending on the user's level."") #S"
"move231 =(""""pursuit""""",dark,20,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move will be used before a pokémon is switched out, doubling its power."") #S"
"move232 =(""""quick attack""""","normal",30,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",yes,-1,False,0,0,"""this move typically goes first."")"
"move233 =(""""rage""""","normal",20,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after this move is used, the user's attack will increase by one stage for each time it is hit."") #S"
"move234 =(""""rain dance""""",water,5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,rain,"""nil""",False,-1,False,0,0,"""the user summons rain, replacing the current weather, for five turns."")"
"move235 =(""""rapid spin""""","normal",40,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after this move is used, the effects of binding, leech seed, and spikes are removed."") #S"
"move236 =(""""razor leaf""""",grass,25,55,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,1,"""this move has an increased critical hit ratio."")"
"move237 =(""""razor wind""""","normal",10,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user charges on the first turn, then attack on the second turn."") #S"
"move238 =(""""recover""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move239 =(""""recycle""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if the user has used up a held item, this move recovers it when used."") #S"
"move240 =(""""reflect""""",psychic,20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""all physical damage taken on the user's side is halved for five 5 turns."") #S"
"move241 =(""""refresh""""","normal",20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user cures itself of its poison, burn, or paralysis."") #S"
"move242 =(""""rest""""",psychic,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move puts the user to sleep, replacing any current status condition, but restores all of its hp."") #S"
"move243 =(""""return""""","normal",20,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power increases the greater the user's friendship is."") #S"
"move244 =(""""revenge""""",fighting,10,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",last,-1,False,0,0,"""this move typically goes last. its power is doubled if the user was hit during the turn."") #S"
"move245 =(""""reversal""""",fighting,15,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power increases the less hp the user has."") #S"
"move246 =(""""roar""""","normal",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move typically goes last. the target is forced to switch out. this ends a wild battle."") #S"
"move247 =(""""rock blast""""",rock,10,25,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""this move hits 2-5 times."")"
"move248 =(""""rock slide""""",rock,10,70,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,0,"""this move has a 30% chance to make the target flinch."")"
"move249 =(""""rock smash""""",fighting,15,20,100,0,0,0,0,0,0,0,-1,0,0,0,0,0,"""nil""","""nil""",False,50,False,0,0,"""this move has a 50% chance to lower the target's defense by one stage."")"
"move250 =(""""rock throw""""",rock,15,50,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move251 =(""""rock tomb""""",rock,10,50,80,0,0,0,0,0,0,0,0,0,0,-1,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's speed by one stage."")"
"move252 =(""""role play""""",psychic,10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user copies the target's ability, replacing its current ability."") #S"
"move253 =(""""rolling kick""""",fighting,15,60,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,0,"""this move has a 30% chance to make the target flinch."") "
"move254 =(""""rollout""""",rock,20,30,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user will repeatedly use this attack for up to five turns, with its base power doubling after each consecutive use."") #S"
"move255 =(""""sacred fire""""",fire,5,100,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,50,False,0,0,"""this move has a 50% chance of burning the target."")"
"move256 =(""""safeguard""""","normal",25,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user's side is immune to status conditions for five turns."") #S"
"move257 =(""""sand tomb""""",ground,15,15,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bound,False,-1,False,0,0,"""the target is bound for 2-5 turns."")"
"move258 =(""""sand-attack""""",ground,15,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's accuracy by one stage."")"
"move259 =(""""sandstorm""""",rock,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,sandstorm,"""nil""",False,-1,False,0,0,"""the user summons a sandstorm, replacing the current weather, for five turns."")"
"move260 =(""""scary face""""","normal",10,-1,90,0,0,0,0,0,0,0,0,0,0,-2,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's speed by two stages."")"
"move261 =(""""scratch""""","normal",35,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move262 =(""""screech""""","normal",10,-1,85,0,0,0,0,0,0,0,0,0,-2,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's defense by two stages."")"
"move263 =(""""secret power""""","normal",20,70,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's secondary effect depends on the battle location."") #S"
"move264 =(""""seismic toss""""",fighting,20,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals damage equal to the user's level."") #S"
"move265 =(""""selfdestruct""""","normal",5,200,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move causes the user to faint. the target's defense is halved during this attack."") #S"
"move266 =(""""shadow ball""""",ghost,15,80,100,0,0,0,0,0,0,0,0,0,-1,0,0,0,"""nil""","""nil""",False,20,False,0,0,"""this move has a 20% chance to lower the target's sp. def by one stage."")"
"move267 =(""""shadow punch""""",ghost,20,60,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move never misses."")"
"move268 =(""""sharpen""""","normal",30,-1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move increases the user's attack by one stage."")"
"move269 =(""""sheer cold""""",ice,5,-1,30,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,-999,0,"""the target immediately faints. this move fails if the user is at a lower level than the target."") #S"
"move270 =(""""shock wave""""",electric,20,60,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move never misses."")"
"move271 =(""""signal beam""""",bug,15,75,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,10,False,0,0,"""this move has a 10% chance to confuse the target."")"
"move272 =(""""silver wind""""",bug,5,60,100,1,1,1,1,1,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to increase the user's attack, defense, sp. atk, sp. def, and speed by one stage each."")"
"move273 =(""""sing""""","normal",15,-1,55,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move puts the target to sleep."")"
"move274 =(""""sketch""""","normal",1,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, this move will be permanently replaced by the target's last-used move."")"
"move275 =(""""skill swap""""",psychic,10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user and target receive each other's abilities."")"
"move276 =(""""skull bash""""","normal",15,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user charges on the first turn and raises its defense by one stage, then attacks on the second turn."") #S"
"move277 =(""""sky attack""""",flying,5,140,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,1,"""the user charges on the first turn and attacks on the second turn. it has an increased critical hit ratio and a 30% chance to make the target flinch."") #S"
"move278 =(""""sky uppercut""""",fighting,15,85,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move279 =(""""slack off""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move280 =(""""slam""""","normal",20,80,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move281 =(""""slash""""","normal",20,70,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,1,"""this move has an increased critical hit ratio."")"
"move282 =(""""sleep powder""""",grass,15,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move puts the target to sleep."")"
"move283 =(""""sleep talk""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move only works if the user is asleep. it has the user use one of its other moves at random."") #S"
"move284 =(""""sludge""""",poison,20,65,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",poison,False,30,False,0,0,"""this move has a 30% chance to poison the target."")"
"move285 =(""""sludge bomb""""",poison,10,90,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",poison,False,30,False,0,0,"""this move has a 30% chance to poison the target."")"
"move286 =(""""smellingsalt""""","normal",10,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power is doubled against a paralyzed target, curing its paralysis in the process."") #S"
"move287 =(""""smog""""",poison,20,20,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",poison,False,40,False,0,0,"""this move has a 40% chance to poison the target."")"
"move288 =(""""smokescreen""""","normal",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,-1,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's accuracy by one stage."")"
"move289 =(""""snatch""""",dark,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",yes,-1,False,0,0,"""this move typically goes first. if a""no""ther pokémon uses a status move that turn, the user will use it instead."") #S"
"move290 =(""""s""no""re""""","normal",15,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,0,"""this move only works if the user is asleep. it has a 30% chance to make the user flinch."") #S"
"move291 =(""""softboiled""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move292 =(""""solarbeam""""",grass,10,120,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user charges on the first turn, then attack on the second turn. the charging turn is skipped under harsh sunlight."") #S"
"move293 =(""""sonicboom""""","normal",20,-1,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move deals exactly 20 damage."") #S"
"move294 =(""""spark""""",electric,20,65,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,30,False,0,0,"""this move has a 30% chance to paralyze the target."")"
"move295 =(""""spider web""""",bug,10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the target is prevented from escaping."") #S"
"move296 =(""""spike can""no""n""""","normal",15,20,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",yes,-1,False,0,0,"""this move hits 2-5 times."")"
"move297 =(""""spikes""""",ground,20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move covers the opponent's side with spikes that damage any pokémon without a ground-type immunity on entry. up to three layers of spikes can be set for extra damage."") #S"
"move298 =(""""spit up""""","normal",10,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power is determined by the user's stockpile count. it resets the stockpile count to 0 after use."") #S"
"move299 =(""""spite""""",ghost,10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move reduces the pp of the target's last-used move by 2-5."") #S"
"move300 =(""""splash""""","normal",40,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move does ""no""thing."")"
"move301 =(""""spore""""",grass,15,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",sleep,False,-1,False,0,0,"""this move puts the target to sleep."")"
"move302 =(""""steel wing""""",steel,25,70,95,0,1,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,10,False,0,0,"""this move has a 10% chance to raise the user's defense by one stage."")"
"move303 =(""""stockpile""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user increases its stockpile count by 1. the user can go up to a stockpile count of 3."") #S"
"move304 =(""""stomp""""","normal",20,65,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",flinch,False,30,False,0,0,"""this move has a 30% chance to make the target flinch."")"
"move305 =(""""strength""""","normal",15,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move306 =(""""string shot""""",bug,40,-1,95,0,0,0,0,0,0,0,0,0,0,-2,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's speed by two stages."")"
"move307 =(""""struggle""""","normal",1,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user takes recoil damage equal to 25% of the damage dealt."") #recoil"
"move308 =(""""stun spore""""",grass,30,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,-1,False,0,0,"""this move paralyzes the target."")"
"move309 =(""""submission""""",fighting,20,80,80,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user takes recoil damage equal to 25% of the damage dealt."") #recoil"
"move310 =(""""substitute""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,-25,0,"""the user cuts 25% of its hp to create a decoy that is immune to most status moves and takes damage equal to the hp cut from the user."") #S"
"move311 =(""""sunny day""""",fire,5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,sunlight,"""nil""",False,-1,False,0,0,"""the user summons harsh sunlight, replacing the current weather, for five turns."")"
"move312 =(""""super fang""""","normal",10,-2,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move cuts the target's current hp in half."")"
"move313 =(""""superpower""""",fighting,5,120,100,-1,-1,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after use, this move lowers the user's attack and defense by one stage each."")"
"move314 =(""""supersonic""""","normal",20,-1,55,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,-1,False,0,0,"""this move confuses the target."")"
"move315 =(""""surf""""",water,15,95,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move316 =(""""swagger""""","normal",15,-1,90,0,0,0,0,0,0,2,0,0,0,0,0,0,"""nil""",confuse,False,-1,False,0,0,"""this move raises the target's attack by two stages, then confuses it."")"
"move317 =(""""swallow""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user restores hp based on the stockpile count. it resets the stockpile count to 0 after use."") #S"
"move318 =(""""sweet kiss""""","normal",10,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",confuse,False,-1,False,0,0,"""this move confuses the target."")"
"move319 =(""""sweet scent""""","normal",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,-2,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's evasion by two stages."")"
"move320 =(""""swift""""","normal",20,60,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this attack never misses."")"
"move321 =(""""swords dance""""","normal",30,-1,-1,2,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's attack by two stages."")"
"move322 =(""""synthesis""""",grass,5,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,50,0,"""this move restores 50% of the user's max hp."")"
"move323 =(""""tackle""""","normal",35,35,95,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move324 =(""""tail glow""""",bug,20,-1,-1,0,0,2,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move raises the user's sp. atk by two stages."")"
"move325 =(""""tail whip""""","normal",30,-1,100,0,0,0,0,0,0,0,-1,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's defense by 1 stage."")"
"move326 =(""""take down""""","normal",20,90,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user takes recoil damage equal to 25% of the damage dealt."") #recoil"
"move327 =(""""taunt""""",dark,20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move forces the target to use only attacking moves for two turns."") #S"
"move328 =(""""teeter dance""""","normal",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move confuses every other pokémon in play."") #S"
"move329 =(""""teleport""""",psychic,20,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move ends a wild battle. it fails in a trainer battle."") #S"
"move330 =(""""thief""""",dark,10,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""if the target is holding an item and the user is ""no""t, the user will steal the item."") #S"
"move331 =(""""thrash""""","normal",20,90,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move is used 2-3 turns in a row. the user becomes confused after the turn it finishes."") #S"
"move332 =(""""thunder""""",electric,10,120,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,10,False,0,0,"""this move has a 10% chance to paralyze the target."") "
"move333 =(""""thunder wave""""",electric,20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,-1,False,0,0,"""this move paralyzes the target."")"
"move334 =(""""thunderbolt""""",electric,15,95,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,10,False,0,0,"""this move has a 10% chance to paralyze the target."")"
"move335 =(""""thunderpunch""""",electric,15,75,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,10,False,0,0,"""this move has a 10% chance to paralyze the target."")"
"move336 =(""""thundershock""""",electric,30,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,10,False,0,0,"""this move has a 10% chance to paralyze the target."")"
"move337 =(""""tickle""""","normal",20,-1,100,0,0,0,0,0,0,-1,-1,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move lowers the target's attack and defense by one stage each."")"
"move338 =(""""torment""""",dark,15,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move prevents the target from using the same move twice in a row."") #S"
"move339 =(""""toxic""""",poison,10,-1,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bpoison,False,-1,False,0,0,"""this move badly poisons the target."")"
"move340 =(""""transform""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move transforms the user into the target, copying its stats and moves, each with 5 pp."") #S"
"move341 =(""""tri attack""""","normal",10,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has a 20% chance to either paralyze, freeze, or burn the target."") #S"
"move342 =(""""trick""""",psychic,10,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user swaps held items with the target."") #S"
"move343 =(""""triple kick""""",fighting,10,10,90,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move hits up to three times, with each hit having a chance to miss."") #S"
"move344 =(""""twineedle""""",bug,20,25,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move hits twice."") #S"
"move345 =(""""twister""""",dragon,20,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has a 20% chance to make the user flinch."") #S"
"move346 =(""""uproar""""","normal",10,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,0,0,"""the user will repeatedly use this attack for 2-5 turns, during which all pokémon can""no""t fall asleep and sleeping pokémon will be woken up."") #S"
"move347 =(""""vicegrip""""","normal",30,55,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move348 =(""""vine whip""""",grass,10,35,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move349 =(""""vital throw""""",fighting,10,70,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",last,-1,False,0,0,"""this move typically goes last. it never misses."")"
"move350 =(""""volt tackle""""",electric,15,120,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user takes recoil damage equal to 1/3 of the damage dealt."") #recoil"
"move351 =(""""water gun""""",water,25,40,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move352 =(""""water pulse""""",water,20,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,yes,20,0,"""this move has a 20% chance to confuse the target."")"
"move353 =(""""water sport""""",water,15,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""the user's side takes 50% damage from fire-type moves for five 5 turns."") #S"
"move354 =(""""water spout""""",water,5,-2,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power decreases the less hp the user has."") #S"
"move355 =(""""waterfall""""",water,15,80,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move356 =(""""weather ball""""","normal",10,50,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move's power is doubled in any weather, and its type changes depending on the weather."") #S"
"move357 =(""""whirlpool""""",water,15,15,70,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bound,False,-1,False,0,0,"""the target is bound for 2-5 turns."")"
"move358 =(""""whirlwind""""","normal",20,-1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",last,-1,False,0,0,"""this move typically goes last. the target is forced to switch out. this ends a wild battle."") #S"
"move359 =(""""will-o-wisp""""",fire,15,-1,75,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",burn,False,-1,False,0,0,"""this move burns the target."")"
"move360 =(""""wing attack""""",flying,35,60,100,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""this move has "False"secondary effect."")"
"move361 =(""""wish""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""","""nil""",False,-1,False,0,0,"""after the next turn, this move heals the current pokémon for 50% of the user's max hp."") #S"
"move362 =(""""withdraw""""",water,40,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bound,False,-1,False,0,0,"""the target is bound for 2-5 turns."")"
"move363 =(""""wrap""""","normal",20,15,85,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",bound,False,-1,False,0,0,"""the target is bound for 2-5 turns."")"
"move364 =(""""yawn""""","normal",10,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",drowsy,False,-1,False,0,0,"""this move makes the target drowsy. after the next turn, it will fall asleep."")"
"move365 =(""""zap can""no""n""""",electric,5,100,50,0,0,0,0,0,0,0,0,0,0,0,0,0,"""nil""",paralyse,False,-1,False,0,0,"""this move paralyzes the target."")"
'''
#ensure all placeholder moves work before adding actual moves (test speical effects, poison, double hits etc)
move366 = Moves("""<stat_test>""","flying",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""heal_self""",False,-1,False,0,0,
                """test stat changes"""
                )
move367 = Moves("""<poison_test>""","poison",
                10,10,100,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""poison_enemy""",False,-1,"no",0,0,
                """no"""
                )
move368 = Moves("""<paralyse_test>""","electric",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""paralyse_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move369 = Moves("""<burn_test>""","fire",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""burn_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move370 = Moves("""<nuke_test>""","normal",
                99,99999,-1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""burn_enemy""",False,-1,False,0,0,
                """kaboom, explosion final boss"""
                )
move371 = Moves("""<flinch_test>""","dark",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""flinch_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move372 = Moves("""<sleep_test>""","sleep",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""flinch_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move373 = Moves("""<bind_test>""","grass",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""bind_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move374 = Moves("""<frozen_test>""","ice",
                99,0,-1,0,0,0,
                1,1,1,1,1,1,1,1,1,1,
                """nil""","""ice_enemy""",False,-1,False,0,0,
                """test stat changes"""
                )
move375 = Moves("""<miss>""","grass",
                10,0,1,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,"no",0,0,
                """no"""
                )
move376 = Moves("""<splash>""","water",
                40,0,-50,0,0,0,
                0,0,0,0,0,0,0,0,0,0,
                """nil""","""nil""",False,-1,"no",0,0,
                """no"""
                )