# Algoritimo para balanceamento de servidor

Para executar so rodar o comando abaixo passando o parametro obrigatório de input em **--file**.
Existem parametros opcionais que tem valor default por exemplo:
* **--ttask** que é o tempo que a tarefa fica ativa, o valor default é 5.
* **--umax=2** número máximo de tarefa por servidores, valor default é 10
* **--output** Arquivo de output nome default é output.txt
`python execute.py --file=input.txt --ttask=4 --umax=2 --output=out.txt`

