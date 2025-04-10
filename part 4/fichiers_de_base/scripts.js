// Fonction pour obtenir un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonction pour vérifier l'authentification
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    return token;
}

// Gestion du formulaire de connexion
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://0.0.0.0:5001/api/v1/auth/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const errorMessage = document.getElementById('error-message');
                    errorMessage.textContent = 'Échec de la connexion. Vérifiez vos identifiants.';
                }
            } catch (error) {
                console.error('Erreur:', error);
                const errorMessage = document.getElementById('error-message');
                errorMessage.textContent = 'Une erreur est survenue. Veuillez réessayer.';
            }
        });
    }
});

// Fonction pour récupérer les lieux
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://0.0.0.0:5001/api/v1/places/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Erreur lors de la récupération des lieux:', error);
    }
}

// Fonction pour afficher les lieux
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p>Prix par nuit: ${place.price_by_night}€</p>
            <a href="place.html?id=${place.id}" class="details-button">Voir les détails</a>
        `;
        placesList.appendChild(placeCard);
    });
}

// Fonction pour récupérer les détails d'un lieu
async function fetchPlaceDetails(placeId, token) {
    try {
        const response = await fetch(`http://0.0.0.0:5001/api/v1/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            fetchReviews(placeId, token);
        }
    } catch (error) {
        console.error('Erreur lors de la récupération des détails:', error);
    }
}

// Fonction pour afficher les détails d'un lieu
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    placeDetails.innerHTML = `
        <h2>${place.name}</h2>
        <div class="place-info">
            <p>${place.description}</p>
            <p>Prix par nuit: ${place.price_by_night}€</p>
            <p>Nombre de chambres: ${place.number_rooms}</p>
            <p>Nombre de salles de bain: ${place.number_bathrooms}</p>
            <p>Nombre maximum d'invités: ${place.max_guest}</p>
        </div>
    `;
}

// Fonction pour récupérer les avis
async function fetchReviews(placeId, token) {
    try {
        const response = await fetch(`http://0.0.0.0:5001/api/v1/places/${placeId}/reviews`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        }
    } catch (error) {
        console.error('Erreur lors de la récupération des avis:', error);
    }
}

// Fonction pour afficher les avis
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;

    reviewsList.innerHTML = '';
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <p>${review.text}</p>
            <p>Par: ${review.user_id}</p>
        `;
        reviewsList.appendChild(reviewCard);
    });
}

// Gestion du formulaire d'avis
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = checkAuthentication();
            if (!token) {
                window.location.href = 'login.html';
                return;
            }

            const placeId = new URLSearchParams(window.location.search).get('id');
            const reviewText = document.getElementById('review-text').value;

            try {
                const response = await fetch(`http://0.0.0.0:5001/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Erreur lors de l\'ajout de l\'avis');
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('Une erreur est survenue');
            }
        });
    }
});

// Gestion du filtre de prix
document.addEventListener('DOMContentLoaded', () => {
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const places = document.querySelectorAll('.place-card');
            
            places.forEach(place => {
                const price = parseInt(place.querySelector('p').textContent.match(/\d+/)[0]);
                if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
                    place.style.display = 'block';
                } else {
                    place.style.display = 'none';
                }
            });
        });
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    
    // Si on est sur la page d'accueil, charger les lieux
    if (document.getElementById('places-list')) {
        fetchPlaces(token);
    }
    
    // Si on est sur la page de détails, charger les détails du lieu
    const placeId = new URLSearchParams(window.location.search).get('id');
    if (placeId) {
        fetchPlaceDetails(placeId, token);
    }
}); 