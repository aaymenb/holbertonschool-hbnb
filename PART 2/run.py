from api import create_app
import logging
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info("Démarrage de l'application...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'application: {str(e)}")
        raise 