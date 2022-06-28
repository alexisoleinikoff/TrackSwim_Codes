import sys
sys.path.append('/home/tspi/.local/lib/python3.9/site-packages')
import tm1637

tmd = tm1637.TM1637(clk=2, dio=3) #GPIO NUM, écran vert
tmt = tm1637.TM1637(clk=23, dio=24) #GPIO NUM, écran bleu

tmt.brightness(2)

tmt.write([0,0,0,0,0,0])
tmd.write([0,0,0,0,0,0])


tmd.write([79, 91, 134, 125, 109, 102])
tmt.write([79, 91, 6, 125, 109, 102])


