from flask_restplus import fields
from analysis.api.restplus import api

blog_post = api.model('Blog post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'pub_date': fields.DateTime,
    'category_id': fields.Integer(attribute='category.id'),
    'category': fields.String(attribute='category.id'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(blog_post))
})

category = api.model('Blog category', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'name': fields.String(required=True, description='Category name'),
})

category_with_posts = api.inherit('Blog category with posts', category, {
    'posts': fields.List(fields.Nested(blog_post))
})


address = api.model('Address details', {
    'UDPRN': fields.Integer(readOnly=True, description='The unique identifier of a address'),
    'Name': fields.String(required=True, description='Name'),
    'Address1': fields.String(required=True, description='Address1'),
    'Address2': fields.String(required=True, description='Address1'),
    'Address3': fields.String(required=True, description='Address1'),
    'Address4': fields.String(required=True, description='Address1'),
    'Address5': fields.String(required=True, description='Address1'),
    'Address6': fields.String(required=True, description='Address1'),
    'Address7': fields.String(required=True, description='Address1'),
    'Address8': fields.String(required=True, description='Address1'),
    'Address9': fields.String(required=True, description='Address1'),
    'Address10': fields.String(required=True, description='Address1'),
    'created': fields.DateTime,
})

