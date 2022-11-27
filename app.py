from flask import Flask, jsonify, json
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

app.app_context().push()



# Schema

class Meter(db.Model):
    __tablename__ = "meters_table"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    db.create_all()


class MeterData(db.Model):
    __tablename__ = "meter_data"
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey("meters_table.id"))
    time = db.Column(db.DateTime, server_default=db.func.now())
    value = db.Column(db.Integer)


api = Api(app)





#views
class MetersApi(Resource):
    def get(self):
        meters = Meter.query.all()
        d = {}
        for meter in meters:
                endpoint = "http://127.0.0.1:5000/meters/{0}".format(meter.id)
                d.update({meter.label: endpoint})
        return jsonify(d)


class MeterEndPoint(Resource):
    def get(self, id):
        meter_datas = MeterData.query.filter_by(meter_id=id).order_by(MeterData.time)
        d = {}
        l = []
        for meter_data in meter_datas:
            d.update({"id":meter_data.id})
            d.update({"meter_id":meter_data.meter_id})
            d.update({"time":meter_data.time})
            d.update({"value":meter_data.value})
            l.append(d)
        return jsonify(l)




api.add_resource(MetersApi, '/meters')
api.add_resource(MeterEndPoint, '/meters/<int:id>')



if __name__ == '__main__':
    app.run(debug=True)
