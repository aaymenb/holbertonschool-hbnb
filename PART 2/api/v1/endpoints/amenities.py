from flask_restx import Namespace, Resource, fields
from ...models.amenity import Amenity
from ...services.facade import Facade

api = Namespace('amenities', description='Opérations liées aux commodités')

# Schémas pour la documentation Swagger
amenity_schema = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Identifiant unique de la commodité'),
    'name': fields.String(required=True, description='Nom de la commodité'),
    'created_at': fields.DateTime(readonly=True, description='Date de création'),
    'updated_at': fields.DateTime(readonly=True, description='Date de dernière mise à jour')
})

amenity_input = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Nom de la commodité')
})

# Service Facade pour les commodités
amenity_facade = Facade(Amenity)

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_schema)
    def get(self):
        """Liste toutes les commodités"""
        return amenity_facade.get_all()
    
    @api.doc('create_amenity')
    @api.expect(amenity_input)
    @api.marshal_with(amenity_schema, code=201)
    def post(self):
        """Crée une nouvelle commodité"""
        amenity = amenity_facade.create(**api.payload)
        return amenity, 201

@api.route('/<string:id>')
@api.param('id', 'Identifiant de la commodité')
class AmenityItem(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_schema)
    def get(self, id):
        """Récupère une commodité par son ID"""
        amenity = amenity_facade.get(id)
        if amenity is None:
            api.abort(404, f"La commodité {id} n'existe pas")
        return amenity
    
    @api.doc('update_amenity')
    @api.expect(amenity_input)
    @api.marshal_with(amenity_schema)
    def put(self, id):
        """Met à jour une commodité"""
        amenity = amenity_facade.get(id)
        if amenity is None:
            api.abort(404, f"La commodité {id} n'existe pas")
        updated_amenity = amenity_facade.update(id, **api.payload)
        return updated_amenity 