Um orquestrador (**orquestrador.py**) que trabalha de forma síncrona, centralizando as chamadas dos microsserviços e fazendo rollback em caso de falhas. O orquestrador será responsável por coordenar todo o fluxo de transações distribuídas, garantindo que cada serviço execute sua parte e revertendo operações em caso de erro.

---

Dependências:

Flask (instale com **'pip install Flask'**)
dotenv (instale com **'pip install python.dotenv'**)


