from flask_restx import Namespace, Resource, fields
from ...models.place import Place
from ...services.facade import Facade

api = Namespace('places', description='Opérations liées aux lieux')

# Schémas pour la documentation Swagger
place_schema = api.model('Place', {
    'id': fields.String(readonly=True, description='Identifiant unique du lieu'),
    'owner_id': fields.String(required=True, description='ID du propriétaire'),
    'name': fields.String(required=True, description='Nom du lieu'),
    'description': fields.String(description='Description du lieu'),
    'number_rooms': fields.Integer(required=True, description='Nombre de chambres'),
    'number_bathrooms': fields.Integer(required=True, description='Nombre de salles de bain'),
    'max_guest': fields.Integer(required=True, description='Nombre maximum d\'invités'),
    'price_by_night': fields.Float(required=True, description='Prix par nuit'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.Nested(api.model('Amenity', {
        'id': fields.String,
        'name': fields.String
    }))),
    'reviews': fields.List(fields.Nested(api.model('Review', {
        'id': fields.String,
        'text': fields.String,
        'user_id': fields.String
    }))),
    'created_at': fields.DateTime(readonly=True, description='Date de création'),
    'updated_at': fields.DateTime(readonly=True, description='Date de dernière mise à jour')
})

place_input = api.model('PlaceInput', {
    'owner_id': fields.String(required=True, description='ID du propriétaire'),
    'name': fields.String(required=True, description='Nom du lieu'),
    'description': fields.String(description='Description du lieu'),
    'number_rooms': fields.Integer(required=True, description='Nombre de chambres'),
    'number_bathrooms': fields.Integer(required=True, description='Nombre de salles de bain'),
    'max_guest': fields.Integer(required=True, description='Nombre maximum d\'invités'),
    'price_by_night': fields.Float(required=True, description='Prix par nuit'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

# Service Facade pour les lieux
place_facade = Facade(Place)

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_schema)
    def get(self):
        """Liste tous les lieux"""
        return place_facade.get_all()
    
    @api.doc('create_place')
    @api.expect(place_input)
    @api.marshal_with(place_schema, code=201)
    def post(self):
        """Crée un nouveau lieu"""
        place = place_facade.create(**api.payload)
        return place, 201

@api.route('/<string:id>')
@api.param('id', 'Identifiant du lieu')
class PlaceItem(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_schema)
    def get(self, id):
        """Récupère un lieu par son ID"""
        place = place_facade.get(id)
        if place is None:
            api.abort(404, f"Le lieu {id} n'existe pas")
        return place
    
    @api.doc('update_place')
    @api.expect(place_input)
    @api.marshal_with(place_schema)
    def put(self, id):
        """Met à jour un lieu"""
        place = place_facade.get(id)
        if place is None:
            api.abort(404, f"Le lieu {id} n'existe pas")
        updated_place = place_facade.update(id, **api.payload)
        return updated_place 