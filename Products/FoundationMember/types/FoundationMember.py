# coding=utf-8

from Products.Archetypes.atapi import BaseFolder
from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import ComputedField
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import IdWidget
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import registerType
from Products.FoundationMember.config import VIEW_PF_MEMBERS_DETAIL
from Products.FoundationMember.config import MANAGE_PF_MEMBERS
from Products.FoundationMember.config import PROJECTNAME
from AccessControl import ClassSecurityInfo

schema = BaseFolderSchema + Schema((
    StringField('id',
        required=0,
        mode="rw",
        accessor="getId",
        mutator="setId",
        default=None,
        schemata='contact',
        widget=IdWidget(
            label="Short Name",
            label_msgid="label_short_name",
            description="Should not contain spaces, underscores or mixed case. "\
                    "Short Name is part of the item's web address.",
                    description_msgid="help_shortname",
                    visible={'view' : 'invisible'},
                    i18n_domain="plone"),
        ),

    ComputedField('title',
        accessor='Title',
        expression="'%s %s' % (context.getFname(), context.getLname())",
        mode='r',
        widget=StringWidget(
            modes=('view',),
            ),
        schemata='contact',
        ),
    StringField('lname',
        required=1,
        widget=StringWidget(
            label='Last Name',
            size=15
            ),
        schemata='contact',
        ),

    StringField('fname',
        required=1,
        widget=StringWidget(
            label='First Name',
            size=20
            ),
        schemata='contact',
        ),

    StringField('email',
        required=1,
        validators=('isEmail',),
        schemata='contact',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
        ),

    StringField('address',
            required=1,
            widget=StringWidget(
                label='Address',
                size=45,
                ),
            schemata='contact',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
            ),

    StringField('city',
        required=1,
        widget=StringWidget(
            label='City',
            size=25,
            ),
        schemata='contact',
        ),

    StringField('state',
        required=0,
        widget=StringWidget(
            label='State/Region',
            size=25,
            ),
        schemata='contact',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
        ),

    StringField('postalCode',
        required=1,
        widget=StringWidget(
            label='Postal Code/Zip Code',
            size=25,
            ),
        schemata='contact',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
        ),

    StringField('country',
            required=1,
            widget=SelectionWidget(
                label='Country',
                ),
            vocabulary='getCountryVocab',
            enforceVocabulary=1,
            schemata='contact',
            ),

    StringField('organization',
            required=1,
            widget=StringWidget(
                label='Organization',
                size=50,
                ),
            schemata='contact',
            ),

    TextField('merit',
            required=1,
            widget=RichWidget(
                label='Contributions',
                description='Describe your contributions to the project.',
                ),
            allowable_content_types=('text/html','text/structured','text/restructured'),
            default_content_type='text/html',
            default_output_type='text/x-html-safe',
            schemata='merit',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
            ),

    IntegerField('orgsize',
            default='',
            widget=IntegerWidget(
                label='Organization Size',
                description="Number of people in your organization. It's fine to estimate.",
                ),
            schemata='survey',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
            ),

    TextField('ploneuse',
            widget=RichWidget(
                label='Plone Use',
                description='How is Plone used by your organization?',
                ),
            allowable_content_types=('text/html','text/structured','text/restructured'),
            default_content_type='text/html',
            default_output_type='text/x-html-safe',
            schemata='survey',
        read_permission=VIEW_PF_MEMBERS_DETAIL,
            ),

    ))


class FoundationMember(BaseFolder):
    """Member of Plone Foundation"""

    schema=schema
    content_icon='user.gif'

    schemata_help={}

    schemata_help['contact']="""<p>The Plone Foundation is owned and operated by its
membership.  Becoming a member simply requires merit and this application.
After this application is submitted, the Plone Foundation's membership
committee will review it and make a recommendation on your application.</p>
<p>For any questions about Plone Foundation membership, this form, or a pending
application, please email <a href="mailto:membership-committee@lists.plone.org">membership-committee@lists.plone.org</a>.</p>"""

    schemata_help['survey']="""<p>The Plone Foundation needs information to
better serve its members and the foundation's mission. Please take the extra
time to tell us a little bit about yourself. Note: This information is used to
help us better understand our community and is <span style="font-style:
italic;">not</span> used in determining eligibility for membership.</p>"""

    schemata_help['merit']=""" <p>The Plone Foundation accepts members based on
merit. As described on the Merit Criteria page, merit is shown by enduring
contributions that benefit the general Plone community. Please describe below
your participation, including references to contributions such as code,
documentation, maintenance, marketing, or support. Explain how these
contributions are enduring and general.</p>"""

    archetype_name="Foundation Member"
    meta_type="Foundation Member"
    use_folder_contents=0
    global_allow=0
    filter_content_types=1
    allowed_content_types=()

    security = ClassSecurityInfo()

    security.declareProtected(VIEW_PF_MEMBERS_DETAIL, 'toXML')
    def toXML(self, schematas=['contact','survey']):
        """To XML for Paul ;) """

        out =""
        out += """<foundationmember id="%s">""" % self.getId()
        for f in [ f for f in self.Schema().fields() if ( f.schemata in schematas ) and f.getName()<>'id' ]:
            out += "<%s>%s</%s>" % (f.getName(), getattr(self, f.accessor)(), f.getName())
        out += "</foundationmember>"
        return out

    security.declareProtected(MANAGE_PF_MEMBERS, 'manageFdnMember')
    def manageFdnMember(self):
        """Just getting the permission registered."""
        pass

    def getCountryVocab(self):
        return DisplayList((
            ('AF','Afghanistan'),
            ('AL','Albania'),
            ('DZ','Algeria'),
            ('AS','American Samoa'),
            ('AD','Andorra'),
            ('AO','Angola'),
            ('AI','Anguilla'),
            ('AQ','Antarctica'),
            ('AG','Antigua and Barbuda'),
            ('AR','Argentina'),
            ('AM','Armenia'),
            ('AW','Aruba'),
            ('AU','Australia'),
            ('AT','Austria'),
            ('AZ','Azerbaijan'),
            ('BS','Bahamas'),
            ('BH','Bahrain'),
            ('BD','Bangladesh'),
            ('BB','Barbados'),
            ('BY','Belarus'),
            ('BE','Belgique'),
            ('BZ','Belize'),
            ('BJ','Benin'),
            ('BM','Bermuda'),
            ('BT','Bhutan'),
            ('BO','Bolivia'),
            ('BA','Bosnia and Herzegovina'),
            ('BW','Botswana'),
            ('BV','Bouvet Island'),
            ('BR','Brazil'),
            ('IO','British Indian Ocean Territory'),
            ('BN','Brunei Darussalam'),
            ('BG','Bulgaria'),
            ('BF','Burkina Faso'),
            ('BI','Burundi'),
            ('KH','Cambodia'),
            ('CM','Cameroon'),
            ('CA','Canada'),
            ('CV','Cape Verde'),
            ('KY','Cayman Islands'),
            ('CF','Central African Republic'),
            ('TD','Chad'),
            ('CL','Chile'),
            ('CN','China, mainland'),
            ('CX','Christmas Island'),
            ('CC','Cocos (Keeling) Islands'),
            ('CO','Colombia'),
            ('KM','Comoros'),
            ('CG','Congo, Republic of the'),
            ('CD','Congo, The Democratic Republic Of The'),
            ('CK','Cook Islands'),
            ('CR','Costa Rica'),
            ('CI',"Côte d'Ivoire"),
            ('HR','Croatia'),
            ('CU','Cuba'),
            ('CY','Cyprus'),
            ('CZ','Czech Republic'),
            ('DK','Denmark'),
            ('DJ','Djibouti'),
            ('DM','Dominica'),
            ('DO','Dominican Republic'),
            ('EC','Ecuador'),
            ('EG','Egypt'),
            ('SV','El Salvador'),
            ('GQ','Equatorial Guinea'),
            ('ER','Eritrea'),
            ('EE','Estonia'),
            ('ET','Ethiopia'),
            ('FK','Falkland Islands'),
            ('FO','Faroe Islands'),
            ('FJ','Fiji'),
            ('FI','Finland'),
            ('FR','France'),
            ('GF','French Guiana'),
            ('PF','French Polynesia'),
            ('TF','French Southern Territories'),
            ('GA','Gabon'),
            ('GM','Gambia'),
            ('GE','Georgia'),
            ('DE','Germany'),
            ('GH','Ghana'),
            ('GI','Gibraltar'),
            ('GR','Greece'),
            ('GL','Greenland'),
            ('GD','Grenada'),
            ('GP','Guadeloupe'),
            ('GU','Guam'),
            ('GT','Guatemala'),
            ('GN','Guinea'),
            ('GW','Guinea-Bissau'),
            ('GY','Guyana'),
            ('HT','Haiti'),
            ('HM','Heard Island and McDonald Islands'),
            ('VA','Vatican City State'),
            ('HN','Honduras'),
            ('HK','Hong Kong'),
            ('HU','Hungary'),
            ('IS','Iceland'),
            ('IN','India'),
            ('ID','Indonesia'),
            ('IR','Iran'),
            ('IQ','Iraq'),
            ('IE','Ireland'),
            ('IM','Isle of Man'),
            ('IL','Israel'),
            ('IT','Italy'),
            ('JM','Jamaica'),
            ('JP','Japan'),
            ('JO','Jordan'),
            ('KZ','Kazakhstan'),
            ('KE','Kenya'),
            ('KI','Kiribati'),
            ('KP',"Korea, North"),
            ('KR','Korea, South'),
            ('KW','Kuwait'),
            ('KG','Kyrgyzstan'),
            ('LA',"Laos"),
            ('LV','Latvia'),
            ('LB','Lebanon'),
            ('LS','Lesotho'),
            ('LR','Liberia'),
            ('LY','Libya'),
            ('LI','Liechtenstein'),
            ('LT','Lithuania'),
            ('LU','Luxembourg'),
            ('MO','Macao'),
            ('MK','Macedonia'),
            ('MG','Madagascar'),
            ('MW','Malawi'),
            ('MY','Malaysia'),
            ('MV','Maldives'),
            ('ML','Mali'),
            ('MT','Malta'),
            ('MH','Marshall Islands'),
            ('MQ','Martinique'),
            ('MR','Mauritania'),
            ('MU','Mauritius'),
            ('YT','Mayotte'),
            ('MX','Mexico'),
            ('FM','Micronesia'),
            ('MD','Moldova'),
            ('MC','Monaco'),
            ('MN','Mongolia'),
            ('MS','Montserrat'),
            ('MA','Morocco'),
            ('MZ','Mozambique'),
            ('MM','Myanmar'),
            ('NA','Namibia'),
            ('NR','Nauru'),
            ('NP','Nepal'),
            ('NL','Netherlands'),
            ('AN','Netherlands Antilles'),
            ('NC','New Caledonia'),
            ('NZ','New Zealand'),
            ('NI','Nicaragua'),
            ('NE','Niger'),
            ('NG','Nigeria'),
            ('NU','Niue'),
            ('NF','Norfolk Island'),
            ('MP','Northern Mariana Islands'),
            ('NO','Norway'),
            ('OM','Oman'),
            ('PK','Pakistan'),
            ('PW','Palau'),
            ('PS','Palestinian West Bank and Gaza'),
            ('PA','Panama'),
            ('PG','Papua New Guinea'),
            ('PY','Paraguay'),
            ('PE','Peru'),
            ('PH','Philippines'),
            ('PN','Pitcairn'),
            ('PL','Poland'),
            ('PT','Portugal'),
            ('PR','Puerto Rico'),
            ('QA','Qatar'),
            ('RE','Reunion'),
            ('RO','Roumanie'),
            ('RU','Russian Federation'),
            ('RW','Rwanda'),
            ('SH','Saint Helena'),
            ('KN','Saint Kitts and Nevis'),
            ('LC','Saint Lucia'),
            ('PM','Saint Pierre and Miquelon'),
            ('VC','Saint Vincent and the Grenadines'),
            ('WS','Samoa'),
            ('SM','San Marino'),
            ('ST','Sao Tome and Principe'),
            ('SA','Saudi Arabia'),
            ('SN','Senegal'),
            ('CS','Serbia and Montenegro'),
            ('SC','Seychelles'),
            ('SL','Sierra Leone'),
            ('SG','Singapore'),
            ('SK','Slovakia'),
            ('SI','Slovenia'),
            ('SB','Solomon Islands'),
            ('SO','Somalia'),
            ('ZA','South Africa'),
            ('ES','Spain'),
            ('LK','Sri Lanka'),
            ('SD','Sudan'),
            ('SR','Suriname'),
            ('SZ','Swaziland'),
            ('SE','Sweden'),
            ('CH','Switzerland'),
            ('SY','Syria'),
            ('TW','Taiwan'),
            ('TJ','Tajikistan'),
            ('TZ','Tanzania'),
            ('TH','Thailand'),
            ('TL','East Timor'),
            ('TG','Togo'),
            ('TK','Tokelau'),
            ('TO','Tonga'),
            ('TT','Trinidad and Tobago'),
            ('TN','Tunisia'),
            ('TR','Turkey'),
            ('TM','Turkmenistan'),
            ('TC','Turks and Caicos Islands'),
            ('TV','Tuvalu'),
            ('UG','Uganda'),
            ('UA','Ukraine'),
            ('AE','United Arab Emirates'),
            ('GB','United Kingdom'),
            ('US','United States'),
            ('UY','Uruguay'),
            ('UZ','Uzbekistan'),
            ('VU','Vanuatu'),
            ('VE','Venezuela'),
            ('VN','Viet Nam'),
            ('VG','Virgin Islands, British'),
            ('VI','Virgin Islands, U.S'),
            ('WF','Wallis and Futuna'),
            ('EH','Western Sahara'),
            ('YE','Yemen'),
            ('ZM','Zambia'),
            ('ZW','Zimbabwe'),
            ))
registerType(FoundationMember, PROJECTNAME)
