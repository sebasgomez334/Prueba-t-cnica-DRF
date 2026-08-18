from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Llamamos primero al manejador por defecto de DRF para obtener la respuesta estándar
    response = exception_handler(exc, context)

    # Si la respuesta existe (es un error controlado por DRF)
    if response is not None:
        if response.status_code == 401:
            mensaje_feedback = "Acceso denegado. No estás autenticado o tu token ha expirado. Por favor, inicia sesión."
        else:
            mensaje_feedback = "Ocurrió un error en la solicitud."

        custom_data = {
            "error": True,
            "status_code": response.status_code,
            "mensaje": mensaje_feedback,
            "detalles": response.data
        }
        response.data = custom_data

    return response