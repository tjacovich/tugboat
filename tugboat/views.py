# encoding: utf-8
"""
Views
"""

from client import client
import traceback
from flask import redirect, current_app, request, abort, render_template
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser
import urllib
from datetime import datetime
import calendar

class IndexView(Resource):
    """
    Return the index page. This is temporary until the app is deployed on its
    own instance.
    """
    def get(self):
        """
        HTTP GET request
        :return: index html page
        """
        return current_app.send_static_file('index.html')


class SimpleClassicView(Resource):
    """for testing, show ads page with single input text field"""
    def get(self):
        return current_app.send_static_file('classic_w_BBB_button.html')

class ComplexClassicView(Resource):
    """for testing, show standard ads search page"""
    def get(self):
        return current_app.send_static_file('fielded_classic_w_BBB_button.html')

class ComplexClassicArXivView(Resource):
    """for testing, show standard ads search page with arXiv classes visible"""
    def get(self):
        return current_app.send_static_file('preprint_service_w_BBB_button.html')

class ComplexClassicPhysicsView(Resource):
    """for testing, show standard ads search page with physics classes visible"""
    def get(self):
        return current_app.send_static_file('physics_service_w_BBB_button.html')

class TranslationValue():
    """simple singleton container class to hold translation components

    functions that translation specific parameters typically augment the TranslationValue
    """

    # consider adding field for sort order and other args
    def __init__(self):
        self.search = []
        self.filter= []
        self.error_message = []
        self.warning_message = []
        self.sort = ''

class ClassicSearchRedirectView(Resource):
    """
    End point converts classic search to bumbblebee, returns an http redirect

    Where possible, returned query should be human readable and illustrate what a good query looks like
    """

    def __init__(self):
        super(ClassicSearchRedirectView, self).__init__()
        self.translation = TranslationValue()


        # all the parameters from classic
        # typically integer fields must be represented by Field to allow None values
        # some of these need use type fields.List
        self.api = {
            # the following we currently translate
            'article_sel': fields.Str(required=False),
            'aut_logic': fields.Str(required=False),
            'aut_xct': fields.Str(required=False),
            'author': fields.Str(required=False),
            'data_link': fields.Str(required=False),
            'db_key': fields.Str(required=False),
            'end_entry_day': fields.Field(required=False),
            'end_entry_mon': fields.Field(required=False),
            'end_entry_year': fields.Field(required=False),
            'end_mon': fields.Field(required=False),
            'end_year': fields.Field(required=False),
            'jou_pick': fields.Str(required=False),
            'obj_logic': fields.Str(required=False),
            'object': fields.Str(required=False),
            'open_link': fields.Str(required=False),
            'preprint_link': fields.Str(required=False),
            'qsearch': fields.Str(required=False),
            'return_req': fields.Str(required=False),
            'start_entry_day': fields.Field(required=False),
            'start_entry_mon': fields.Field(required=False),
            'start_entry_year': fields.Field(required=False),
            'start_mon': fields.Field(required=False),
            'start_year': fields.Field(required=False),
            'text': fields.Str(required=False),
            'txt_logic': fields.Str(required=False),
            'title': fields.Str(required=False),
            'ttl_logic': fields.Str(required=False),

            # implementations for the following just create errors
            # perhaps because there is no ads/bumbleebee support yet
            'nr_to_return': fields.Field(required=False),
            'start_nr': fields.Field(required=False),

            # golnaz - 3/5/2018
            'article_link': fields.Str(required=False),
            'gif_link': fields.Str(required=False),
            'article': fields.Str(required=False),
            'simb_obj': fields.Str(required=False),
            'ned_obj': fields.Str(required=False),
            'data_and': fields.Str(required=False),
            'toc_link': fields.Str(required=False),
            'pds_link': fields.Str(required=False),
            'multimedia_link': fields.Str(required=False),
            'ref_link': fields.Str(required=False),
            'citation_link': fields.Str(required=False),
            'associated_link': fields.Str(required=False),
            'lib_link': fields.Str(required=False),
            'ar_link': fields.Str(required=False),
            'aut_note': fields.Str(required=False),
            'spires_link': fields.Str(required=False),
            'group_and': fields.Str(required=False),
            'group_sel': fields.Str(required=False),
            'abstract': fields.Str(required=False),
            'sort': fields.Str(required=False),
            'aut_wt': fields.Field(required=False),
            'obj_wt': fields.Field(required=False),
            'ttl_wt': fields.Field(required=False),
            'txt_wt': fields.Field(required=False),
            'aut_wgt': fields.Str(required=False),
            'obj_wgt': fields.Str(required=False),
            'ttl_wgt': fields.Str(required=False),
            'txt_wgt': fields.Str(required=False),
            'aut_syn': fields.Str(required=False),
            'ttl_syn': fields.Str(required=False),
            'txt_syn': fields.Str(required=False),
            'aut_sco': fields.Str(required=False),
            'ttl_sco': fields.Str(required=False),
            'txt_sco': fields.Str(required=False),
            'aut_req': fields.Str(required=False),
            'obj_req': fields.Str(required=False),
            'ttl_req': fields.Str(required=False),
            'txt_req': fields.Str(required=False),
            'ref_stems': fields.Str(required=False),
            'arxiv_sel': fields.Str(required=False),

            # these can be ignored, at least for now
            'sim_query': fields.Str(required=False),
            'ned_query': fields.Str(required=False),
            'mail_link': fields.Str(required=False),
            'gpndb_obj': fields.Str(required=False),
            'min_score': fields.Str(required=False),
            'lpi_query': fields.Str(required=False),
            'iau_query': fields.Str(required=False),
            'data_type': fields.Str(required=False),
            'adsobj_query': fields.Str(required=False),

            # and the following are not yet translated
            'kwd_wt': fields.Field(required=False),
            'full_wt': fields.Field(required=False),
            'aff_wt': fields.Field(required=False),
            'full_syn': fields.Str(required=False),
            'aff_syn': fields.Str(required=False),
            'kwd_wgt': fields.Str(required=False),
            'full_wgt': fields.Str(required=False),
            'aff_wgt': fields.Str(required=False),
            'kwd_sco': fields.Str(required=False),
            'full_sco': fields.Str(required=False),
            'aff_sco': fields.Str(required=False),
            'kwd_req': fields.Str(required=False),
            'full_req': fields.Str(required=False),
            'aff_req': fields.Str(required=False),
            'aut_logic': fields.Str(required=False),
            'obj_logic': fields.Str(required=False),
            'kwd_logic': fields.Str(required=False),
            'ttl_logic': fields.Str(required=False),
            'txt_logic': fields.Str(required=False),
            'full_logic': fields.Str(required=False),
            'aff_logic': fields.Str(required=False),

            }


    def get(self):
        """
        return 302 to bumblebee
        """
        try:
            current_app.logger.info('Classic search redirect received data, headers: {}'.format(request.headers))
            bbb_url=current_app.config['BUMBLEBEE_URL']
            bbb_query = self.translate(request)
            redirect_url = bbb_url + '/#search/'+ bbb_query
            current_app.logger.info('translated classic {} to bumblebee {}, {}'.format(request, bbb_query, redirect_url))
            # golnaz 3/11/2018
            # while testing and using curl to see the build url after redirect call, noticed that url gets html encoded,
            # and in particular & become &amp; that BBB does not like, hence switched to render_template to tell it that
            # the url is safe and not encode it
            # but then while testing classic template, realized no encoding was done and so switched back, since
            # it felt redirect was faster and unnoticeable compared to render_template
            return redirect(redirect_url, code=302)
            #return render_template('redirect.html', url=redirect_url), 200
        except Exception as e:
            current_app.logger.error(e.message)
            current_app.logger.error(traceback.format_exc())
            return '<html><body><h2>Error translating classic query</h2> ' + e.message + '<p>' + traceback.format_exc() + '<p>' + str(request) + '</body></html>'


    def parse(self, request):
        """
        Parse the input parameter
        """
        args = parser.parse(self.api, request)
        # group_sel is a special case since we could have repeated entries, (i.e., &group_sel=ARI&group_sel=ESO%2FLib&group_sel=HST)
        # hence need to extract them to a list, and then turn it to a string, since calling parser.parse only parses the first element
        group_sel = request.args.getlist('group_sel', type=str)
        if len(group_sel) > 0:
            args['group_sel'] = ','.join(group_sel)
        # similarly db_key
        db_key = request.args.getlist('db_key', type=str)
        if len(db_key) > 0:
            args['db_key'] = ','.join(db_key)
        # and arxiv_sel
        arxiv_sel = request.args.getlist('arxiv_sel', type=str)
        if len(arxiv_sel) > 0:
            args['arxiv_sel'] = ','.join(arxiv_sel)
        return args

    def translate(self, request):
        """
        Convert all classic search related parameters to ads/bumblebee
        """
        args = self.parse(request)
        # functions to translate/process specific parameters
        # consider using reflection to obtain this list
        funcs = [self.translate_authors, self.translate_pubdate,
                 self.translate_entry_date, self.translate_results_subset,
                 self.translate_return_req, self.translate_article_sel,
                 self.translate_qsearch, self.translate_database,
                 self.translate_property_filters, self.translate_jou_pick,
                 self.translate_data_entries, self.translate_group_sel,
                 self.translate_sort, self.translate_to_ignore,
                 self.translate_weights, self.translate_arxiv_sel,
                 self.translate_ref_stems,
                 ]
        for f in funcs:
            f(args)  # each may contribute to self.translation singleton

        # functions to deal with the simple cases where only parameter name changes
        self.translate_simple(args, 'object', 'object')
        self.translate_simple(args, 'title', 'title')
        self.translate_simple(args, 'text', 'abs')

        # combine translation fragments in self.translation to ads/bumblebee parameter string
        if len(self.translation.search) == 0:
            self.translation.search = ['*:*']
        solr_query = 'q=' + ' '.join(self.translation.search)
        if len(self.translation.filter) > 0:
            solr_query += '&fq=' + '&fq='.join(self.translation.filter)
        if len(self.translation.sort) > 0:
            solr_query += '&sort=' + self.translation.sort
        if len(self.translation.error_message) > 0:
            solr_query += '&error_message=' + '&error_message='.join(self.translation.error_message)
        if len(self.translation.warning_message):
            solr_query += '&warning_message=' + '&warning_message='.join(self.translation.warning_message)
        if len(args.keys()):
            # the functions that translate individual parameters use pop to remove parameters from arg list
            # here if there are unprocessed parameters
            # pass their names out ads/bumblebee
            solr_query += '&unprocessed_parameter=' + urllib.quote('Parameters not processed: ' + ' '.join(args.keys()))

        return solr_query


    @staticmethod
    def author_exact(args):
        """given an aut_xct value, is it true"""
        value = args.pop('aut_xct', None)
        if value:
            if 'YES' == str(value).upper():
                return True
        return False

    @staticmethod
    def get_logic(classic_param, args):
        """given a logic parameter, return its value canonical form"""
        classic_param_to_logic = {'author': 'aut_logic', 'title': 'ttl_logic',
                                  'text': 'txt_logic', 'object': 'obj_logic'}
        if classic_param in args:
            logic_param = classic_param_to_logic[classic_param]
            value = args.pop(logic_param, None)
            if value:
                value = value.upper()
            return value
        return ''

    @staticmethod
    def supplied(value):
        """check html parameter to see if it is valid"""
        if value is None or (isinstance(value, basestring) and len(value) == 0):
            return False
        return True

    def translate_authors(self, args):
        """return string with all author search elements

        classic ui allows different and/or between authors and objects so we handle 
        just the author affecting elements here
        """
        connector = ' AND '
        search = ''
        logic = self.get_logic('author', args)
        exact = self.author_exact(args)
        if logic == 'OR':
            connector = ' OR '
        author_field = 'author:'
        if exact:
            author_field = '=author:'
        # one lone parameter should hold all authors from classic
        authors_str = args.pop('author', None)
        if authors_str:
            authors = self.classic_field_to_array(authors_str)
            search += urllib.quote(author_field) + '('
            for author in authors:
                if len(author) > 1:
                    # make sure user has not specified double quotes, and then put author in double quote
                    search += urllib.quote('"' + author.replace('"', '') + '"' + connector)
            search = search[:-len(urllib.quote(connector))]  # remove final
            search += ')'
            self.translation.search.append(search)

    def translate_simple(self, args, classic_param, bbb_param):
        """process easy to translate fields like title

        simply change name of parameter and use boolean connector
        """
        connector = ' AND '
        search = ''
        logic = self.get_logic(classic_param, args)
        if logic == 'OR':
            connector = ' OR '
        # one lone parameter should hold all authors from classic
        classic_str = args.pop(classic_param, None)
        if classic_str:
            terms = ClassicSearchRedirectView.classic_field_to_array(classic_str)
            search += urllib.quote(bbb_param + ':') + '('
            for term in terms:
                search += urllib.quote(term + connector)
            search = search[:-len(urllib.quote(connector))]  # remove final connector
            search += ')'
            self.translation.search.append(search)

    def translate_pubdate(self, args):
        """translate string with pubdate element

        for pubdate date search, only start or end need be specified
        at least one start year or end year must be provided
        unlike entry date search, negative offsets are not supported
        in classic, 2 digit years were permitted
        bumblebee example: pubdate:[1990-01 TO 1990-02]
        """

        start_year = args.pop('start_year', None)
        end_year = args.pop('end_year', None)
        start_month = args.pop('start_mon', None)
        end_month = args.pop('end_mon', None)

        if self.supplied(start_year) is False and self.supplied(end_year) is False:
            return

        # if start is not provided, use beginning of time
        if not self.supplied(start_year):
            start_year = 0
        if not self.supplied(start_month):
            start_month = 1

        # if end is not provided, use now
        if not self.supplied(end_year):
            tmp = datetime.now()
            end_year = tmp.year
            if not self.supplied(end_month):
                end_month = tmp.month
        else:
            if not self.supplied(end_month):
                end_month = 12

        start_year = int(start_year)
        start_month = int(start_month)
        end_year = int(end_year)
        end_month = int(end_month)
        # Y10k problem, but for 2 digit years we want to be clear what years we are searching
        search = 'pubdate' + urllib.quote(':[{:04d}-{:02d} TO {:04d}-{:02}]'.format(start_year, start_month,
                                                                                    end_year, end_month))
        self.translation.search.append(search)

    def translate_entry_date(self, args):
        """ return string for pubdate element

        like pubdate search, only start on end need be specified
        bumblebee does not yet implement, assume to follow pubdate 
        """
        start_year = args.pop('start_entry_year', None)
        end_year = args.pop('end_entry_year', None)
        start_month = args.pop('start_entry_mon', None)
        start_day = args.pop('start_entry_day', None)
        end_month = args.pop('end_entry_mon', None)
        end_day = args.pop('end_entry_day', None)

        if self.supplied(start_year) is False and self.supplied(end_year) is False:
            return  # nothing to do

        # if start is not provided, use beginning of time
        if not self.supplied(start_year):
            start_year = 0
        if not self.supplied(start_month):
            start_month = 1
        if not self.supplied(start_day):
            start_day = 1

        # if end is not provided, use now
        if not self.supplied(end_year):
            tmp = datetime.now()
            end_year = tmp.year
            if not self.supplied(end_month):
                end_month = tmp.month
            if not self.supplied(end_day):
                end_day = tmp.day
        else:
            if not self.supplied(end_month):
                end_month = 12
            if not self.supplied(end_day):
                # get last day of end month/year
                end_day = calendar.monthrange(end_year, end_month)[1]

        start_year = int(start_year)
        start_month = int(start_month)
        start_day = int(start_day)
        end_year = int(end_year)
        end_month = int(end_month)
        end_day = int(end_day)
        search = 'entry_date' + \
            urllib.quote(':[{:04d}-{:02d}-{:02d} TO {:04d}-{:02}-{:02d}]'.format(start_year, start_month, start_day,
                                                                                 end_year, end_month, end_day))
        self.translation.search.append(search)

    def validate_db_key(self, db_key):
        """Validate database selections"""
        valid_db_key = ['AST', 'PHY', 'PRE']
        if len(db_key) == 0:
            return False
        entry = db_key.split(',')
        for e in entry:
            if e not in valid_db_key:
                return False
        return True

    def translate_database(self, args):
        """translate which database to use

        only support for ast and phy, bbb does not support arxiv value, classic does not support general
        """
        dict_db = {'AST': 'astronomy',
                   'PHY': 'physics',
                   'PRE': 'e-prints'}
        value = args.pop('db_key', None)
        if value is None:
            return
        if self.validate_db_key(value):
            # if all entries are valid include them, anding them
            db_key = ''
            entry = value.split(',')
            for e in entry:
                if e != 'PRE':
                    if len(db_key) > 0:
                        db_key += ' AND '
                    db_key += 'database:"' + dict_db[e] + '"'
            if len(db_key) > 0:
                self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_database}') + \
                                               '&fq_database=(' + urllib.quote(db_key) + ')')
        else:
            # unrecognizable value
            self.translation.error_message.append(urllib.quote('Invalid database from classic {}'.format(value)))

    def translate_results_subset(self, args):
        """subset/pagination currently not supported by bumblebee

        provide error message if pagination request is present"""
        number_to_return = args.pop('nr_to_return', None)
        start_nr = args.pop('start_nr', None)
        # golnaz: hold off for now
        # if number_to_return or start_nr:
        #     self.translation.error_message.append(urllib.quote('Result subset/pagination is not supported'))

    def translate_jou_pick(self, args):
        """translate for refereed, non-refereed"""
        jou_pick = args.pop('jou_pick', None)
        if jou_pick is None:
            # if not provided, include everything in results, which is default
            pass
        elif jou_pick == 'ALL':
            # include everything in results, which is default
            pass
        elif jou_pick == 'NO':
            # only include refereed journals
            self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_property}') + \
                                           '&fq_property=(' + urllib.quote('property:("refereed")') + ')')
        elif jou_pick == 'EXCL':
            # only include non-refereed
            self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_property}') + \
                                           '&fq_property=(' + urllib.quote('property:("not refereed")') + ')')
        else:
            self.translation.error_message.append(urllib.quote('Invalid value for jou_pick: {}'.format(jou_pick)))

    def translate_data_entries(self, args):
        """ Convert all classic data entries search related parameters to ads/bumblebee """
        dict_entries = {'article_link'    : 'esources:("PUB_PDF" OR "PUB_HTML" OR "AUTHOR_PDF" OR "AUTHOR_HTML" OR "ADS_PDF" OR "ADS_SCAN")',
                        'gif_link'        : 'esources:("ADS_SCAN")',
                        'article'         : 'esources:("PUB_PDF" OR "PUB_HTML")',
                        'preprint_link'   : 'esources:("EPRINT_HTML")',
                        'toc_link'        : 'property:("TOC")',
                        'ref_link'        : 'reference:(*)',
                        'citation_link'   : 'citation_count:[1 TO *]',
                        'associated_link' : 'property:("ASSOCIATED")',
                        'simb_obj'        : 'data:("simbad")',
                        'ned_obj'         : 'data:("ned")',
                        'pds_link'        : 'property:("PDS")',
                        'aut_note'        : 'property:("NOTE")',   # need to verify this later, it is being implemented 3/12
                        'lib_link'        : 'property:("LIBRARYCATALOG")',
                        'ar_link'         : 'read_count:[1 TO *]',
                        'multimedia_link' : 'property:("PRESENTATION")',
                        'spires_link'     : 'property:("INSPIRE")',
                        'abstract'        : 'abstract:(*)',
        }

        operator = self.translate_data_and(args)
        if operator is not None:
            # each may contribute to self.translation singleton
            for classic,BBB in dict_entries.iteritems():
                value = args.pop(classic, None)
                if value is None:
                    # if not provided, we do not need to include it in the result
                    pass
                elif value == 'YES':
                    # include entry, first add the operator
                    if (operator == 'NOT') or len(self.translation.search) > 0:
                        self.translation.search.append(operator)
                    self.translation.search.append(urllib.quote(BBB))
                else:
                    # unrecognizable value
                    self.translation.error_message.append(urllib.quote('Invalid value for {}: {}'.format(classic, value)))

    def translate_data_and(self, args):
        """ get bibliographic entries operator """
        data_and = args.pop('data_and', None)
        if data_and is None:
            operator = None
        elif data_and == 'ALL':
            # when 'A bibliographic entry' radio button is selected => include everything in results, which is default
            operator = None
        elif data_and == 'NO':
            # when 'At least one of the following (OR)' radio button is selected
            operator = 'OR'
        elif data_and == 'YES':
            # when 'All of the following (AND)' radio button is selected
            operator = 'AND'
        elif data_and == 'NOT':
            # when 'None of the following (NOT)' radio button is selected
            operator = 'NOT'
        else:
            operator = None
            self.translation.error_message.append(urllib.quote('Invalid value for data_and: {}'.format(data_and)))
        return operator

    def validate_group_sel(self, group_sel):
        valid_group_sel = ['ARI', 'CfA', 'CFHT', 'Chandra', 'ESO/Lib', 'ESO/Telescopes', 'Gemini', 'Herschel', 'HST',
                           'ISO', 'IUE', 'JCMT', 'Keck', 'Leiden', 'LPI', 'Magellan', 'NOAO', 'NRAO', 'NRAO/Telescopes',
                           'ROSAT', 'SDO', 'SMA', 'Spitzer', 'Subaru', 'Swift', 'UKIRT', 'USNO', 'VSGC', 'XMM']
        if len(group_sel) == 0:
            return False
        entry = group_sel.split(',')
        for e in entry:
            if e not in valid_group_sel:
                return False
        return True

    def translate_group_sel(self, args):
        """ Convert all classic group entries search related parameters to ads/bumblebee """
        operator = self.translate_group_and(args)
        if operator is not None:
            value = args.pop('group_sel', None)
            if value is None:
                return
            if self.validate_group_sel(value):
                # if all entries are valid include them, adding in the selected operator
                group_sel = ''
                entry = value.split(',')
                for e in entry:
                    if (operator == 'NOT') or len(group_sel) > 0:
                        group_sel += ' ' + operator + ' '
                    group_sel += '"' + e + '"'
                if len(group_sel) > 0:
                    self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_bibgroup_facet}') + \
                        '&fq_bibgroup_facet=(' + urllib.quote_plus('bibgroup_facet:({})'.format(group_sel)) + ')')
            else:
                # unrecognizable value
                self.translation.error_message.append(urllib.quote('Invalid value for group_sel: {}'.format(value)))

    def translate_group_and(self, args):
        """ set group entries operator """
        group_and = args.pop('group_and', None)
        if group_and is None:
            operator = None
        elif group_and == 'ALL':
            # when 'All Groups' radio button is selected => include everything in results, which is default
            operator = None
        elif group_and == 'NO':
            # when 'At least one of the following groups (OR)' radio button is selected
            operator = 'OR'
        elif group_and == 'YES':
            # when 'All of the following groups (AND)' radio button is selected
            operator = 'AND'
        else:
            operator = None
            self.translation.error_message.append(urllib.quote('Invalid value for group_and: {}'.format(group_and)))
        return operator

    def translate_return_req(self, args):
        """if return_req parameter is provided, it must be 'result' or None

        return error if any other value is supplied

        """
        return_req = args.pop('return_req', None)
        if return_req is None:
            pass
        elif return_req == 'result':
            pass
        else:
            self.translation.error_message.append(urllib.quote('Invalid value for return_req({}), should be "result"'.format(return_req)))

    def translate_property_filters(self, args):
        """filter query for property 

        several search fields translate to a Bumblebee filter query with property
        """
        to_bbb_property = {'data_link': 'data',
                           'open_link': 'OPENACCESS', 'preprint_link': 'eprint'}
        clauses = []
        for key in to_bbb_property.keys():
            if str(args.pop(key, None)).upper() == 'YES':
                value = to_bbb_property[key]
                self.translation.filter.append(urllib.quote('{{!type=aqp v=$fq_doctype}}&fq_doctype=(doctype:"{}")'.format(to_bbb_property.get(key))))

    def translate_article_sel(self, args):
        article_sel = args.pop('article_sel', None)
        if article_sel is None:
            pass
        elif article_sel == 'YES':
            # only include article journals
            self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_property}') + \
                                           '&fq_property=(' + urllib.quote("article") + ')')
        else:
            self.translation.error_message.append(urllib.quote('Invalid value for article_sel: {}'.format(article_sel)))


    def translate_qsearch(self, args):
        """translate qsearch parameter from single input form on classic_w_BBB_button.html

        return nonfielded metadata search query
        """
        qsearch = args.pop('qsearch', None)
        if qsearch:
            self.translation.search.append(qsearch)

    def translate_sort(self, args):
        """ translate sort parameter """
        dict_sort = {'SCORE'      : 'date desc, bibcode desc',
                     'AUTHOR'     : 'first_author desc',
                     'NDATE'      : 'date desc',
                     'ODATE'      : 'date asc',
                     'BIBCODE'    : 'bibcode desc',
                     'RBIBCODE'   : 'bibcode asc',
                     'ENTRY'      : 'entry_date desc',
                     'CITATIONS'  : 'citation_count desc',
                     'AUTHOR_CNT' : 'author_count desc',
                     'SBIBCODE'   : 'bibcode desc',
                     'READS'      : 'read_count desc',
                     'AR_SCORE'   : 'read_count desc',
                     'NONE'       : '',
        }

        value = args.pop('sort', None)
        if value is None:
            self.translation.sort = urllib.quote('date desc, bibcode desc')
            return

        for classic,BBB in dict_sort.iteritems():
            if value == classic:
                self.translation.sort = urllib.quote(BBB)
                return

        # unrecognizable value
        self.translation.error_message.append(urllib.quote('Invalid value for sort: {}'.format(value)))

    def translate_to_ignore(self, args):
        """ remove the fields that is being ignored """
        classic_ignored_fields = ['sim_query', 'ned_query', 'lpi_query', 'iau_query', 'min_score', 'mail_link', 'gpndb_obj',
                                  'data_type', # From Alberto 3/12 regarding data_type: we'll want it available for API queries, so it's for later
                                  'adsobj_query',
                                 ]
        for field in classic_ignored_fields:
            args.pop(field, None)

    def translate_weights(self, args):
        """ check the weight parameters """
        # these weights are checked/present as default, if they are not present add them in,
        # for ***_wt if the values have been changed, keep them in the args to be
        # reported in the unprocessed parameters to BBB otherwise
        # if they have stayed unchanged from default then remove them from args
        dict_weights_default_present = {'aut_syn'  :  'YES',
                                        'ttl_syn'  :  'YES',
                                        'txt_syn'  :  'YES',
                                        'aut_wt'   :  '1.0',
                                        'obj_wt'   :  '1.0',
                                        'ttl_wt'   :  '0.3',
                                        'txt_wt'   :  '3.0',
                                        'aut_wgt'  :  'YES',
                                        'obj_wgt'  :  'YES',
                                        'ttl_wgt'  :  'YES',
                                        'txt_wgt'  :  'YES',
                                        'ttl_sco'  :  'YES',
                                        'txt_sco'  :  'YES',
        }
        # for completeness the default absented weights are listed here,
        # basically, nothing needs to get done for absented weights, if they
        # have been selected (not default) leave them in the args
        # if they have stayed unchanged from default, they do not appear in args
        dict_weights_default_absent = {'aut_sco'  :  'YES',
                                       'aut_req'  :  'YES',
                                       'obj_req'  :  'YES',
                                       'ttl_req'  :  'YES',
                                       'txt_req'  :  'YES',
        }
        for key,value in dict_weights_default_present.iteritems():
            if key in args:
                if args[key] == value:
                    args.pop(key, None)
            else:
                args[key] = ''

    def validate_arxiv_sel(self, arxiv_sel):
        """Validate arXiv selections"""
        valid_arxiv_sel = ['astro-ph', 'cond-mat', 'cs', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
                           'math', 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph', 'q-bio']
        if len(arxiv_sel) == 0:
            return False
        entry = arxiv_sel.split(',')
        for e in entry:
            if e not in valid_arxiv_sel:
                return False
        return True

    def translate_arxiv_sel(self, args):
        """Convert all classic arXiv entries search related parameters to ads/bumblebee"""
        dict_arxiv = {'astro-ph'  :  'Astrophysics',
                      'cond-mat'  :  'Condensed Matter',
                      'cs'        :  'Computer Science',
                      'gr-qc'     :  'General Relativity and Quantum Cosmology',
                      'hep-ex'    :  'High Energy Physics - Experiment',
                      'hep-lat'   :  'High Energy Physics - Lattice',
                      'hep-ph'    :  'High Energy Physics - Phenomenology',
                      'hep-th'    :  'High Energy Physics - Theory',
                      'math'      :  'Mathematics',
                      'math-ph'   :  'Mathematical Physics',
                      'nlin'      :  'Nonlinear Sciences',
                      'nucl-ex'   :  'Nuclear Experiment',
                      'nucl-th'   :  'Nuclear Theory',
                      'physics'   :  'Physics',
                      'quant-ph'  :  'Quantum Physics',
                      'q-bio'     :  'Quantitative Biology',
        }
        value = args.pop('arxiv_sel', None)
        if value is None:
            return
        # consider arXiv only if other dbs are not selected
        filter = urllib.unquote(''.join(self.translation.filter))
        if 'database:"astronomy"' in filter or 'database:"physics"' in filter:
            return
        if self.validate_arxiv_sel(value):
            # if all entries are valid include them, oring them
            entry = value.split(',')
            # if all the classes are selected apply arxiv:(*) query
            if len(entry) == len(dict_arxiv):
                self.translation.search.append('property:(' + urllib.quote("EPRINT_OPENACCESS") + ')')
            else:
                arxiv_sel = ''
                for e in entry:
                    if len(arxiv_sel) > 0:
                        arxiv_sel += ' OR '
                    arxiv_sel += '"' + dict_arxiv[e].lower() + '"'
                self.translation.search.append('keyword:(' + urllib.quote(arxiv_sel) + ')')
        else:
            # unrecognizable value
            self.translation.error_message.append(urllib.quote('Invalid value for arxiv_sel: {}'.format(value)))

    def translate_ref_stems(self, args):
        """
        BBB: bibstem:(ApJ.. OR AJ..); classic: ref_stems="ApJ..,AJ..."
        list of comma-separated ADS bibstems to return, e.g. ref_stems="ApJ..,AJ..."
        """
        value = args.pop('ref_stems', None)
        if value is None:
            return
        # not validating, just pass it to BBB, if any bibstem has been specified
        ref_stems = ''
        if len(value) > 0:
            entry = value.split(',')
            for e in entry:
                if len(ref_stems) > 0:
                    ref_stems += ' OR '
                ref_stems += '"' + e + '"'
            if len(ref_stems) > 0:
                self.translation.filter.append(urllib.quote('{') + '!' + urllib.quote('type=aqp v=$fq_bibstem_facet}') + \
                                               '&fq_bibstem_facet=(' + urllib.quote('bibstem_facet:({})'.format(ref_stems)) + ')')

    @staticmethod
    def classic_field_to_array(value):
        """ convert authors or objects from classic to list"""
        value = urllib.unquote(value)
        value = value.replace('\r\n', ';')
        values = value.split(';')
        for i in range(0, len(values)):
            values[i] = values[i].replace('+', ' ')
            if ' ' in values[i] and (values[i].startswith('"') and values[i].endswith('"')) is False:
                # value has space and is not already surrounded by double quotes so we add quotes
                values[i] = '"' + values[i] + '"'
        return values


    
    
class BumblebeeView(Resource):
    """
    End point that is used to forward a search result page from ADS Classic
    to ADS Bumblebee
    """

    def get_post_data(self, request):
        """
        Attempt to coerce POST json data from the request, falling
        back to the raw data if json could not be coerced.
        :param request: flask.request

        :return: dict
        """
        try:
            post_data = request.get_json(force=True)
        except:
            post_data = request.values

        return post_data

    def post(self):
        """
        HTTP GET request

        There are two simple steps:
            1. Send a query to myads-service in 'store-query' that contains
               the list of bibcodes in the user's ADS Classic search
            2. Return a URL with the relevant queryid that the user can be
               forwarded to

        When the user clicks the URL, it will use execute-query to run the
        relevant query via Solr's Bigquery.

        Returns:
        302: redirect to the relevant URL

        :return: str
        """

        # Setup the data
        current_app.logger.info('Received data, headers: {}'.format(request.headers))
        data = self.get_post_data(request)

        if not isinstance(data, list):
            current_app.logger.error(
                'User passed incorrect format: {}, {}'.format(type(data), data)
            )
            abort(400)
        elif not all([isinstance(i, unicode) for i in data]):
            current_app.logger.error(
                'List contains non-unicode characters: {}'.format(data)
            )
            abort(400)

        bigquery_data = {
            'bigquery': ['bibcode\n' + '\n'.join(data)],
            'q': ['*:*'],
            'fq': ['{!bitset}']
        }

        headers = {'Authorization': 'Bearer ' + current_app.config['API_DEV_KEY']}

        # POST the query
        # https://api.adsabs.harvard.edu/v1/vault/query
        current_app.logger.info('Contacting vault/query ' + str(current_app.config['TESTING']))
        r = client().post(
        current_app.config['VAULT_QUERY_URL'],
        data=bigquery_data,
        headers = headers
        )

        if r.status_code != 200:
            current_app.logger.warning(
                'vault/query returned non-200 exit status: {}'.format(r.text)
            )
            return r.text, r.status_code, r.headers.items()

        # Get back a query id
        current_app.logger.info('vault/query returned: {}'.format(r.json()))
        query_id = r.json()['qid']

        # Formulate the url based on the query id
        redirect_url = '{BBB_URL}/#search/q=*%3A*&__qid={query_id}'.format(
            BBB_URL=current_app.config['BUMBLEBEE_URL'],
            query_id=query_id
        )
        current_app.logger.info(
            'Returning redirect: {}'.format(redirect_url)
        )

        # Return the query id to the user
        return {'redirect': redirect_url}, 200
