#!/usr/bin/env python
"""
Generic Image Plotter
"""

import sys
from matplotlib import pyplot as plt
import shapelets

if __name__ == '__main__':
    from optparse import OptionParser
    o = OptionParser()
    o.set_usage('%prog [options] FITS_IMAGE')
    o.set_description(__doc__)
    o.add_option('-r', '--region', dest='region', default=None,
        help='Region of image plot, (xmin,xmax,ymin,ymax), default: None')
    o.add_option('-s', '--savefig', dest='savefig', default=None,
        help='Save the figure, requires filename')
    opts, args = o.parse_args(sys.argv[1:])

    def onclick(event):
        print('start: \tx=%d \ty=%d'%(event.xdata, event.ydata))

    def onrelease(event):
        print('end: \tx=%d \ty=%d'%(event.xdata, event.ydata))
        print('==================================')

    fn=args[0]
    if fn.split('.')[-1].lower() == 'fits':
        im,hdr=shapelets.fileio.readFITS(fn,hdr=True)
    else:
        im=shapelets.fileio.readImg(fn)
    if not (opts.region is None):
        extent=list(map(int, opts.region.split(',')))
        im=shapelets.img.selPxRange(im,[extent[2],extent[3],extent[0],extent[1]]) #numpy axis flip
    
    fig = plt.figure()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('button_release_event', onrelease)
    
    plt.title('Image')
    plt.imshow(im)
    plt.colorbar()
    plt.xlabel('X/RA')
    plt.ylabel('Y/Dec')
    print('==================================')
    if not (opts.savefig is None):
        plt.savefig(opts.savefig)
    else: plt.show()

