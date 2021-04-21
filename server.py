# SERVIDOR
import psutil, cpuinfo, datetime, time, platform, os, nmap, subprocess, socket, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname() 
PORT = 9998
HP = (HOST, PORT)
buffer_size = 1024
#32768
#nm = nmap.PortScanner()
server.bind(HP)
server.listen()
print("Servidor:", HOST, "esperando na porta", PORT, "Aguarde só um pouquinho!")
(client, addr) = server.accept()
print("Máquina do cliente conectada:", addr)
def processador():
    inicio = time.time() 
    lista = []
    lista_med = []
    info = cpuinfo.get_cpu_info()
    dic_cpu = []
    dic_cpu = psutil.cpu_stats()
    dic_cpu_nucleo = []
    dic_cpu_nucleo = psutil.cpu_percent(interval=1, percpu=True)
    lista_nucleo = []
    nome_cpu = info['brand']
    arq_cpu = info['arch']
    palavra_cpu = str(info['bits'])
    freq_base = info['hz_advertised']
    for i in range(10):
        freq_cpu = psutil.cpu_freq().current / 1000
        time.sleep(1)
        lista_med.append(freq_cpu)       
    freq_cpu = str(int(sum(lista_med)) / int(len(lista_med)))    
    lista_med_uso = []
    for i in range(10):
        uso_cpu = psutil.cpu_percent()
        time.sleep(1)
        lista_med_uso.append(uso_cpu)
    uso_cpu = str(int(sum(lista_med_uso)) / int(len(lista_med_uso)))
    lista_nucleo = psutil.cpu_percent(interval=1, percpu=True)
    nucleos_cpu_logicos = str(psutil.cpu_count(logical=True))
    nucleos_cpu_fisicos = str(psutil.cpu_count(logical=False))
    lista.append(nome_cpu)
    lista.append(arq_cpu)
    lista.append(palavra_cpu)   
    lista.append(freq_base)   
    lista.append(freq_cpu) 
    lista.append(uso_cpu) 
    lista.append(lista_nucleo) 
    lista.append(nucleos_cpu_logicos)
    lista.append(nucleos_cpu_fisicos)  
    fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")    
    return lista
def memoria():
    inicio = time.time()
    lista = []
    lista_med = []
    memoria_total = round(psutil.virtual_memory().total/1024**3) 
    memoria_livre = round(psutil.virtual_memory().free/1024**3)
    memoria_swap_total = round(psutil.swap_memory().total/1024**3)
    memoria_swap_livre = round(psutil.swap_memory().free/1024**3)
    for i in range(10):
        memoria_uso = psutil.virtual_memory().percent
        time.sleep(1)
        lista_med.append(memoria_uso)       
    memoria_uso = round((sum(lista_med) / len(lista_med)))
    lista.append(memoria_total)
    lista.append(memoria_livre)
    lista.append(memoria_uso)
    lista.append(memoria_swap_total)
    lista.append(memoria_swap_livre)
    fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")   
    return lista    
def armazenamento():    
    inicio = time.time()    
    lista = []   
    armazenamento_total = round(psutil.disk_usage(os.getcwd()).total/1024**3)
    armazenamento_livre = round(psutil.disk_usage(os.getcwd()).free/1024**3)
    armazenamento_uso = round(psutil.disk_usage(os.getcwd()).percent)    
    lista.append(armazenamento_total) 
    lista.append(armazenamento_livre) 
    lista.append(armazenamento_uso)     
    fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")   
    return lista 
def arquivo():    
    inicio = time.time()  
    diretorio = os.listdir() 
    dicionario_arq = {} 
    lista_diretorios = [] 
    dicionario_arq_dados = {}   
    d2 = {} 
    for arquivo in diretorio: 
        if os.path.isfile(arquivo): 
            size=(round(os.stat(arquivo).st_size / 1024)) # tamanho em bytes 
            path=os.path.abspath(arquivo) # caminho absoluto 
            filec=time.ctime(os.path.getctime(arquivo)) # criação do arquivo 
            filem=time.ctime(os.path.getmtime(arquivo)) # última modificação 
            filea=time.ctime(os.path.getatime(arquivo)) # último acesso 
            d2={'Tamanho (bytes)':size,'Caminho absoluto':path,'Criação':filec,'Última modificação':filem,'Último acesso':filea} 
            dicionario_arq_dados.update({arquivo:d2}) 
        else: 
            lista_diretorios.append(arquivo) 
    lista = [lista_diretorios, dicionario_arq_dados]    
    return lista
def pid():   
    inicio = time.time()   
    dicionario = {}
    key = 0
    for proc in psutil.process_iter():
        if psutil.pid_exists(proc.pid):   
            processID = proc.pid        
            try:            
                processName = proc.name()
                processExecutable = proc.exe()
                processCpuTime = round(proc.cpu_times().user,2)
                processMemory = round((proc.memory_info().rss / (1024*1024)),2)             
                processCreateTime = datetime.datetime.fromtimestamp(proc.create_time()).strftime("%d-%m-%Y %H:%M:%S")            
                lista = []
                lista.append(processName)
                lista.append(processID)
                lista.append(processExecutable) 
                lista.append(processCpuTime)
                lista.append(processMemory) 
                lista.append(processCreateTime)       
                dicionario [key] = lista
                key = key + 1            
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): 
               pass   
    fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")    
    return dicionario
def rede():
    inicio = time.time()   
    interfaces = psutil.net_if_addrs()
    nomes = []
    status = psutil.net_if_stats()
    for i in interfaces:
        nomes.append(str(i))
        dic_itf = psutil.net_if_addrs()
        dic_nic = psutil.net_if_stats()
        dic_io = psutil.net_io_counters(pernic=True, nowrap=True)
        lista = []
        ipv4 = dic_itf[nomes[0]][1][1]
        ipv6 = dic_itf[nomes[0]][2][1]
        mascara = dic_itf[nomes[0]][1][2]
        mac = dic_itf[nomes[0]][0][1]       
        lista.append(ipv4)
        lista.append(ipv6)
        lista.append(mascara)
        lista.append(mac)       
        fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")    
    return lista
'''def nmap():   
    inicio = time.time()   
    octeto = "0"
    dicionario = {}
    d2 = {}
    key = 0
    i = 0
    for octeto in range(6):    
        lista = []
        ip = ("%s%s").strip() % (base_ipv4, octeto)        
        nm.scan(ip)    
        for host in nm.all_hosts():
            ip_subrede = str(host).strip()       
            for proto in nm[host].all_protocols():
                protocolo_subrede = str(proto).upper()
                lport = nm[host][proto].keys()
                for port in lport:
                    porta_subrede = str(port).strip()
                    estado_porta_subrede = str(nm[host][proto][port]['state']).strip()
                d2={'Protocolo':protocolo_subrede, 'Porta':porta_subrede, 'Estado':estado_porta_subrede}        
            dicionario.update({ip_subrede:d2})       
    fim = time.time()
    print("Tempo da chamada:", round((fim-inicio),2), "segundo(s).")   
    return dicionario'''
while True:
    option = client.recv(buffer_size)   
    if option.decode('utf-8') == " ":
        print("Conexão bem-sucedida.")   
    elif option.decode('utf-8') == "1":
        bytes_resp = pickle.dumps(processador())
        client.send(bytes_resp)
    elif option.decode('utf-8') == "2":
        bytes_resp = pickle.dumps(memoria())
        client.send(bytes_resp)      
    elif option.decode('utf-8') == "3":
        bytes_resp = pickle.dumps(armazenamento())
        client.send(bytes_resp)   
    elif option.decode('utf-8') == "4":
        bytes_resp = pickle.dumps(arquivo())
        client.send(bytes_resp)      
    elif option.decode('utf-8') == "5":
        bytes_resp = pickle.dumps(pid())
        client.send(bytes_resp)      
    elif option.decode('utf-8') == "6":
        bytes_resp = pickle.dumps(rede())
        client.send(bytes_resp)
    elif option.decode('utf-8') == "7":
        ip = client.recv(buffer_size)
        endereco_ip = ip.decode('utf-8')
        base_ipv4 = endereco_ip       
        '''nmap_resultado = nmap()
        bytes_resp = pickle.dumps(nmap_resultado)
        client.send(bytes_resp)'''       
client.close()
server.close()
input("Pressione qualquer tecla para sair...")
