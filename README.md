# Métodos alternativos para atribuição de mandatos nas eleições legislativas portuguesas.

Link to streamlit app: https://share.streamlit.io/tiagotvv/alternativa_mandatos/main/distribuicao_mandatos.py

* Eleições Legislativas: E se os mandatos fossem distribuídos de forma diferente? Nesta web app pode-se testar, com os resultados das eleições legislativas de 2019 e 2022, diferentes formas de atribuir mandatos, como círculo eleitoral único, utilização de círculo de compensação, fusão de pequenos círculos entre outras.

* Há também um what-if scenario para o PSD: o que aconteceria se o partido tivesse concorrido coligado? Qual seria o efeito na representatividade dos resultados eleitorais?

* Para avaliar a representatividade destes métodos alternativos, incluí o índice de Loosemore–Hanby (LHI) que mede a desproporção relativa entre votos e assentos obtidos pelos partidos em uma eleição. Para calcular o índice somamos o valor absoluto das diferenças (para que não haja cancelamento entre diferenças positivas e negativas) entre a porcentagem de votos recebidos (V) e a porcentagem assentos obtidos (S). A divisão por 2 é para limitar a faixa de valores do índice entre 0% e 100%. (fórmula no fim do documento)
 
 
EN Translation

* Legislative Elections: What if the elected candidates were selected differently? In this web app one can test, using the electoral results from 2019 and 2022, different ways to allocate the seats such as: one grand national electoral circle, the use of one compensation electoral circle, the merge of small electoral circles, among others.

* There is also one what-if scenario for the PSD (Social Democratic Party). What would happen if they ran in a coalition with CDS-PP?

* To quantitavely evaluate the representativeness of these alternative methods, I included the Loosemore-Hanby index (LHI) that measures the disproportionality of the electoral system. It computes the absolute difference between votes cast and seats obtained. To compute the index, we sum the absolute value of the differences (in order not to cancel positiva and negative differences) between the percentage of received votes (V) and the percentage of seats (S). The division by 2 is used to limit the range of values from 0% to 100%. (formula below)


#### Loosemore-Hanby Index formula: 

$LHI = 1/2 \sum_{i=1,...,n}{|V_i - S_i|}$
