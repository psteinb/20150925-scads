import argparse as ap
from skimage import io
from bootstrap_utils import *
import os
from multiprocessing import Pool

def change_and_write(_fname,_image,_args):

    value = _image
    if not _args.color_only:    
        value = random_rotate(value)
        
    if not _args.rotate_only:    
        value = random_enhance_color(value)

    #write to disk
    namebase,nameext = os.path.splitext(_fname)
    name2save = namebase+_args.name_insert+str(0)+nameext
    if not os.path.exists(name2save):
        io.imsave(name2save,value)
    else:
        for i in range(1,10):
            name2save = namebase+_args.name_insert+str(i)+nameext
            if not os.path.exists(name2save):
                io.imsave(name2save,value)
                break

    if _args.verbose:
        print name2save, " written to disk"

def wrap_change_and_write(_tuple):
    change_and_write(_tuple[0], _tuple[1], _tuple[2])
    

if __name__ == '__main__':

    parser = ap.ArgumentParser(description="""Bootstrapping tool to change a 2D image in a pseudo-random way\n
    (supported bootstraps: color channel, rotation)""")

    parser.add_argument('filenames', metavar='fname', type=str, nargs='+',
                        help='files to bootstrap')

    parser.add_argument('-v','--verbose',
                        # type=bool,
                        #nargs='?',
                        default=False,
                        action='store_true',
                        help='verbose messages (default: False)')

    parser.add_argument('-j','--num_threads',
                        default=1,
                        action='store',
                        type=int,
                        help='number of threads/processes to use (default: 1)')

    
    parser.add_argument('-c','--color_only',
                        default=False,
                        action='store_true',
                        help='perform color channel increase only (default: False)')

    parser.add_argument('-r','--rotate_only',
                        default=False,
                        action='store_true',
                        help='perform rotation only (default: False)')

    parser.add_argument('-n','--name_insert',
                        default='_e',
                        action='store',
                        type=str,
                        help='file name insertion for bootstrapped image (default: _e)')
    
    
    args = parser.parse_args()
    images = {}

    for fname in args.filenames:
        if os.path.exists(fname):
            image = None
            try:
                image = io.imread(fname)
            except :
                if args.verbose:
                    print fname, " is not an image! skipping it ..."
            else:
                images[fname] = image
        else:
            if args.verbose:
                print fname, "does not exist! skipping it ..."


    if args.num_threads > 1:
        p = Pool(args.num_threads)
        arg_list = [ (k,v,args) for (k,v) in images.iteritems() ]
        p.map(wrap_change_and_write, arg_list)
    else:
        for (k,v) in images.iteritems():
            change_and_write(k,v,args)

    
