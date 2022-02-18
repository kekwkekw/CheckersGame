import pygame
import math

FPS = 60
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
LIGHTROSE = (255, 209, 220)
LIGHTPURPLE = (230, 198, 136)
BLACK = (0, 0, 0)
OPACITY = 155


def add_content_from(listfrom, listto):
    content = []
    for i in listfrom:
        if type(i) == list:
            add_content_from(i, content)
        else:
            content.append(i)
    for i in content:
        listto.append(i)

class Tale:
    def __init__(self, x, y, iswhite, isplayable=True):
        self.x = x
        self.y = y
        self._iswhite = iswhite
        self._isplayable = isplayable
        self.checker = None
        self._isvisible = False
        if self._iswhite:
            self.image = pygame.image.load("LightTale.png")
        else:
            self.image = pygame.image.load("DarkTale.png")
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.color = GRAY
        self.ishighlighted = False
        self.highlightsurface = pygame.Surface((40, 40))
        self.highlightsurface.fill(self.color)
        self.highlightsurface.set_alpha(0)

    def update(self):
        if self._isplayable:
            if self._isvisible:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image.set_alpha(OPACITY)
                else:
                    self.image.set_alpha(255)
            else:
                self.image.set_alpha(0)
        if self.ishighlighted:
            self.highlightsurface.fill(self.color)
            self.highlightsurface.set_alpha(255 - OPACITY)
        else:
            self.highlightsurface.set_alpha(0)
        screen.blit(self.image, self.rect)
        screen.blit(self.highlightsurface, (self.x * 40, self.y * 40))

    def show(self):
        self._isvisible = True

    def hide(self):
        self._isvisible = False

    def placechecker(self, checker):
        if self.checker is None:
            self.checker = checker

    def removechecker(self):
        if self.checker is not None:
            self.checker = None

    def copy(self):
        return Tale(self.x, self.y, self._iswhite, self._isplayable)

    def highlight(self, color):
        if not self.ishighlighted:
            self.color = color
            self.ishighlighted = True

    def unhighlight(self):
        if self.ishighlighted:
            self.color = None
            self.ishighlighted = False

    def __eq__(self, other):
        if type(other)!=Tale:
            return False
        elif (other.x, other.y) == (self.x, self.y):
            return True
        else:
            return False

class Checker:
    def __init__(self, iswhite, tale):
        self._iswhite = iswhite
        tale.placechecker(self)
        self.tale = tale
        self.cover = tale.copy()
        self.isplayable = True
        self.x = self.tale.x
        self.y = self.tale.y
        self.isvisible = True
        self.ishighlighted = False
        self.color = BLACK
        self.highlightsurface = pygame.Surface((40, 40))
        self.highlightsurface.fill(self.color)
        self.highlightsurface.set_alpha(0)
        if self._iswhite:
            self.image = pygame.image.load("White.png")
        else:
            self.image = pygame.image.load("Black.png")
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.image.set_alpha(255)
        self.playabletales = []
        self.isbeating = False
        self.isdamka = False
        self.canbeat = False
        self.pathlist = self.find_possible_tales(self.tale, True, True)

    def copy(self):
        return Checker(self._iswhite, self.tale)

    def find_possible_tales(self, st,
                            chi,
                            ok,
                            showweight = False):
        weight = []
        if not self.isdamka:
            path = []
            x = st.x
            y = st.y
            for i in [-1, 1]:
                for j in [-1, 1]:
                    possibletale = tales[x + i][y + j]
                    if possibletale._isplayable:
                        if possibletale.checker is None:
                            if chi:
                                if (self._iswhite and j < 0) or (not self._iswhite and j > 0):
                                    path.append(possibletale)
                        else:
                            if possibletale.checker._iswhite != self._iswhite and ok:
                                newpossibletale = tales[x + 2 * i][y + 2 * j]
                                if newpossibletale.checker is None and newpossibletale._isplayable:
                                    path.append(newpossibletale)
                                    weight.append(newpossibletale)
            finalpath = []
            add_content_from(path, finalpath)
            if len(finalpath) != 0:
                if showweight:
                    return [finalpath,weight]
                else:
                    return finalpath
            else:
                return None
        else:
            path = []
            x = st.x
            y = st.y
            maximumne = 6
            maximumse = 6
            maximumnw = 6
            maximumsw = 6
            for k in range(1, 7):
                for i in [-k, +k]:
                    for j in [-k, +k]:
                        if (i < 0 and j < 0 and k < maximumnw) or (i < 0 < j and k < maximumsw) or (
                                i > 0 and j > 0 and k < maximumse) or (
                                i > 0 > j and k < maximumne):
                            try:
                                possibletale = tales[x + i][y + j]
                                if possibletale._isplayable:
                                    if possibletale.checker is None:
                                        if chi:
                                            path.append(possibletale)
                                    else:
                                        if possibletale.checker._iswhite == self._iswhite:
                                            if i < 0 and j < 0:
                                                maximumnw = k - 1
                                            elif i < 0 and j > 0:
                                                maximumsw = k - 1
                                            elif i > 0 and j > 0:
                                                maximumse = k - 1
                                            elif i > 0 and j < 0:
                                                maximumne = k - 1
                                        if possibletale.checker._iswhite != self._iswhite and ok:
                                            newpossibletale = tales[int(x + (k + 1) * i / abs(i))][
                                                int(y + (k + 1) * j / abs(j))]
                                            if newpossibletale.checker is None and newpossibletale._isplayable:
                                                path.append(newpossibletale)
                                            else:
                                                if i < 0 and j < 0:
                                                    maximumnw = k - 1
                                                elif i < 0 and j > 0:
                                                    maximumsw = k - 1
                                                elif i > 0 and j > 0:
                                                    maximumse = k - 1
                                                elif i > 0 and j < 0:
                                                    maximumne = k - 1
                            except IndexError:
                                if i < 0 and j < 0:
                                    maximumnw = k
                                elif i < 0 and j > 0:
                                    maximumsw = k
                                elif i > 0 and j > 0:
                                    maximumse = k
                                elif i > 0 and j < 0:
                                    maximumne = k
            finalpath = []
            add_content_from(path, finalpath)
            if len(finalpath) != 0:
                if showweight:
                    return [finalpath, weight]
                else:
                    return finalpath
            else:
                return None

    def hide(self):
        if self.isvisible:
            self.isvisible = False

    def show(self):
        if not self.isvisible:
            self.isvisible = True

    def getridof(self):
        if self.isplayable:
            self.isplayable = False

    def highlight(self, color):
        if not self.ishighlighted:
            self.color = color
            self.ishighlighted = True

    def unhighlight(self):
        if self.ishighlighted:
            self.ishighlighted = False

    def move(self, totale):
        self.tale.checker = None
        self.tale = totale
        self.tale.placechecker(self)
        self.x = self.tale.x
        self.y = self.tale.y
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))

    def bebeaten(self):
        global whites
        global blacks
        if self._iswhite:
            for i in whites:
                if i == self:
                    whites.remove(i)
        else:
            for i in blacks:
                if i == self:
                    blacks.remove(i)
        self.tale.checker = None
        self.tale = tales[0][0]
        self.cover = self.tale.copy()
        self.tale.placechecker(self)
        self.x = self.tale.x
        self.y = self.tale.y
        self.rect = self.image.get_rect(topleft=(self.x * 40, self.y * 40))
        self.isplayable = False
        self.hide()

    def beat(self, beaten_checker):
        deltax, deltay = beaten_checker.x - self.x, beaten_checker.y - self.y
        self.move(tales[int(self.x + (abs(deltax) + 1) * deltax / abs(deltax))][
                      int(self.y + (abs(deltay) + 1) * deltay / abs(deltay))])
        beaten_checker.bebeaten()
        if self.isdamka:
            self.justbeated = True

    def makeaturn(self, tale):
        global whitesturn
        if self.isdamka:
            if self._iswhite == whitesturn:
                possibletale = None
                for i in self.pathlist:
                    if tale == i:
                        possibletale = i
                if possibletale is not None:
                    deltax = (tale.x - self.x) / abs(tale.x - self.x)
                    deltay = (tale.y - self.y) / abs(tale.y - self.y)
                    beatentale = None
                    for i in range(1, abs(tale.x - self.x)+1):
                        maybetale = tales[int(self.x + deltax * i)][int(self.y + deltay * i)]
                        if maybetale.checker is not None:
                            if maybetale.checker._iswhite != self._iswhite:
                                if beatentale is None:
                                    beatentale = maybetale
                    if beatentale is None:
                        canbeat = False
                    else:
                        canbeat = True
                    if not canbeat:
                        self.move(possibletale)
                        whitesturn = not whitesturn
                    elif canbeat:
                        if possibletale.checker is None:
                            if beatentale is not None:
                                if beatentale.x <= tales[int(tale.x - deltax)][int(tale.y - deltay)].x:
                                    self.beat(beatentale.checker)
                                    self.isbeating = True
                                    self.update()
                                    if self.pathlist is None:
                                        self.isbeating = False
                                        self.justbeated = False
                                        whitesturn = not whitesturn
        else:
            if self._iswhite == whitesturn and self.pathlist is not None:
                possibletale = None
                for i in self.pathlist:
                    if tale == i:
                        possibletale = i
                if possibletale is not None:
                    if abs(possibletale.x - self.x) == 1:
                        self.move(possibletale)
                        self.maybebecomedamka()
                        whitesturn = not whitesturn
                    elif abs(possibletale.x - self.x) == 2:
                        self.beat(tales[int((possibletale.x + self.x) / 2)][int((possibletale.y + self.y) / 2)].checker)
                        self.isbeating = True
                        self.maybebecomedamka()
                        self.update()
                        if self.pathlist is None:
                            self.isbeating = False
                            whitesturn = not whitesturn


    def maybebecomedamka(self):
        if (self.tale.y == 1 and self._iswhite) or (self.tale.y == 8 and not self._iswhite):
            self.isdamka = True
            if self._iswhite:
                self.image = pygame.image.load("WhiteDamka.png")
            else:
                self.image = pygame.image.load("BlackDamka.png")

    def update(self):
        if self.isplayable:
            if self.isvisible:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.cover.image.set_alpha(255 - OPACITY)
                else:
                    self.cover.image.set_alpha(0)
            else:
                self.cover.image.set_alpha(255)
            if self.ishighlighted:
                self.highlightsurface.fill(self.color)
                self.highlightsurface.set_alpha(255 - OPACITY)
            else:
                self.highlightsurface.set_alpha(0)
            if not self.isbeating:
                self.pathlist = self.find_possible_tales(self.tale, True, True)
            else:
                self.pathlist = self.find_possible_tales(self.tale, False, True)
            screen.blit(self.image, self.rect)
            screen.blit(self.cover.image, self.rect)
            screen.blit(self.highlightsurface, self.rect)
        else:
            self.cover.image.set_alpha(255)
            screen.blit(self.cover.image, self.rect)

    def __eq__(self, other):
        if (other.x, other.y, other._iswhite) == (self.x, self.y, self._iswhite):
            return True
        else:
            return False

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 400))
tales = []
pygame.display.set_caption("Checkers")
whitesturn = True
firstclick = True
playingchecker = None
wrongtale = None
whitewins = None
for i in range(10):
    row = []
    for j in range(10):
        if i == 0 or i == 9 or j == 0 or j == 9:
            newtale = Tale(i, j, True, False)
        else:
            if i % 2 == j % 2:
                newtale = Tale(i, j, True)
            else:
                newtale = Tale(i, j, False)
            newtale.show()
        row.append(newtale)
    tales.append(row)
whites = []
blacks = []
clock = pygame.time.Clock()
for i in range(1, 5):
    for j in range(6, 9):
        if j % 2 == 1:
            newwhitechecker = Checker(True, tales[2 * i][j])
        else:
            newwhitechecker = Checker(True, tales[2 * i - 1][j])
        whites.append(newwhitechecker)

for i in range(1, 5):
    for j in range(1, 4):
        if j % 2 != 1:
            newblackchecker = Checker(False, tales[2 * i - 1][j])
        else:
            newblackchecker = Checker(False, tales[2 * i][j])
        blacks.append(newblackchecker)

running1 = True
# mainloops
while running1:
    clock.tick(FPS)
    # events
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running1 = False
        # tracking mouse position
        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        # clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.button == 1:
                clicked_tale = Tale(math.floor(mousex / 40), math.floor(mousey / 40), True, True)
                for i in tales:
                    for j in i:
                        if clicked_tale == j:
                            clicked_tale = j
                if firstclick:
                    if clicked_tale.checker is not None:
                        playingchecker = clicked_tale.checker
                        if playingchecker._iswhite == whitesturn:
                            playingchecker.highlight(GRAY)
                            if playingchecker.pathlist is not None:
                                for i in playingchecker.pathlist:
                                    i.highlight(GREEN)
                        else:
                            playingchecker.highlight(RED)
                        firstclick = False
                else:
                    if playingchecker.pathlist is not None:
                        for i in playingchecker.pathlist:
                            i.unhighlight()
                    if wrongtale is not None:
                        wrongtale.unhighlight()
                    if playingchecker.pathlist is not None:
                        if clicked_tale not in playingchecker.pathlist:
                            wrongtale = clicked_tale
                            wrongtale.highlight(RED)
                    playingchecker.makeaturn(clicked_tale)
                    if playingchecker.pathlist is not None:
                        for i in playingchecker.pathlist:
                            i.highlight(GREEN)
                    if not playingchecker.isbeating:
                        firstclick = True
                        playingchecker.unhighlight()
                        if playingchecker.pathlist is not None:
                            for i in playingchecker.pathlist:
                                i.unhighlight()

    # updates+rendering
    screen.fill(LIGHTROSE)
    for i in tales:
        for j in i:
            j.update()
    for i in whites:
        i.update()
    for i in blacks:
        i.update()
    pygame.draw.rect(screen, BLACK, (40, 40, 320, 320), 1)
    # global update
    pygame.display.flip()
    # endgame
    if len(whites) == 0:
        whitewins = False
        running1 = False
    elif len(blacks) == 0:
        whitewins = True
        running1 = False

if whitewins:
    print("Congratulations Player1!")
else:
    print("Congratulations Player2!")