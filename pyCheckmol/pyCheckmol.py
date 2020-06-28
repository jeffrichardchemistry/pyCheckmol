import subprocess
import os
import pandas as pd

class CheckMol:
    def __init__(self):
        self.information_ = ''

    def functionalGroupSmiles(self, smiles = '', isString=True, generate3D=False,justFGcode=True, returnDataframe=True, deleteTMP=True):
        """
        This funtion returns the Functional groups (FG) information. Each FG is
        labeled with a code. Altogether there are 204 FG labeled. The table with
        this information can be viewed at 
        https://github.com/jeffrichardchemistry/pyCheckmol/blob/master/examples/fgtable.pdf
        
        Arguments
        ---------------------
        smiles
            Smiles as a string or a Path to file, file must be a smiles extension: .smiles or .smi.
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
            if returnDataframe:
                return getdf
            else:
                return getdf.to_dict('list')
        

""" if __name__ == '__main__':
    #file = '/dados/programas/checkmol/mole3.sdf'
    filesmi = '/dados/programas/checkmol/mole2.smiles'
    smi = 'C1(C(C(C2(C(C1([H])[H])(C(C(=C(C2([H])[H])[H])C(=O)[H])(C(=O)[H])O[H])C([H])([H])[H])[H])(C([H])([H])[H])C([H])([H])[H])([H])[H])([H])[H]'
    cm = CheckMol()
    #get = cm.functionalGroups(file, justFGcode=True, returnDataframe=False)
    #print(get)

    smi = cm.functionalGroupSmiles(smiles=smi, isString=True, generate3D=False, justFGcode=True, returnDataframe=True,deleteTMP=False)
    print(smi) """

