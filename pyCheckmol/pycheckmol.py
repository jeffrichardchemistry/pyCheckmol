import subprocess
import pandas as pd

class CheckMOl:
    def __init__(self):
        self.information = ''

    def functionalGroups(self, file = '', justFGcode=True, returnDataframe=False):
        """
        This funtion returns the Functional groups (FG) information. Each FG is
        labeled with a code. Altogether there are 204 FG labeled. The table with
        this information can be viewed at .......
        
        Arguments
        ---------------------
        file
            Path to file, must be: .sdf, .mol, .mol2, .smiles.
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
        self.information = subprocess.getoutput('checkmol -v {}'.format(file))
        if justFGcode:
            get = [int(getline.replace(getline[3:], '')) for getline in get.splitlines()]
            return get
        else:
            getdf = pd.DataFrame([x.split(':') for x in get.splitlines()], columns=['FG_code', 'n_atoms', 'Atoms_label'])
            if returnDataframe:
                return getdf
            else:
                return getdf.to_dict('list')
        

if __name__ == '__main__':
    file = 'examples/mol.sdf'

    cm = CheckMOl()
    get = cm.functionalGroups(file, justFGcode=True, returnDataframe=True)
    print(get)
    

