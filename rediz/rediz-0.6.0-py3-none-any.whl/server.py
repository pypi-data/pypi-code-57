from flask_restx import Resource, reqparse
import flask


# --------------------------------------------------------------------------
#            Single stream operations
# --------------------------------------------------------------------------

single_set_parser = reqparse.RequestParser()
single_set_parser.add_argument('write_key', required=True)
single_set_parser.add_argument('values', required=True)
single_set_parser.add_argument('budget', required=True)

single_del_parser = reqparse.RequestParser()
single_del_parser.add_argument('write_key', required=True)

class SingleStreamReader:

    def __init__(self, rdz):
        super(SingleStream, self).__init__()
        self.rdz = rdz

    def get(self, name):
        """ Retrieve current value (or a derived quantity if prefix is used) """
        value = self.rdz.get(name=name)
        return flask.jsonify(value)

class SingleStream(SingleStreamReader):

    def __init__(self, rdz):
        super(SingleStreamReader, self).__init__(rdz=rdz)

    def put(self, name):
        """ Set current stream value """
        args = single_set_parser.parse_args()
        response = self.rdz.set(names=name, write_key=args["write_key"], value=args["value"], budgets=args["budget"])
        return flask.jsonify(response)

    def delete(self,name):
        """ Delete a stream """
        args = single_del_parser.parse_args()
        response = self.rdz.delete(name=name, write_key=args["write_key"])
        return flask.jsonify(response)


 # --------------------------------------------------------------------------
 #            Multiple streams operations
 # --------------------------------------------------------------------------

multi_set_parser = reqparse.RequestParser()
multi_set_parser.add_argument('names', required=True, action='split')
multi_set_parser.add_argument('write_keys', required=True, action='split')
multi_set_parser.add_argument('values', required=True, action='split')
multi_set_parser.add_argument('budgets', required=True, action='split')

multi_get_parser = reqparse.RequestParser()
multi_get_parser.add_argument('names', required=True, action='split')

multi_del_parser = reqparse.RequestParser()
multi_del_parser.add_argument('names', required=True, action='split')
multi_del_parser.add_argument('write_key', required=True)


class MultiStream(Resource):

    def __init__(self, rdz):
        super(MultiStream,self).__init__()
        self.rdz = rdz

    def put(self):
        """ Set multiple stream values """
        args = multi_set_parser.parse_args()
        fvalues = [ float(v) for v in args["values"] ]
        fbudgets = [ float(b) for b in args["budgets"] ]
        response = self.rdz.mset(names=args["names"],write_keys=args["write_keys"],values=fvalues,budgets=fbudgets)
        return flask.jsonify(response)

    def get(self):
        """ Retrieve values for multiple names """
        names = multi_get_parser.parse_args()["names"]
        values = self.rdz.mget(names=names)
        return flask.jsonify(values)

    def delete(self):
        """ Delete multiple streams """
        args = multi_set_parser.parse_args()
        response = self.rdz.mdelete(names=args["names"], write_keys=args["write_keys"] )
        return flask.jsonify(response)


multi_touch_parser = reqparse.RequestParser()
multi_touch_parser.add_argument('names', required=True, action='split')
multi_touch_parser.add_argument('write_keys', required=True, action='split')

class MultiTouch(Resource):

    def __init__(self, rdz):
        super(MultiTouch, self).__init__()
        self.rdz = rdz

    def put(self):
        """ Touch """
        args = multi_touch_parser.parse_args()
        names = args["names"]
        write_key = args["write_key"]
        budgets = args["budgets"]
        fbudgets = [float(b) for b in budgets]
        return self.rdz.mtouch(names=names, write_key=write_key, budgets=fbudgets)



# --------------------------------------------------------------------------
#           Operations on distributional predictions
# --------------------------------------------------------------------------

predictions_put_parser = reqparse.RequestParser()
predictions_put_parser.add_argument('write_key', required=True)
predictions_put_parser.add_argument('delay', required=True)
predictions_put_parser.add_argument('values', required=True, action='split')

predictions_get_parser = reqparse.RequestParser()
predictions_get_parser.add_argument('delay', required=True)
predictions_get_parser.add_argument('values', required=True, action='split')

predictions_delete_parser = reqparse.RequestParser()
predictions_delete_parser.add_argument('write_key', required=True)
predictions_delete_parser.add_argument('delay', required=True)


class Distribution(Resource):

    def __init__(self, rdz):
        super(Distribution, self).__init__()
        self.rdz = rdz

    def get(self, name, delay, values):
        """ Retrieve approximate cdf """
        args = predictions_get_parser.parse_args()
        values = [ float(v) for v in args["values"] ]
        percentiles = self.rdz.get_cdf(name=name,values=values,delay=int(args["delay"]))
        return flask.jsonify(percentiles)

    def put(self, name):
        """ Submit or overwrite existing scenarios """
        args = predictions_put_parser.parse_args()
        write_key = args["write_key"]
        delay = int(args["delay"])
        values = [float(v) for v in args["values"]]
        feedback = self.rdz.predict(name=name, write_key=write_key, delay=delay, values=values)
        return flask.jsonify(feedback)

    def delete(self, name):
        """ Withdraw scenarios """
        args = predictions_delete_parser.parse_args()
        result = self.rdz.delete_scenarios(name=name, write_key=args["write_key"], delay=int(args["delay"]))
        return flask.jsonify(result)



