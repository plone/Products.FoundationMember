def remove(self):
    "get out of pf"


    ft = self.portal_factory
    t = ft.getFactoryTypes().keys()
    t.remove('FoundationMember')
    ft.manage_setPortalFactoryTypes(listOfTypeIds=t)
    return "done"
