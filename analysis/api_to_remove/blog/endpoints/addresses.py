import logging

from flask import request
from flask_restplus import Resource
from analysis.api.blog.business import create_blog_post, update_post, delete_post
from analysis.api.blog.serializers import address
from analysis.api.blog.parsers import pagination_arguments
from analysis.api.restplus import api
from analysis.database.models import Address


log = logging.getLogger(__name__)

ns = api.namespace('blog/address', description='Operations related to accessing address information for given postcode')

@ns.route('/<string:postcode>')
@api.response(404, 'Postcode not found.')
class PostItem(Resource):

    @api.marshal_with(address)
    def get(self, postcode):
        """
        Returns an address details for given postcode.
        """
        return Address.query.filter(Address.Postcode == postcode).one()
