def validate_user_data(data):
    """
    Valida los datos de un usuario
    Retorna: (is_valid, error_message)
    """
    if not data:
        return False, 'No se proporcionaron datos'
    
    if 'name' not in data or not data['name']:
        return False, 'El campo name es requerido'
    
    if 'email' not in data or not data['email']:
        return False, 'El campo email es requerido'
    
    # Validación básica de email
    if '@' not in data['email'] or '.' not in data['email']:
        return False, 'El email no tiene un formato válido'
    
    return True, None


def validate_product_data(data):
    """
    Valida los datos de un producto
    Retorna: (is_valid, error_message)
    """
    if not data:
        return False, 'No se proporcionaron datos'
    
    required_fields = ['name', 'price', 'category_id']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f'El campo {field} es requerido'
    
    # Validar que el precio sea un número positivo
    try:
        price = float(data['price'])
        if price <= 0:
            return False, 'El precio debe ser mayor a 0'
    except (ValueError, TypeError):
        return False, 'El precio debe ser un número válido'
    
    # Validar que category_id sea un número
    try:
        int(data['category_id'])
    except (ValueError, TypeError):
        return False, 'El category_id debe ser un número válido'
    
    return True, None
