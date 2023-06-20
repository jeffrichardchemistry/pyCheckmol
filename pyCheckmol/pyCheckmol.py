import subprocess
import os
import pandas as pd
import numpy as np

ABSOLUT_PATH = os.path.dirname(os.path.realpath(__file__))

class CheckMol:
    def __init__(self):
        self.information_ = ''

    def functionalGroupASbitvector(self, smiles = ''):
        """This function returns a array of 0's and 1's that
        represents the presence or absence of a functional group.
        The first position of this array is always 0, because python
        start a array as index 0. Here we Following the table 1-204 
        (index) 

        Args:
            smiles (str, optional): Smiles as a string.
        """
        get_list = self.functionalGroupSmiles(smiles=smiles)
        vet = np.zeros(205)
        vet[get_list] = 1
        
        return vet
        
    def functionalGroupSmiles(self, smiles = '', isString=True, generate3D=False,justFGcode=True, returnDataframe=True, deleteTMP=True):
        """
        This funtion returns the Functional groups (FG) information. Each FG is
        labeled with a code. Altogether there are 204 FG labeled. The table with
        this information can be viewed at 
        https://github.com/jeffrichardchemistry/pyCheckmol/blob/master/examples/fgtable.pdf
        
        Arguments
        ---------------------
        smiles
             or a Path to file, file must be a smiles extension: .smiles or .smi.
        isString
            If True a string must be passed in `smiles` argument, otherwise `smiles` argument
            must be a path
        generate3D
            If true the smiles will be converted into a sdf with 3D coordinates.
            Openbabel run in backend. If False will be converted with 2D coordinates.
        justFGcode
            if True return just code of FG, If False return the FG's code,
            number of atoms with these code and each atoms label as a dataframe
            or dict.
        returnDataframe
            Use only justFGcode=False. If returnDataframe=False the result is a
            dictionary, if True result is a dataframe.
        deleteTMP
            If True the temporary file will be deleted. The tmp file is created
            in $HOME/.pycheckmoltmp/
        """

        homedir = os.getenv("HOME")+'/.pycheckmoltmp/'
        if isString:
            f = open(homedir+'smitmp.smiles', 'w')
            f.write(smiles)
            f.close()

            smiles = homedir+'smitmp.smiles'
        
        if generate3D:
            smi2sdf = subprocess.getoutput('obabel {} -O {}tmp.sdf --gen3D'.format(smiles, homedir))
            fg = CheckMol.functionalGroups(self, file=homedir+'tmp.sdf', justFGcode=justFGcode, returnDataframe=returnDataframe)
            if deleteTMP:
                os.remove(homedir+'tmp.sdf')
            else:
                pass
            return fg
        else:
            smi2sdf = subprocess.getoutput('obabel {} -O {}tmp.sdf --gen2D'.format(smiles, homedir))
            fg = CheckMol.functionalGroups(self, file=homedir+'tmp.sdf', justFGcode=justFGcode, returnDataframe=returnDataframe)
            if deleteTMP:
                os.remove(homedir+'tmp.sdf')
                os.remove(homedir+'smitmp.smiles')
            else:
                pass
            return fg


    def functionalGroups(self, file = '', justFGcode=True, returnDataframe=True):
        """
        This funtion returns the Functional groups (FG) information. Each FG is
        labeled with a code. Altogether there are 204 FG labeled. The table with
        this information can be viewed at 
        https://github.com/jeffrichardchemistry/pyCheckmol/blob/master/examples/fgtable.pdf
        
        Arguments
        ---------------------
        file
            Path to file, must be: .sdf, .mol, .mol2
        justFGcode
            if True return just code of FG, If False return the FG's code,
            number of atoms with these code and each atoms label as a dataframe
            or dict.
        returnDataframe
            Use only justFGcode=False. If returnDataframe=False the result is a
            dictionary, if True result is a dataframe.
        """
        get = subprocess.getoutput('checkmol -p {}'.format(file))
        get = get.replace('#','')
        self.information_ = subprocess.getoutput('checkmol -v {}'.format(file))
        if justFGcode:
            get = [int(getline.replace(getline[3:], '')) for getline in get.splitlines()]
            return get
        else:
            getdf = pd.DataFrame([x.split(':') for x in get.splitlines()], columns=['FG_code', 'n_atoms', 'Atoms_label'])
            
            path2fulltable = '{}/data/fg_list.csv'.format(ABSOLUT_PATH)
            dftable = pd.read_csv(path2fulltable,sep=';')
            
            index2get = getdf['FG_code'].values.astype(int) - 1
            df_filteredTable = dftable.iloc[index2get,:].reset_index(drop=True)
            getdf = pd.concat([getdf,df_filteredTable.iloc[:,[1,2]]],axis=1,ignore_index=True)
            getdf.columns = ['Functional Group Number', 'Frequency', 'Atom Position', 'Functional Group', 'Code']
            getdf = getdf[['Functional Group','Frequency','Atom Position','Functional Group Number','Code']]
            if returnDataframe:
                return getdf
            else:
                return getdf.to_dict('list')
        

#Argsparse
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-smi',"--smiles", help="Type molecules smiles. Ex: 'CC(=O)OC'")
    parser.add_argument('-p', "--path", help="Type a path to molecules file.")
    args = parser.parse_args()
    
    cm = CheckMol()
    if args.smiles != None:
        res = cm.functionalGroupSmiles(smiles=args.smiles, isString=True, generate3D=False, justFGcode=False, returnDataframe=True,deleteTMP=True)
        print(res)
    elif args.path != None:
        res = cm.functionalGroups(file=args.path, justFGcode=False,returnDataframe=True)
        print(res)
    
"""if __name__ == '__main__':
    smi = 'CC1(C(N2C(S1)C(C2=O)NC(=O)C(C3=CC=C(C=C3)O)N)C(=O)O)C'
    cm = CheckMol()
    #get = cm.functionalGroups(file, justFGcode=True, returnDataframe=False)
    #print(get)

    info = cm.functionalGroupSmiles(smiles=smi, isString=True, generate3D=False, justFGcode=False, returnDataframe=True,deleteTMP=False)
    print(info)
    #cm.functionalGroupASbitvector(smi)"""

