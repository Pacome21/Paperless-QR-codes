"""
# avery_labels.py
"""
from collections.abc import Iterator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm


# pip install reportlab 
# pip install reportlab_qrcode

# Usage:
#   label = AveryLabels.AveryLabel(5160)
#   label.open( "labels5160.pdf" )
#   label.render( RenderAddress, 30 )
#   label.close()
#
# 'render' can either pass a callable, which receives the canvas object
# (with X,Y=0,0 at the lower right) or a string "form" name of a form
# previously created with canv.beginForm().


# labels across
# labels down
# label size w/h
# label gutter across/down
# page margins left/top

labelInfo = {
    4731: (7, 27, (25.4*mm, 10*mm), (0.25*cm, 0), (0.85*cm, 1.35*cm) ),
    # 2.6 x 1 address labels
    5160: ( 3, 10, (187,  72), (11, 0), (14, 36)),
    5161: ( 2, 10, (288,  72), (0, 0), (18, 36)),
    # 4 x 2 address labels
    5163: ( 2,  5, (288, 144), (0, 0), (18, 36)),
    # 1.75 x 0.5 return address labels
    5167: ( 4, 20, (126,  36), (0, 0), (54, 36)),
    # 3.5 x 2 business cards
    5371: ( 2,  5, (252, 144), (0, 0), (54, 36)),
    #6121: ( 5,  13, (38*mm, 21*mm), (0.0*cm, 0.02*cm), (1*cm, 1*cm)),
    # used for my HP printer 6121: ( 5,  13, (38*mm, 21*mm), (0.0*cm, 0.0*cm), (1*cm, 1.1*cm)),
    6121: ( 5,  13, (38*mm, 21*mm), (1.50*mm, 1.0*mm), (8*mm, 5*mm)),
    # margin : (left, top)
}

RETURN_ADDRESS = 5167
BUSINESS_CARDS = 5371

class AveryLabel:

    def __init__(self, label, **kwargs):
        data = labelInfo[label]
        self.across = data[0]
        self.down = data[1]
        self.size = data[2]
        self.labelsep = self.size[0]+data[3][0], self.size[1]+data[3][1]
        self.margins = data[4]
        self.topDown = True
        self.debug = False
        self.pagesize = A4
        self.position = 0
        self.__dict__.update(kwargs)
        print(f"1 mm = {mm} px")
        print(f"across = {self.across} px")
        print(f"down = {self.down} px")
        print(f"size = {self.size} px")
        print(f"labelsep = {self.labelsep} px")
        print(f"margins = {self.margins} px")
        print(f"across = {self.across/mm} mm")
        print(f"down = {self.down/mm} mm")
        print(f"size = {self.size[0]/mm, self.size[1]/mm} mm")
        print(f"labelsep = {self.labelsep[0]/mm, self.labelsep[1]/mm} mm")
        print(f"margins = {self.margins[0]/mm, self.margins[1]/mm} mm")

    def open(self, filename):
        self.canvas = canvas.Canvas( filename, pagesize=self.pagesize )
        if self.debug:
            self.canvas.setPageCompression( 0 )
        self.canvas.setLineJoin(1)
        self.canvas.setLineCap(1)

    def topLeft(self, x=None, y=None):
        if x == None:
            x = self.position
        if y == None:
            if self.topDown:
                x,y = divmod(x, self.down)
            else:
                y,x = divmod(x, self.across)

        return (
            self.margins[0]+x*self.labelsep[0],
            self.pagesize[1] - self.margins[1] - (y+1)*self.labelsep[1]
        )

    def advance(self):
        self.position += 1
        if self.position == self.across * self.down:
            self.canvas.showPage()
            self.position = 0

    def close(self):
        if self.position:
            self.canvas.showPage()
        self.canvas.save()
        self.canvas = None

    # To render, you can either create a template and tell me
    # "go draw N of these templates" or provide a callback.
    # Callback receives canvas, width, height.
    #
    # Or, pass a callable and an iterator.  We'll do one label
    # per iteration of the iterator.

    def render( self, thing, count, *args ):
        assert callable(thing) or isinstance(thing, str)
        if isinstance(count, Iterator):
            return self.render_iterator( thing, count )

        canv = self.canvas
        for i in range(count):
            canv.saveState()
            canv.translate( *self.topLeft() )
            if self.debug:
                canv.setLineWidth( 0.25 )
                canv.rect( 0, 0, self.size[0], self.size[1] )
            if callable(thing):
                thing( canv, self.size[0], self.size[1], *args )
            elif isinstance(thing, str):
                canv.doForm(thing)
            canv.restoreState()
            self.advance()

    def render_iterator( self, func, iterator ):
        canv = self.canvas
        for chunk in iterator:
            canv.saveState()
            canv.translate( *self.topLeft() )
            if self.debug:
                canv.setLineWidth( 0.25 )
                canv.rect( 0, 0, self.size[0], self.size[1] )
            func( canv, self.size[0], self.size[1], chunk )
            canv.restoreState()
            self.advance()