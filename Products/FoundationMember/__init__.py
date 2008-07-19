from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils

from Products.FoundationMember.config import ADD_CONTENT_PERMISSION
from Products.FoundationMember.config import PROJECTNAME


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import Products.FoundationMember.types

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

