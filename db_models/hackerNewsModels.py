from app import db


class CommentSentimentAndTopic(db.Model):
    __tablename__ = 'sentiment_and_topic'

    id = db.Column(db.Integer, primary_key=True)
    raw_txt = db.Column(db.String())
    sentiment = db.Column(db.String())
    topic = db.Column(db.String())
