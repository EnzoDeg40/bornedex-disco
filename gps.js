class GeolocationManager {
    constructor() {
        this.watchId = null;
        this.currentPosition = null;
        this.options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };
    }

    // Méthode pour activer le GPS et demander les autorisations
    activateGPS() {
        if (!navigator.geolocation) {
            console.error('La géolocalisation n\'est pas supportée par ce navigateur.');
            return;
        }
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.currentPosition = position;
                console.log('Position mise à jour:', position);
            },
            (error) => {
                console.error('Erreur de géolocalisation:', error);
            },
            this.options
        );
        console.log('GPS activé');
    }

    // Méthode pour récupérer la position actuelle avec précision
    // getCurrentPosition() {
    //     return new Promise((resolve, reject) => {
    //         if (!navigator.geolocation) {
    //             reject('La géolocalisation n\'est pas supportée par ce navigateur.');
    //             return;
    //         }
    //         navigator.geolocation.getCurrentPosition(
    //             (position) => {
    //                 this.currentPosition = position;
    //                 resolve(position);
    //             },
    //             (error) => {
    //                 reject(error);
    //             },
    //             this.options
    //         );
    //     });
    // }

    // Recupere le nom de la ville
    getCityName() {
        return new Promise((resolve, reject) => {
            if (this.currentPosition) {
                const { latitude, longitude } = this.currentPosition.coords;
                fetch(`https://api-adresse.data.gouv.fr/reverse/?lon=${longitude}&lat=${latitude}`)
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.features.length > 0) {
                            resolve(data.features[0].properties.city);
                        } else {
                            reject('Aucune ville trouvée.');
                        }
                    })
                    .catch((error) => {
                        reject(error);
                    });
            } else {
                reject('Aucune position actuelle disponible.');
            }
        });
    }

    // Méthode pour désactiver le GPS
    deactivateGPS() {
        if (this.watchId !== null) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
            console.log('GPS désactivé');
        } else {
            console.log('Le GPS n\'était pas activé.');
        }
    }
}
