from chalice import Chalice, Response

from classifier import FlowerClassifier

app = Chalice(app_name='flowers')

@app.route('/predict', methods=['POST'], cors=True)
def index():

    request = app.current_request
    return Response(body={'values': FlowerClassifier.instance().invoke(request.raw_body)},
                    status_code=200)

