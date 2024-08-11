def limpiar_messages(request, messages):
    if messages.get_messages(request):
    # Itera sobre los mensajes y los elimina de la cola
        for message in messages.get_messages(request):
            pass 

