from SceneGenerator import MovingObject



import Clock

for i in range(1000):
    O = MovingObject(50,(512,512), 60, 30)

    for f in range(1500):
        t = f/50

        Clock.update(t)

        rT, cL, rB, cR = O.getBounds()

        if((cR-cL!=50 )|(rB-rT)!=50):
            print(cL,cR)
            rT, cL, rB, cR = O.getBounds()

        if((cR<0) | (cL)<0 | rT <0 |rB<0):
            print('Negative')
