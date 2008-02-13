from Products.Archetypes.atapi import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.FoundationMember.config import *
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility 
from Products.GenericSetup.interfaces import ISetupTool

EXTENSION_PROFILES = ('Products.FoundationMember:default',) 

import transaction

from StringIO import StringIO

def install(self):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.setChainForPortalTypes(pt_names=['FoundationMember'] , chain='foundation_member_workflow')
    print >> out, 'Set foundation_member_workflow as default for foundation members'

    ft = getToolByName(self, 'portal_factory')
    portal_factory_types = ft.getFactoryTypes().keys()
    for t in ['FoundationMember']:
        if t not in portal_factory_types:
            portal_factory_types.append(t)
    ft.manage_setPortalFactoryTypes(listOfTypeIds=portal_factory_types)
    print >> out, 'New types use portal_factory'

    portal_setup = getUtility(ISetupTool)
    quickinstaller = getToolByName(self, 'portal_quickinstaller')

    # The following section is boilerplate code that can be reused when you 
    # need to invoke a GenericSetup profile from Install.py. 
    for extension_id in EXTENSION_PROFILES: 
        portal_setup.setImportContext('profile-%s' % extension_id) 
        portal_setup.runAllImportSteps(purge_old=False) 
        product_name = extension_id.split(':')[0] 
        quickinstaller.notifyInstalled(product_name) 
        transaction.savepoint() 

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
