add_products_schema = {
    'price': {'type': 'integer', 'required': True, 'min': 0},
    'qty': {'type': 'integer', 'required': True, 'min': 1},
    'description': {'type': 'string', 'required': True, 'empty': False},
    'category': {'type': 'string', 'required': True, 'empty': False},
    'location': {'type': 'string', 'required': True, 'empty': False},
}