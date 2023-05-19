import serial
import time
import struct

def menu(matricula):

    acoes = {
        "1": (solicitar_dados, "161"),
        "2": (solicitar_dados, "162"),
        "3": (solicitar_dados, "163"),
        "4": (envia, "177"),
        "5": (envia, "178"),
        "6": (envia, "179")
        }
    #limpa terminal
    print('\033c')
    print('Bem vindo ao programa de comunicação serial.')
    print('Escolha uma opção:')
    print('1 - Solicitar int')
    print('2 - Solicitar float')
    print('3 - Solicitar string')
    print('4 - Enviar int')
    print('5 - Enviar float')
    print('6 - Enviar string')
    print('7 - Sair')
    opcao = int(input('Digite a opção desejada: '))
    if opcao == 7:
        return True
     
    serial_port = abre_porta('/dev/serial0', 9600)
    if serial_port != None:
        funcao, solicitacao = acoes[str(opcao)]
        recebido = funcao(serial_port, matricula, int(solicitacao))

        if recebido != None:
            print(recebido)
            time.sleep(5)
        return False
    else:
        print('Não foi possível abrir a porta serial.')
        time.sleep(5)
        return False

# Enviar dados pela porta UART
def solicitar_dados(serial_port, dados_enviados, solicitacao):

    dados_enviados = [solicitacao] + dados_enviados
    bytes_enviados = serial_port.write(bytes(dados_enviados))
    if bytes_enviados > 0:
        print('Dados enviados com sucesso.')
    else:
        print('Não foi possível enviar os dados.')
    time.sleep(1)

    if solicitacao == 161:
        return receber_int(serial_port)
    elif solicitacao == 162:
        return receber_float(serial_port)
    elif solicitacao == 163:
        return receber_string(serial_port)

# Ler dados da porta UART
def receber_int(serial_port):
    dados_recebidos = serial_port.read(4) 
    inteiro_recebido = int.from_bytes(dados_recebidos, byteorder='little')
    serial_port.close()
    return inteiro_recebido

def receber_float(serial_port):
    dados_recebidos = serial_port.read(4)
    dados_recebidos = bytes(dados_recebidos)
    float_recebido = struct.unpack('f',dados_recebidos)
    serial_port.close()
    return float_recebido

def receber_string(serial_port):
    tamanho_string = serial_port.read(1)
    tamanho_string = int.from_bytes(tamanho_string, byteorder='little')

    dados_recebidos = serial_port.read(tamanho_string) 
    string_recebida = dados_recebidos.decode('utf-8').strip()
    serial_port.close()
    return string_recebida

def abre_porta(porta, baud_rate):
    try:
        serial_port = serial.Serial(porta, baud_rate)
        print('Porta serial aberta.')
        #limpar buffer
        serial_port.reset_input_buffer()
        serial_port.reset_output_buffer()
        return serial_port
    except:
        print('Erro ao abrir a porta serial.')
        return None

def envia(serial_port, dados_enviados, solicitacao):
    if solicitacao == 177:
        bytes_int = struct.pack('i', 13)
        dados_enviados = [solicitacao] + list(bytes_int) + dados_enviados
    elif solicitacao == 178:
        bytes_float = struct.pack('f', 13.2)
        dados_enviados = [solicitacao] + list(bytes_float) + dados_enviados
    elif solicitacao == 179:
        tamanho_string = len('teste')
        dados_enviados = [solicitacao] + [tamanho_string] + list('teste'.encode('utf-8')) + dados_enviados
    
    bytes_enviados = serial_port.write(bytes(dados_enviados))
    if bytes_enviados > 0:
        print('Dados enviados com sucesso.')
    else:
        print('Não foi possível enviar os dados.')
    time.sleep(1)

if __name__ == '__main__':
    matricula = [ 4, 4, 9, 8]
    
    while True:
        if menu(matricula):
            break

    print('Fim do programa.')
