from app import db


class TopicLabel(db.Model):
    __tablename__ = 'hn_topic_labelling'

    id = db.Column(db.Integer, primary_key=True)
    raw_txt = db.Column(db.String())
    standard_ml_label = db.Column(db.String())
    neural_net_label = db.Column(db.String())
