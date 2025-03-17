from flask_restx import Namespace, Resource, fields
from ...models.review import Review
from ...services.facade import Facade

api = Namespace('reviews', description='Opérations liées aux avis')

# Schémas pour la documentation Swagger
review_schema = api.model('Review', {
    'id': fields.String(readonly=True, description='Identifiant unique de l\'avis'),
    'user_id': fields.String(required=True, description='ID de l\'utilisateur'),
    'place_id': fields.String(required=True, description='ID du lieu'),
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'created_at': fields.DateTime(readonly=True, description='Date de création'),
    'updated_at': fields.DateTime(readonly=True, description='Date de dernière mise à jour')
})

review_input = api.model('ReviewInput', {
    'user_id': fields.String(required=True, description='ID de l\'utilisateur'),
    'place_id': fields.String(required=True, description='ID du lieu'),
    'text': fields.String(required=True, description='Texte de l\'avis')
})

# Service Facade pour les avis
review_facade = Facade(Review)

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_schema)
    def get(self):
        """Liste tous les avis"""
        return review_facade.get_all()
    
    @api.doc('create_review')
    @api.expect(review_input)
    @api.marshal_with(review_schema, code=201)
    def post(self):
        """Crée un nouvel avis"""
        review = review_facade.create(**api.payload)
        return review, 201

@api.route('/<string:id>')
@api.param('id', 'Identifiant de l\'avis')
class ReviewItem(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_schema)
    def get(self, id):
        """Récupère un avis par son ID"""
        review = review_facade.get(id)
        if review is None:
            api.abort(404, f"L'avis {id} n'existe pas")
        return review
    
    @api.doc('update_review')
    @api.expect(review_input)
    @api.marshal_with(review_schema)
    def put(self, id):
        """Met à jour un avis"""
        review = review_facade.get(id)
        if review is None:
            api.abort(404, f"L'avis {id} n'existe pas")
        updated_review = review_facade.update(id, **api.payload)
        return updated_review
    
    @api.doc('delete_review')
    def delete(self, id):
        """Supprime un avis"""
        if review_facade.delete(id):
            return '', 204
        api.abort(404, f"L'avis {id} n'existe pas") 