db = new Mongo().getDB("products");
db.createUser({
    user: process.env.MONGODB_USERNAME,
    pwd: process.env.MONGODB_PASSWORD,
    roles: [
        {
            role: 'readWrite',
            db: 'products',
        },
    ],
});
db.auth(process.env.MONGODB_USERNAME, process.env.MONGODB_PASSWORD);

db.createCollection('wine', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            properties: {
                article: {
                    bsonType: 'string',
                    description: 'Product unique article',
                    maximum: 20
                },

                name: {
                    bsonType: 'string',
                    description: 'Name of product',
                    maximum: 100
                },
                
                type: {
                    bsonType: 'string',
                    description: 'Type of wine'
                },

                country: {
                    bsonType: 'string',
                    description: 'Which country\' wine is it',
                    maximum: 40
                },

                region: {
                    bsonType: 'string',
                    description: 'Region of wine production'
                },
                
                vintage_dating: {
                    bsonType: 'int',
                    description: 'Year of vintage'
                },

                winery: {
                    bsonType: 'string',
                    description: 'Name of wine manufactorer',
                    maximum: 50
                },

                alcohol: {
                    bsonType: 'double',
                    description: 'Alcohol content in wine',
                },
                
                capacity: {
                    bsonType: 'double',
                    description: 'Volume of bottle'
                },

                description: {
                    bsonType: 'string',
                    description: 'Description of wine',
                    maximum: 1000
                },

                price: {
                    bsonType: 'double',
                    description: 'Pirce per item'
                },

                items_left: {
                    bsonType: 'int',
                    description: 'How many items left in store'
                },


            },

            required: [
                'article',
                'name',
                'type',
                'country',
                'region',
                'vintage_dating',
                'winery',
                'alcohol',
                'capacity',
                'price',
                'items_left'
            ],

            title: 'Validation of wine collection'
        }
    }
});


db.createCollection('cart', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            properties: {
                client_username: {
                    bsonType: 'string',
                    description: 'Username of cart owner',
                    maximum: 30
                },

                cart_list: {
                    bsonType: 'array',
                    description: 'Cart consistance',
                    items: {
                        bsonType: 'object',
                        properties: {
                            wine: {
                                bsonType: 'objectId',
                                description: 'Reference to product'
                            },

                            amount: {
                                bsonType: 'int',
                                description: 'Amount of products in cart'
                            }
                        }
                    }
                },

            },

            required: [
                'client_username',
                'cart_list'
            ],

            title: 'Validation of cart collection'
        }
    }
});

db.wine.insertMany([
    {
        article: '137816',
        name: 'Anno Domini Cabernet Franc',
        type: 'Red Unfortified still wines',
        country: 'Italy',
        region: 'I.G.T./D.O.C. Veneto',
        vintage_dating: 2019,
        winery: 'Anno Domini Vineyards',
        alcohol: 12.5,
        capacity: 0.75,
        description: 'Varieties: Cabernet\nFrancAllergens: Contains sulfites',
        price: 6.85,
        items_left: 50
    }
]);

db.wine.insertMany([
    {
        article: '829044',
        name: 'Vi de Vila Cims de Porrera',
        type: 'Red Unfortified still wines',
        country: 'Spain',
        region: 'D.O.Q. Priorat',
        vintage_dating: 2017,
        winery: 'Cims De Porrera',
        alcohol: Double(15),
        capacity: 0.75,
        description: 'Varieties: Carinyena / Mazuelo, Garnatxa\nNegraAllergens: Contains sulfites',
        price: 17.44,
        items_left: 50
    }
]);

db.wine.createIndex({article: 'text', name: 'text', winery: 'text', country: 'text', region: 'text'});
db.cart.createIndex({client_username: 1}, {unique: true});