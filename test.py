class WurzelKnoten(object):
    def __init__(self, wert):
        self.wert = wert
        self.links = None
        self.rechts = None
        self.hoehe = 1

class AVLBaum(object):
    def suche(self, wurzel, key):
        if wurzel is None:
            print("search false")
            return None
        elif wurzel.wert == key:
            print("search true")
            return wurzel
        elif wurzel.wert > key:
            return Baum.suche(wurzel.links, key)
        else:
            return Baum.suche(wurzel.rechts, key)

    def insert(self, wurzel, key):
        if not wurzel:
            # print("Inserted node: ", key)
            print("ins true")
            return WurzelKnoten(key)
        elif key < wurzel.wert:
            wurzel.links = self.insert(wurzel.links, key)
        elif key > wurzel.wert:
            wurzel.rechts = self.insert(wurzel.rechts, key)
        else:
            print("ins false")

        wurzel.hoehe = 1 + max(self.gethoehe(wurzel.links),
                              self.gethoehe(wurzel.rechts))
        balance2 = Baum.balancieren(wurzel, key)
        return balance2
        
    def loeschen(self, wurzel, key):
        if wurzel is None:
            print("del false")
            return None
        elif wurzel.wert == key:
            print("del true")
            wurzel = None
        elif key > wurzel.wert:
            wurzel.rechts = self.loeschen(wurzel.rechts, key)
        elif key < wurzel.wert:
            wurzel.links = self.loeschen(wurzel.links, key)
        else:
            print("del false")

        wurzel.hoehe = 1 + max(self.gethoehe(wurzel.links),
                             self.gethoehe(wurzel.rechts))            
        balance3 = Baum.balancieren(wurzel, key)
        return balance3
            
            
    def balancieren(self, wurzel, key):
        balance = self.getBalance(wurzel)
        if balance > 1 and key < wurzel.links.wert:
            return self.rechtsRotation(wurzel)
        elif balance < -1 and key > wurzel.rechts.wert:
            return self.linksRotation(wurzel)
        elif balance > 1 and key > wurzel.links.wert:
            wurzel.links = self.linksRotation(wurzel.links)
            return self.rechtsRotation(wurzel)
        elif balance < -1 and key < wurzel.rechts.wert:
            wurzel.rechts = self.rechtsRotation(wurzel.rechts)
            return self.linksRotation(wurzel)
        return wurzel

    def rechtsRotation(self, x):
        y = x.links
        puffer = y.rechts
        y.rechts = x
        x.links = puffer
        x.hoehe = 1 + max(self.gethoehe(x.links),
                           self.gethoehe(x.rechts))
        y.hoehe = 1 + max(self.gethoehe(y.links),
                           self.gethoehe(y.rechts))
        return y

    def linksRotation(self, x):
        y = x.rechts
        puffer = y.links
        y.links = x
        x.rechts = puffer
        x.hoehe = 1 + max(self.gethoehe(x.links),
                           self.gethoehe(x.rechts))
        y.hoehe = 1 + max(self.gethoehe(y.links),
                           self.gethoehe(y.rechts))
        return y

    def getBalance(self, wurzel):
        if not wurzel:
            return 0
        return self.gethoehe(wurzel.links) - self.gethoehe(wurzel.rechts)


    def gethoehe(self, wurzel):
        if not wurzel:
            return 0
        return wurzel.hoehe

Baum = AVLBaum()
wurzel = None

wurzel = Baum.insert(wurzel, 10)
wurzel = Baum.insert(wurzel, 5)
wurzel = Baum.insert(wurzel, -5)
wurzel = Baum.insert(wurzel, 20)
results = Baum.suche(wurzel, 20)
# print('results of suche', results)
wurzel = Baum.insert(wurzel, 30)
wurzel = Baum.insert(wurzel, 40)
wurzel = Baum.insert(wurzel, 50)
results = Baum.suche(wurzel, 70)
results = Baum.suche(wurzel, 30)
wurzel = Baum.insert(wurzel, 50)

wurzel = Baum.loeschen(wurzel, 10)
results = Baum.suche(wurzel, 30)

# results = Baum.suche(wurzel, 30)
# print('results of suche', results)
# results = Baum.suche(wurzel, 40)
# print('results of suche', results)

# results = Baum.suche(wurzel, 10)
# print('results of suche', results)

# results = Baum.suche(wurzel, 20)
# print('results of suche', results)