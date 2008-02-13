from Products.Archetypes.atapi import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.FoundationMember.config import *
from Products.FoundationMember.Extensions import Workflow
from Products.CMFCore.utils import getToolByName

from StringIO import StringIO

def install(self):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    Workflow.install()
    wf_tool = getToolByName(self, 'portal_workflow')

    if not 'foundation_member_workflow' in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('foundation_member_workflow (Approval process for foundation members)',
                                   'foundation_member_workflow')
    wf_tool.updateRoleMappings()

    print >> out, 'Installed foundation_member_workflow.'

    wf_tool.setChainForPortalTypes(pt_names=['FoundationMember'] , chain='foundation_member_workflow')
    print >> out, 'Set foundation_member_workflow as default for foundation members'


    ft = getToolByName(self, 'portal_factory')
    portal_factory_types = ft.getFactoryTypes().keys()
    for t in ['FoundationMember']:
        if t not in portal_factory_types:
            portal_factory_types.append(t)
    ft.manage_setPortalFactoryTypes(listOfTypeIds=portal_factory_types)
    print >> out, 'New types use portal_factory'

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()
