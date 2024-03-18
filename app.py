from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

# Conexão com o servidor RabbitMQ
credentials = pika.PlainCredentials('inteli', 'inteli')
parameters = pika.ConnectionParameters('rabbitmq-1ohw', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declaração da fila
channel.queue_declare(queue='fila_de_teste')

@app.route('/enviar', methods=['POST'])
def enviar_mensagem():
    # Recebe os dados da solicitação
    dados = request.json

    # Obtém a mensagem a partir dos dados recebidos
    mensagem = dados.get('mensagem')

    # Publica a mensagem na fila do RabbitMQ
    channel.basic_publish(exchange='', routing_key='fila_de_teste', body=mensagem)
    print("Mensagem enviada para a fila:", mensagem)

    # Retorna uma resposta indicando que a mensagem foi enviada com sucesso
    return jsonify({'mensagem': 'Mensagem enviada para a fila do RabbitMQ'}), 200

@app.route('/ler', methods=['GET'])
def ler_mensagem():
    # Obtém a próxima mensagem da fila
    method_frame, header_frame, body = channel.basic_get(queue='fila_de_teste')

    if method_frame:
        # Se houver uma mensagem na fila, retorna-a como resposta
        mensagem = body.decode()
        print("Mensagem lida da fila:", mensagem)
        return jsonify({'mensagem': mensagem}), 200
    else:
        # Se não houver mensagem na fila, retorna uma mensagem indicando que a fila está vazia
        return jsonify({'mensagem': 'A fila está vazia'}), 404

if __name__ == '__main__':
    app.run(debug=True)
