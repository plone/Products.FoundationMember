approvedMembers=context.portal_catalog(Type='Foundation Member',
                                  review_state='approved', sort_on='sortable_title');
renewedMembers=[member.getObject() for member in approvedMembers
                if '2008' in member.ExpirationDate]
waitingMembers=[member.getObject() for member in approvedMembers
                if not member.getObject() in  renewedMembers]



emeritusMembers = context.portal_catalog(Type='Foundation Member',
                                         review_state='emeritus', sort_on='sortable_title')
emeritusMembers=[member.getObject() for member in emeritusMembers]



wftool = context.portal_workflow
pendingMembers = context.portal_catalog(Type='Foundation Member', 
                                        review_state='pending')
newApplications = []
renewApplications = []
againApplications = []
for member in pendingMembers:
    memberObject =  member.getObject()
    reviewHistory = wftool.getInfoFor(memberObject, 'review_history', [])
    reviewHistory = [review['action'] for review in reviewHistory 
                     if review.get('action','')]
    if 'approve' in reviewHistory:
        renewApplications.append(memberObject)
    elif 'reject' in reviewHistory:
        againApplications.append(memberObject)
    else:
        newApplications.append(memberObject)

initialMembers = context.portal_catalog(Type='Foundation Member', 
                                        review_state='initial')
initialApplications = []
rejectedApplications = []
for member in initialMembers:
    memberObject =  member.getObject()
    reviewHistory = wftool.getInfoFor(memberObject, 'review_history', [])
    reviewHistory = [review['action'] for review in reviewHistory 
                     if review.get('action','')]
    if 'reject' in reviewHistory:
        rejectedApplications.append(memberObject)
    else:
        initialApplications.append(memberObject)

def titleCompare(a, b):
    return cmp(a.Title(), b.Title())

againApplications.sort(titleCompare)
newApplications.sort(titleCompare)
renewApplications.sort(titleCompare)
renewedMembers.sort(titleCompare)
waitingMembers.sort(titleCompare)
emeritusMembers.sort(titleCompare)
initialApplications.sort(titleCompare)
rejectedApplications.sort(titleCompare)

result = dict(pendingMembers=pendingMembers, 
              againApplications=againApplications,
              newApplications=newApplications, 
              renewApplications=renewApplications,
              renewedMembers=renewedMembers,
              waitingMembers=waitingMembers,
              emeritusMembers=emeritusMembers,
              initialMembers=initialMembers,
              initialApplications=initialApplications, 
              rejectedApplications=rejectedApplications,
              )
return result
