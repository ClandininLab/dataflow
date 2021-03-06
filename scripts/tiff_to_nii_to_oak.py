import sys
import os
import dataflow as flow

def main(args):
    ''' mode options: tiff_to_nii, to_oak, tiff_to_nii_to_oak
    '''

    mode = args[0]
    output = args[1]
    folder = args[2]
    #oak_target = 'X:/data/Brezovec/2P_Imaging/imports'
    oak_target = 'X:/data/Ashley2/imports'
    extensions_for_oak_transfer = ['.nii', '.csv', '.xml', 'json', 'tiff'] # needs to for 4 char

    full_target = os.path.join('F:/ftp_imports', folder)
    if mode == 'tiff_to_nii':
        flow.start_convert_tiff_collections(full_target)
    elif mode == 'to_oak':
        flow.start_oak_transfer(full_target, oak_target, extensions_for_oak_transfer)
    elif mode == 'tiff_to_nii_to_oak':
        if output == 'tiff':
            flow.convert_tiff_collections_to_stack(full_target)
        elif output == 'nii':
            flow.start_convert_tiff_collections(full_target)
        else:
            print('Invalid mode')
        flow.start_oak_transfer(full_target, oak_target, extensions_for_oak_transfer)
    elif mode == 'raw_to_oak':
        flow.convert_raw_to_tiff(full_target)
        flow.start_convert_tiff_collections(full_target)
        flow.start_oak_transfer(full_target, oak_target, extensions_for_oak_transfer)
    else:
        print('Invalid mode: {}'.format(mode))
        print('Must be tiff_to_nii, to_oak, or tiff_to_nii_to_oak')

if __name__ == '__main__':
    main(sys.argv[1:])