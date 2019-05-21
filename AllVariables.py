
def getAll():
    allquantlist=[]
    for var in ['num','den']:
        allquantlist.append(var+'_pf')
	allquantlist.append(var+'_calo')

    return allquantlist
