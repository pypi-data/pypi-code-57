from datetime import datetime

from app import db


def format_text(text):
    return ' '.join(text.strip().split())


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer(), primary_key=True)
    route = db.Column(db.String(100))
    method = db.Column(db.String(10))
    request = db.Column(db.Text())
    response = db.Column(db.Text())
    ts = db.Column(db.DateTime(), default=datetime.utcnow)
    duration = db.Column(db.Integer())
    status_code = db.Column(db.String)
    message = db.Column(db.String)

    def __repr__(self):
        return """<log object>
        id: {}
        route: {}
        method: {}
        request: {}
        response: {}
        ts: {}
        duration: {}
        status_code: {}
        message: {}""".format(self.id, self.route, self.method, self.request, self.response, self.ts,
                              self.duration, self.status_code, self.message)

    @staticmethod
    def init(request):
        log = Log()
        log.route = request.path
        log.method = request.method
        log.request = format_text(str(request.json))
        db.session.add(log)
        db.session.commit()
        return log.id

    @staticmethod
    def complete(log_id, response):
        log = Log.query.filter_by(id=log_id).first()
        if log:
            log.response = format_text(str(response.json))
            log.duration = (datetime.utcnow() - log.ts).total_seconds()
            log.status_code = response.status
            log.message = response.json.get('message')
            db.session.add(log)
            db.session.commit()
            return True
        return False

    def delete(self):
        log = Log.query.filter_by(id=self.id).first()
        db.session.delete(log)
        db.session.commit()
