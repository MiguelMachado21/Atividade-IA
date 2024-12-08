## Trabalho Final de IA - Rastreio de Pessoas

Nesse trabalho, eu Miguel Fraga Machado, aluno de Inteligência Artificial, produzi um trabalho sobre rastreio de pessoas. Esse trabalho consiste na ideia de ajudar um comércio local a saber qual o fluxo de pessoas na frente do estabelecimento, assim podendo dar insights de melhoria de como aumentar esse fluxo etc. 

## Configuração do Ambiente Virtual

### Passos para criar e ativar um ambiente virtual:

1. **Criar o ambiente virtual:**

   ```bash
   python -m venv env-visao
   ```

2. **Ativar o ambiente virtual:**

   No macOS e Linux:

   ```bash
   source ./env-visao/bin/activate
   ```

   No Windows:

   ```bash
   .\env-visao\Scripts\activate
   ```

## Instalação de Dependências

Certifique-se de que seu ambiente virtual esteja ativado. Instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Conteúdo do arquivo `requirements.txt`:

```text
numpy==2.0.0
opencv-python==4.10.0.84
```

## Funcionalidade do código

Um ROI é demarcado ao redor da porta, qual a ideia disso? Ter uma análise melhor de quantas pessoas passam em frente a porta do estabelecimento, qual o fluxo real disso. Isso é possível com o ROI devidamente configurado e que conta as pessoas. 

Não tive mais tempo para aperfeiçoar e fazer um contador (toda vez que ele identifica, conta +1 e assim vai). Ele está funcional e daria para ser aplicado em um pequeno projeto, para testes. 

## Controles

Durante a execução do projeto, você pode:

- Pressionar 'p' para pausar/continuar o vídeo.
- Pressionar 'q' para sair do aplicativo.