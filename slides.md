%title: O que as redes sociais podem nos dizer sobre a opinião pública?
%author: Marco Toledo
%date: 2021-12-21

-> O quão acuradas são predições da opinião pública sobre a política com base na extração de dados do Twitter? <-
=====

-> Marco Toledo, RA: 11796419 <-
-> BCC020 <-
-> [Github](https://github.com/Ocramoi) <-

---

-> # São as redes sociais uma boa amostra da população? <-

O acesso às redes sociais, sendo dependente do acesso a tecnologias emergentes e recursos não triviais, tem sido, desde sua incepção, representativa de uma parcela muito escusa da população, trazendo à qualquer análise de seus proponentes um caráter sectarista. Porém, com o avanço do acesso a novas tencologia, as barreiras de acesso ao mundo digital têm caído por chão, ampliando a parcela da população representada nas redes.

---

Essa expansão do acesso digital, somado ao caráter colaborativo da chamada _web 2.0_, onde conteúdo é criado e replicado pelos próprios usuários da plataforma, vem formando nas redes sociais comunidades expressivas e cada vez mais próximas da população no geral, o que nos trás a pergunta:

-> **seria a internet a próxima fronteira da pesquisa pública?** <-

---

-> # O estado atual da pesquisa na área <-

Hoje temos diversos estudos sobre a análise pública com base nas redes sociais, em especial no *Twitter*, já que a rede se baseia em publicações de tamanho fixo em timelines públicas, não divididos em grupos ou comunidades, porém em grande parte esses se focam em questões fechadas, como preferencia  de voto ou popularidade de conteúdos diversos. 
A proposta desse estudo então é colher todo o conteúdo possível sobre um tema específico, com base em palavras chaves relacionadas e realizar uma análise qualitativa do sentimento relacionado ao assunto, como expresso pelos usuários da rede.

---

O objetivo dessa análise é observar se essas técnicas online de extração da opiniao pública conseguem manter a precisão de pesquisas tradicionais feitas por entrevistas pessoais, já que esse método tradicional é extremamente custoso e demorado, sendo a oportunidade de realizar pesquisas à distância, de maneira automatizada e contínua, no contexto analisado da política institucional, um possível abridor de portas para uma forma de governança e campanha mais próxima da realidade da população em si, com uma resposta em tempo real quanto a ações governamentais e de campanha, por exemplo.

---

-> # Como foi realizada tal análise? <-

-> ## Extração de dados e pré processamento de dados <-

A extração dos dados foi feita pela [pesquisa de arquivo da API pública gratuita do Twitter](https://developer.twitter.com/en/docs/twitter-api/premium/search-api/quick-start/premium-full-archive) por termos relacionados ao atual governo federal brasileiro, objeto desse estudo, como:
- Bolsonaro
- Presidente
- Governo
- País
- 'Mito'
Com um subsequente processamento de anonimização, exclusão de duplicatas, *retweets*, postagens contendo links, etc.

---

-> # Como foi realizada tal análise? <-

-> ## Análise de sentimento <-

A análise do "sentimento" do corpus extraído então foi subsequentemente feito utilizando um *fork* pessoal da ferramenta de análise lexical de sentimentos [LeIA](https://github.com/Ocramoi/LeIA/), extraindo o sentimento composto de cada postagem.

---

-> # Como foi realizada tal análise? <-

-> ## Comparação dos resultados <-

Com os valores ternários de sentimento resultantes da análise de sentimento (postagens positivas, neutras e negativas), a porcentagem de aprovação do governo em relação as respostas totais e em relação apenas às respostas binárias (aprova ou não aprova) foi inferida e comparada com valores reais da pesquisa [IPEC](https://www.ipec-inteligencia.com.br/Repository/Files/26/04_13_Ipec_JOB_21_0046-7_Avaliacao_do_Governo_Relatorio_de_tabelas.pdf) no mesmo período.

---

-> # Resultados <-

Os dados sobre a amostra são os seguintes:

->  Pesquisas IPEC:                                           Análise do twitter:                                   <-
-> |             | Aprova   | Desaprova   | Outro* | Total | |             | Positivo | Negativo | Neutro  | Total | <-
->  |-------------+----------+-------------+--------+-------| |-------------+----------+----------+---------+-------| <-
->  | Contagem    |      601 |        1321 |     80 |  2002 | | Contagem    |      388 |      836 |     300 |  1524 | <-
->  | Porcentagem |      30% |         66% |     4% |  100% | | Porcentagem |      25% |      55% |     20% |  100% | <-

--- 

-> # Resultados <-

Podemos ber que há uma grande discrepância nesses valores brutos, porém se analisarmos os dados relativos às respostas binárias (aprova/desaprova na pesquisa da IPEC e positivo/negativo na análise de sentimentos) obtemos dados mais promissores:

-> |         | Aprova/Positivo | Desaprova/Negativo | <-
-> |---------+-----------------+--------------------|
-> | IPEC    |      31.3%      |        68.7%       | <-
-> | Twitter |      31.7%      |        68.3%       | <-

O viés por respostas neutras é, de certa forma, esperado em uma busca simples apenas por palavras chave, já que as postagens retornadas não necessariamente contêm opiniões definidas, como no caso de notícias, ou mesmo contém opiniões que não podem ser analisadas lexicalmente pela ferramenta utilizada.

---

-> # Conclusão <-

Os dados observados, mesmo não sendo conclusivos por si só, indicam a validade de pesquisas futuras nesse campo, contornando limitações encontradas nesse trabalho, como os limites da API gratuita do *Twitter* que impediram a análise de múltiplos meses para maior inferência estatística, ou mesmo um corpus maior em um mesmo mês, além da experimentação de outros métodos de análise, como a o uso de modelos supervisionados de regressão a partir da classificação manual do corpus ou usando bases de dados já desenvolvidas, como a [TweetSentBR](https://bitbucket.org/HBrum/tweetsentbr/).

---

-> O artigo na íntegra, assim como o código desenvolvido para todo o processo, pode ser acessado no repositório abaixo: <-

-> [Ocramoi/twitter-political-analysis-accuracy](https://github.com/Ocramoi/twitter-political-analysis-accuracy) <-

-> **Muito obrigado!** <-
