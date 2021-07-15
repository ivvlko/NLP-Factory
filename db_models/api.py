from flask_restful import Resource, Api, reqparse, fields, marshal_with
from db_models.hackerNewsModels import TopicLabel
from app import app, db

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('raw_txt', type=str, help='Raw Text of the news')
parser.add_argument('title', type=str, help='Title of the news')
parser.add_argument('standard_ml_label', type=str, help='NB prediction of the label')
resource_fields = {
    'title': fields.String,
    'raw_txt': fields.String,
    'standard_ml_label': fields.String,
}


class HnLabelledNews(Resource):
    @marshal_with(resource_fields)
    def get(self):
        results = db.session.query(TopicLabel).order_by(TopicLabel.id.desc()).limit(5000).all()
        return results


api.add_resource(HnLabelledNews, "/hn_api/")
