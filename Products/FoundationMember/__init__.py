from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from config import ADD_CONTENT_PERMISSION, PROJECTNAME, SKINS_DIR, GLOBALS

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import types

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

