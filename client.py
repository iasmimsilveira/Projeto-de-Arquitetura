#CLIENTE
import cpuinfo, datetime, time, platform, os, nmap, subprocess, socket, pickle,psutil

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname() 
PORT = 9999
HP = (HOST, PORT)
buffer_size = 1024
def menu():
    print('============================')
    print('INFORMAÇÕES')
    print('============================')
    print('|1| Processador')
    print('|2| Memória')
    print('|3| Armazenamento')
    print('|4| Arquivos e diretórios')
    print('|5| Processos | PID')
    print('|6| Rede')
    print('|7| Nmap')
    print('============================')      
def option_um():
    lista = []
    print("\n1- Processador:\n")
    title_processador = ['Modelo:', 'Arquitetura:', 'Palavra (bits):', 'Frequência Base:', 'Frequência média (GHz):', 'Uso (%):', 'Uso núcleos (%):', 'Núcleos Lógicos:', 'Núcleos Físicos:', 'Troca de contexto (boot):', 'Interrupções (boot):', 'Chamadas de sistema (boot):']
    var = ' | '.join(map(str,resposta[6]))
    valor_processador = [resposta[0], resposta[1], resposta[2], resposta[3], resposta[4], resposta[5], var, resposta[7], resposta[8]]
    for x,y in zip(title_processador,valor_processador):
        print ('{:30}{:30}'.format(x,y))
    time.sleep(8)
    os.system('cls')
    lista.append(title_processador) 
    return lista
def option_dois():
    lista = []
    print("\n2- Memória\n")
    title_memoria = ['RAM total (GB):', 'RAM livre (GB):', 'RAM uso (%):', 'Swap total (GB):', 'Swap livre (GB):']
    for x,y in zip(title_memoria,resposta):
        print ('{:30}{:30}'.format(x,y))
    time.sleep(8)
    os.system('cls') 
    lista.append(title_memoria)
    return lista
def option_tres():
    lista = []
    print("\n3- Armazenamento\n")
    title_armazenamento = ['Total (GB):', 'Livre (GB):', 'Utilizado (%):']
    for x,y in zip(title_armazenamento,resposta):
        print ('{:30}{:30}'.format(x,y))
    time.sleep(8)
    os.system('cls') 
    lista.append(title_armazenamento)
    return lista
def option_quatro():
    lista = []
    print("\n4- Arquivos e Diretórios\n")
    print("")
    print("\nDiretórios\n")               
    for diretorio in resposta[0]:
        print(diretorio)                
    print("")
    print("\nArquivos\n")
    d1 = resposta[1]
    for key, d1 in d1.items():
        print(key)
        for attribute,value in d1.items():
            print('{}: {}'.format(attribute,value))
        print("")                
    time.sleep(8)
    os.system('cls') 
    lista.append(diretorio)
    return lista
def option_cinco():
    lista = []
    title_pid = ['Nome:', 'PID:', 'Executável:', 'CPU (s):', 'Memória (MB):']               
    i = 0        
    while i <= len(resposta):
        valor_pid = [resposta[i][0], resposta[i][1], resposta[i][2], resposta[i][3], resposta[i][4]]
        i = i + 1                  
        for x,y in zip(title_pid,valor_pid):
            print ('{:30}{:<30}'.format(x,y))
        print("")
    time.sleep(8)
    os.system('cls')
    lista.append(title_pid)
    return lista
def option_seis():
    lista = []
    print("\n6- Rede\n")
    title_rede = ['IPv4:', 'IPv6:', 'Máscara:', 'MAC:']
    valor_rede = [resposta[0], resposta[1], resposta[2], resposta[3]]
    for x,y in zip(title_rede,valor_rede):
        print ('{:30}{:30}'.format(x,y))
    time.sleep(8)
    os.system('cls')
    lista.append(title_rede)
    return lista
def option_sete():
    lista = []
    endereco_ip = input("Entre com o número do IP da rede: ")
    client.send(option.encode('utf-8'))
    client.send(endereco_ip.encode('utf-8'))               
    bytes_resp = client.recv(buffer_size)
    resposta = pickle.loads(bytes_resp)            
    '''print("\n7- NMAP\n")       
    d1=resposta
    for key, d1 in d1.items():
        print(key)
        for attribute,value in d1.items():
            print('{}: {}'.format(attribute,value))
        print("")
    time.sleep(10)
    os.system('cls')                   
    title_nmap = ['IP (sub-rede):', 'Protocolo:', 'Porta:', 'Estado:']               
    for key, value in resposta.items():
        valor_nmap = [resposta[key], resposta.get(key, value[0]), resposta.get(key, value[1]), resposta.get(key, value[3])]'''
    lista.append(resposta)
    return lista  
try: 
    client.connect(HP)
    option = " "
    client.send(option.encode('utf-8')) 
    options = ("1","2", "3", "4", "5", "6")   
    while True:
        menu()
        option = input('DIGITE SUA OPÇÃO:')
        if (option in options):
            client.send(option.encode('utf-8'))
            bytes_resp = client.recv(buffer_size)
            resposta = pickle.loads(bytes_resp)          
            if option == "1":
                option_um()           
            elif option == "2":
                option_dois()       
            elif option == "3":
                option_tres()                         
            elif option == "4":  
                option_quatro()                                    
            elif option == "5":
                option_cinco()                 
            elif option == "6":
                option_seis() 
        if option == "7":
            option_sete()                
except Exception as erro:
    print(str(erro))
client.close()
input("Para sair pressione qualquer tecla...")