
# import necessary packages
from flask import Flask
from flask_restful import Resource, reqparse, Api

# instantiate a flask object
app = Flask(__name__)

# instantiate an api object
api = Api(app)

# setting the location of sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'

# adding configurations for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# import necessary classes from base
from base import Movies, db

# link app object to movies database
db.init_app(app)
app.app_context().push()

# create databases
db.create_all()


class MoviesList(Resource):

    # Instantiating a parser object to hold data from message payload
    parser = reqparse.RequestParser()
    parser.add_argument('director', type=str, required=False, help='Director of the movie')
    parser.add_argument('genre', type=str, required=False, help='Genre of the movie')
    parser.add_argument('collection', type=int, required=True, help='Gross collection of the movie')

# Creating the get method
    def get(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            return item.json()
        return {'Message': 'Movie is not found'}

    # Creating the post method
    def post(self, movie):
        if Movies.find_by_title(movie):
            return {' Message': 'Movie with the  title {} already exists'.format(movie)}

        args = MoviesList.parser.parse_args()
        item = Movies(movie, args['director'], args['genre'], args['collection'])

        item.save_to()
        return item.json()

    # Creating the put method
    def put(self, movie):
        args = MoviesList.parser.parse_args()
        item = Movies.find_by_title(movie)
        if item:
            item.collection = args['collection']
            item.save_to()
            return {'Movie': item.json()}
        item = Movies(movie, args['director'], args['genre'], args['collection'])
        item.save_to()
        return item.json()

    # Creating the delete method
    def delete(self, movie):
        item = Movies.find_by_title(movie)
        if item:
            item.delete_()
            return {'Message': '{} has been deleted from records'.format(movie)}
        return {'Message': '{} is already not on the list'.format()}


# Creating a class to get all the movies from the database.
class AllMovies(Resource):

    # Defining the get method
    def get(self):
        return {'Movies': list(map(lambda x: x.json(), Movies.query.all()))}


# Adding the URIs to the api
api.add_resource(AllMovies, '/')
api.add_resource(MoviesList, '/<string:movie>')
if __name__=='__main__':
    # Run the applications
    app.run()
