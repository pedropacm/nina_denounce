O projeto nina_denounce gerencia o cadastro de denúncias. Possui uma API REST e consome uma API RPC do projeto nina_user.

Escrito em Python 2.7, utiliza uma base de dados SQLite3. Atualmente utiliza a mesma base de dados para produção e execução dos testes automatizados.

Para sua execução e teste é necessário garantir o serviço RPC do projeto nina_user esteja ativo.

A API REST é executada através de um servidor WSGI. No desenvolvimento foi utilizado o Gunicorn.

gunicorn --reload 'nina_denounce.app:get_app()'

Os testes automáticos foram escritos utilizando a biblioteca PyTest.